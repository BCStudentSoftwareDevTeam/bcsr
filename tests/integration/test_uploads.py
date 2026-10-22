from io import BytesIO
from pathlib import Path

import pytest

from app.models import Courses

pytestmark = pytest.mark.integration


@pytest.mark.parametrize('username', ['faculty', 'admin', 'program_chair', 'division_chair'])
def test_authenticated_upload_saves_file_and_metadata(client, login, demo_data, tmp_path, username):
    login(username)
    course = demo_data['faculty_course']
    response = client.post(f'/uploads/{course.CID}', data={
        'file': (BytesIO(b'%PDF-1.4 original'), 'syllabus.pdf'),
    })
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/courses')
    saved = Courses.get_by_id(course.CID)
    assert username in saved.lastModified
    assert Path(str(tmp_path / 'uploads') + saved.filePath).read_bytes() == b'%PDF-1.4 original'


def test_missing_file_is_rejected(client, login, demo_data):
    login()
    course = demo_data['faculty_course']
    response = client.post(f'/uploads/{course.CID}', data={})
    assert response.status_code == 400
    assert Courses.get_by_id(course.CID).filePath is None


def test_unknown_user_cannot_upload(client, demo_data, tmp_path):
    client.environ_base['eppn'] = 'unknown@example.test'
    course = demo_data['faculty_course']
    before = {path: path.read_bytes() for path in (tmp_path / 'uploads').rglob('*')
              if path.is_file()}
    response = client.post(f'/uploads/{course.CID}', data={
        'file': (BytesIO(b'%PDF-1.4 rejected'), 'syllabus.pdf'),
    })
    assert response.status_code == 403
    assert Courses.get_by_id(course.CID).filePath is None
    after = {path: path.read_bytes() for path in (tmp_path / 'uploads').rglob('*')
             if path.is_file()}
    assert after == before


def test_archived_demo_syllabus_can_be_downloaded(client, login, demo_data):
    login()
    response = client.get(f"/download/{demo_data['archived_course'].CID}")
    assert response.status_code == 200
    assert response.data == b'%PDF-1.4 demo syllabus'
    response.close()
