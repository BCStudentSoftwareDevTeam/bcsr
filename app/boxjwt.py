import json
import os
import time
import binascii
from urllib2 import urlopen
from urllib2 import Request
from urllib import urlencode
import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from boxsdk import JWTAuth
from boxsdk import Client

import os
import requests

import os
import datetime

from logic.getAll import *
from boxsdk.exception import BoxAPIException


class BoxUploader():
    """
    Creates folders for term/divisions/programs inside Box application.
    Saves the uploaded files in the right directory inside the box.

    """
    def __init__(self, complete_path="", CID=0):
        """
        
        """

        if complete_path != "":
            self.complete_path = complete_path

        if CID != 0:
            self.new_path = self.convert_prefix_to_program(CID)
        self.config = json.load(open('/var/www/html/bcsr-flask/app/config.json'))
        appAuth = self.config["boxAppSettings"]["appAuth"]
        privateKey = appAuth["privateKey"]
        passphrase = appAuth["passphrase"]

        # To decrypt the private key we use the cryptography library
        # (https://cryptography.io/en/latest/)
        key = load_pem_private_key(
         data=privateKey.encode('utf8'),
         password=passphrase.encode('utf8'),
         backend=default_backend(),
        )

        # We will need the authentication_url  again later,
        # so it is handy to define here
        authentication_url = 'https://api.box.com/oauth2/token'

        claims = {
         'iss': self.config['boxAppSettings']['clientID'],
         'sub': self.config['enterpriseID'],
         'box_sub_type': 'enterprise',
         'aud': authentication_url,
         # This is an identifier that helps protect against
         # replay attacks
         'jti': binascii.hexlify(os.urandom(64)),
         # We give the assertion a lifetime of 45 seconds
         # before it expires
         'exp': int(round(time.time(), 0) + 45)
        }

        keyId = self.config['boxAppSettings']['appAuth']['publicKeyID']

        # Rather than constructing the JWT assertion manually, we are
        # using the pyjwt library.
        assertion = jwt.encode(
         claims,
         key,
         # The API support "RS256", "RS384", and "RS512" encryption
         algorithm='RS512',
         headers={
           'yl95olil': keyId
         }
        )

        params = urlencode({
         # This specifies that we are using a JWT assertion
         # to authenticate
         'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
         # Our JWT assertion
         'assertion': assertion,
         # The OAuth 2 client ID and secret
         'client_id': self.config['boxAppSettings']['clientID'],
         'client_secret': self.config['boxAppSettings']['clientSecret']
        }).encode()

        # Make the request, parse the JSON,
        # and extract the access token
        request = Request(authentication_url, params)
        response = urlopen(request).read()
        access_token = json.loads(response)['access_token']

        # Folder 0 is the root folder for this account
        # and should be empty by default
        request = Request('https://api.box.com/2.0/folders/0', None, {
         'Authorization': "Bearer %s" % access_token
        })
        response = urlopen(request).read()

        #creates a new client that can make authenticated calls to the Box API
        self.sdk = JWTAuth.from_settings_file('/var/www/html/bcsr-flask/app/config.json')
        self.client = Client(self.sdk)


    def fileUpload(self, term):
        """
        Finds the file directory inside box based off the complete_path, which is the file path in our server.
        Uploads file to the box.
        """
        box_path = self.new_path.split("/")[-4:-1]
        # get the semester id
        semester = Semesters.get(Semesters.SEID == term)

        # get the dictionary that holds all Box API folder ids and get that semester's folder id
        box_folder_dict = eval(semester.box_folders)
        # get program folder id
        prog_folder = box_folder_dict[box_path[0]][box_path[1]][box_path[2]]

        try:
            # upload to folder
            box_folder_id = self.client.folder(prog_folder).upload(self.complete_path)
        except BoxAPIException as ee:
            # upload new version of the file in case of error.
            file_id = ee.context_info["conflicts"]["id"]
            box_folder_id = self.client.file(file_id).update_contents(self.complete_path)

    def convert_prefix_to_program(self, CID):
        """
        Convert Prefix to Program Name.
        Example: BIO to Biology
        """
        # Bo
        self.c = Courses.get(Courses.CID == CID)
        new_path = self.complete_path.replace(self.c.prefix, self.c.PID.name, 1).replace(self.c.PID.DID.name.replace(" ", ""), "Division" + str(self.c.PID.DID.DID), 1)
        return new_path


    def createAllFolders(self, term):
        term_dict = {}
        try:
            folder = self.client.folder(folder_id = "0").create_subfolder(term)
            term_folder = folder["id"]
            term_dict[term] = {}
            term_dict[term]["folder_id"] = term_folder
        except BoxAPIException as e:
            term_folder = e.context_info["conflicts"][0]["id"]


        dictionaries = GetAll().create_dictionaries(term)
        divs = dictionaries[0]
        progs = dictionaries[1]

        for div in divs:
            try:
                folder = self.client.folder(folder_id=term_folder).create_subfolder("Division"+str(div.DID))
                div_folder = folder["id"]
                term_dict[term]["Division"+str(div.DID)] = {}
                term_dict[term]["Division"+str(div.DID)]["folder_id"] = div_folder
            except BoxAPIException as e:
                div_folder =e.context_info["conflicts"][0]["id"]

            for prog in divs[div]:
                try:
                    prog_folder = self.client.folder(folder_id=div_folder).create_subfolder(prog.name.replace(" ", "_"))
                    prog_folder_id = prog_folder["id"]
                    term_dict[term]["Division"+str(div.DID)][prog.name] = prog_folder_id
                except:
                    prog_folder_id =e.context_info["conflicts"][0]["id"]

        if len(term_dict) > 0:
            t = Semesters.get(Semesters.SEID == term)
            t.box_folders = str(term_dict)
            t.save()
