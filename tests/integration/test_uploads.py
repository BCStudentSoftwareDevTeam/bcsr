from io import BytesIO
from pathlib import Path

import pytest

from app.models import Courses

pytestmark = pytest.mark.integration


def upload(client, course, token, content=b'%PDF-1.4 original'):
    return client.post(f'/uploads/{course.CID}', data={
        'uploadToken': token,
        'file': (BytesIO(content), 'syllabus.pdf'),
    })


@pytest.mark.parametrize('username', ['faculty', 'admin', 'program_chair', 'division_chair'])
def test_authorized_upload_saves_file_and_metadata(client, login, demo_data, tmp_path, username):
    token = login(username)
    course = demo_data['faculty_course']
    response = upload(client, course, token)
    assert response.status_code == 303
    assert response.headers['Location'].endswith('/courses')
    saved = Courses.get_by_id(course.CID)
    assert username in saved.lastModified
    assert Path(str(tmp_path / 'uploads') + saved.filePath).read_bytes() == b'%PDF-1.4 original'


def test_repeat_submission_preserves_original(client, login, demo_data, tmp_path):
    token = login()
    course = demo_data['faculty_course']
    assert upload(client, course, token).status_code == 303
    original = Courses.get_by_id(course.CID)
    assert upload(client, course, token, b'replacement').status_code == 409
    saved = Courses.get_by_id(course.CID)
    assert (saved.filePath, saved.lastModified) == (original.filePath, original.lastModified)
    assert Path(str(tmp_path / 'uploads') + saved.filePath).read_bytes() == b'%PDF-1.4 original'


@pytest.mark.parametrize('token', ['', 'invalid-token'])
def test_missing_or_invalid_token_does_not_save(client, login, demo_data, tmp_path, token):
    login()
    course = demo_data['faculty_course']
    before = {path: path.read_bytes() for path in (tmp_path / 'uploads').rglob('*')
              if path.is_file()}
    assert upload(client, course, token).status_code == 403
    assert Courses.get_by_id(course.CID).filePath is None
    after = {path: path.read_bytes() for path in (tmp_path / 'uploads').rglob('*')
             if path.is_file()}
    assert after == before


def test_unrelated_faculty_cannot_upload(client, login, demo_data):
    token = login('other_faculty')
    course = demo_data['faculty_course']
    assert upload(client, course, token).status_code == 403
    assert Courses.get_by_id(course.CID).filePath is None


def test_missing_file_is_rejected(client, login, demo_data):
    token = login()
    response = client.post(f"/uploads/{demo_data['faculty_course'].CID}",
                           data={'uploadToken': token})
    assert response.status_code == 400


def test_archived_demo_syllabus_can_be_downloaded(client, login, demo_data):
    login()
    response = client.get(f"/download/{demo_data['archived_course'].CID}")
    assert response.status_code == 200
    assert response.data == b'%PDF-1.4 demo syllabus'
    response.close()
