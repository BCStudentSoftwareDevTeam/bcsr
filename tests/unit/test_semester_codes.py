import pytest

from app.logic.getSemesterManagement import GetSemesterManagement

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(('year', 'term', 'expected'), [
    ('2026', '11', '202611'),
    ('2026', '12', '202512'),
    ('2026', '13', '202513'),
    ('2000', '12', '199912'),
])
def test_semester_code_uses_academic_year(year, term, expected):
    assert GetSemesterManagement().create_seid({'year': year, 'term': term}) == expected
