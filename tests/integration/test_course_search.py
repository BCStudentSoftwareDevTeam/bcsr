import pytest

pytestmark = pytest.mark.integration


def test_search_returns_matching_courses_newest_first(client, login):
    login()
    response = client.get('/course-search', query_string={'prefix': ' CSC ', 'number': '226'})
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert html.index('Fall-2026') < html.index('Spring-2026')
    assert 'CSC-226-A' in html
    assert 'HIS-226-A' not in html
    assert 'Not uploaded' in html
    assert 'Download' in html


@pytest.mark.parametrize(('query', 'message'), [
    ({'prefix': 'CSC'}, 'Please enter a course number'),
    ({'number': '226'}, 'Please enter a course prefix'),
    ({'prefix': 'XYZ', 'number': '999'}, 'No courses found'),
])
def test_search_feedback(client, query, message):
    response = client.get('/course-search', query_string=query)
    assert response.status_code == 200
    assert message in response.get_data(as_text=True)
