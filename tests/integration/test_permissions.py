import pytest

from app.logic.getAuthUser import AuthorizedUser
from app.models import Courses, Users

pytestmark = pytest.mark.integration


@pytest.mark.parametrize(('username', 'expected'), [
    ('admin', 200), ('faculty', 403), ('program_chair', 403),
    ('division_chair', 403), ('unknown', 403),
])
def test_management_requires_administrator(client, username, expected):
    response = client.get('/admin/semesterManagement',
                          environ_overrides={'eppn': username + '@example.test'})
    assert response.status_code == expected


def test_missing_identity_is_denied(client):
    assert client.get('/admin/semesterManagement').status_code == 403


@pytest.mark.parametrize(('username', 'role'), [
    ('admin', 'admin'), ('division_chair', 'division'),
    ('program_chair', 'program'), ('faculty', 'faculty'),
])
def test_seeded_user_roles(client, username, role):
    from app import app
    with app.test_request_context(environ_overrides={'eppn': username + '@example.test'}):
        assert AuthorizedUser().user_level() == role


@pytest.mark.parametrize('changed_prefix', ['CHANGED', 'REPLACED'])
def test_demo_dataset_is_fresh_for_each_test(demo_data, changed_prefix):
    assert Users.select().count() == 5
    assert Courses.select().count() == 3
    assert demo_data['faculty_course'].PID.DID == demo_data['science']
    assert demo_data['archived_course'].SEID == demo_data['previous_term']
    assert demo_data['faculty_course'].filePath is None
    assert demo_data['faculty_course'].prefix == 'CSC'
    # Each invocation must start fresh even after a previous test committed edits.
    Courses.update(prefix=changed_prefix).where(
        Courses.CID == demo_data['faculty_course'].CID).execute()
