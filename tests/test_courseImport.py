import io
import unittest

from openpyxl import Workbook

from app.logic import courseImport as ci

HEADERS = ['CRN', 'Subject', 'Course Number', 'Sequence', 'Title', 'CrossList Courses',
           'Primary Instructor Last Name', 'Primary Instructor First Name', 'Primary Instructor Username',
           'Instructor2 Last Name', 'Instructor2 First Name', 'Instructor2 Username']
PREFIXES = {'CSC': 1, 'MAT': 2}


def csv_file(*rows, headers=HEADERS):
  lines = [",".join(headers)] + [",".join(str(c) for c in r) for r in rows]
  return io.BytesIO("\n".join(lines).encode('utf-8'))


def course(crn, prefix, number, section, user='smithj', **extra):
  return [crn, prefix, number, section, 'A Title', '', 'Smith', 'Jo', user, '', '', ''] if not extra else \
         [crn, prefix, number, section, 'A Title', '', 'Smith', 'Jo', user, extra.get('l2', ''), extra.get('f2', ''), extra.get('u2', '')]


class ParseTests(unittest.TestCase):
  def test_csv_rows_parse_with_spreadsheet_row_numbers(self):
    rows = ci.parse_course_file(csv_file(course(1, 'csc', '226', 'a'), course(2, 'MAT', '101', 'B')), 'x.csv')
    self.assertEqual([r['row'] for r in rows], [2, 3])
    self.assertEqual((rows[0]['prefix'], rows[0]['number'], rows[0]['section']), ('CSC', '226', 'A'))
    self.assertEqual(rows[0]['instructors'][0]['username'], 'smithj')

  def test_blank_rows_are_dropped(self):
    rows = ci.parse_course_file(csv_file(course(1, 'CSC', '226', 'A'), ['', '', ''], course(2, 'CSC', '230', 'A')), 'x.csv')
    self.assertEqual(len(rows), 2)
    self.assertEqual(rows[1]['row'], 4)

  def test_xlsx_numbers_do_not_become_floats(self):
    wb = Workbook()
    ws = wb.active
    ws.append(HEADERS)
    ws.append([21540, 'CSC', 226, 'A', 'Software Engineering', None, 'N', 'A', 'nyabutoa', None, None, None])
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    row = ci.parse_course_file(buf, 'courses.xlsx')[0]
    self.assertEqual((row['crn'], row['number']), ('21540', '226'))

  def test_alternate_header_layouts(self):
    for headers in (['CRN_KEY', 'SUBJ_CODE', 'CRSE_NUMBER', 'SEQ_NUMBER_KEY', 'TITLE', 'PRIMARY_INSTRUCTOR_USERNAME'],
                    ['crn', 'subject', 'course number', 'sequence', 'title', 'primary instructor username']):
      rows = ci.parse_course_file(csv_file([1, 'CSC', '226', 'A', 'T', 'smithj'], headers=headers), 'x.csv')
      self.assertEqual(rows[0]['instructors'][0]['username'], 'smithj')

  def test_wrong_file_type(self):
    with self.assertRaises(ci.CourseImportError):
      ci.parse_course_file(io.BytesIO(b'x'), 'courses.pdf')

  def test_missing_required_column(self):
    with self.assertRaisesRegex(ci.CourseImportError, 'Sequence'):
      ci.parse_course_file(csv_file([1, 'CSC', '226', 'smithj'], headers=['CRN', 'Subject', 'Course Number', 'Primary Instructor Username']), 'x.csv')

  def test_banner_export_without_usernames_is_rejected_with_clear_message(self):
    with open('courseMasterList.csv', 'rb') as f:
      with self.assertRaisesRegex(ci.CourseImportError, 'Username'):
        ci.parse_course_file(f, 'courseMasterList.csv')

  def test_empty_file_and_header_only(self):
    with self.assertRaises(ci.CourseImportError):
      ci.parse_course_file(io.BytesIO(b''), 'x.csv')
    with self.assertRaisesRegex(ci.CourseImportError, 'no courses'):
      ci.parse_course_file(csv_file(), 'x.csv')

  def test_three_instructors_are_read_from_a_real_file(self):
    with open('terms_csv/202113.csv', 'rb') as f:
      rows = ci.parse_course_file(f, '202113.csv')
    self.assertEqual(len(rows), 38)
    multi = [r for r in rows if r['instructors'][1]['username']]
    self.assertEqual(len(multi), 10)
    self.assertEqual(multi[0]['crosslist'], 'ANR 203S/GST 203S')

  def test_every_sample_file_parses(self):
    for name in ('Fall2018', 'Spring2017', 'Summer2018', '202113'):
      with open('terms_csv/{0}.csv'.format(name), 'rb') as f:
        self.assertGreater(len(ci.parse_course_file(f, name + '.csv')), 30, name)


class ValidateTests(unittest.TestCase):
  def run_validate(self, *rows, existing=()):
    parsed = ci.parse_course_file(csv_file(*rows), 'x.csv')
    return ci.validate_rows(parsed, PREFIXES, existing)

  def test_good_rows_are_ok(self):
    result = self.run_validate(course(1, 'CSC', '226', 'A'), course(2, 'MAT', '101', 'A'))
    self.assertEqual([r['status'] for r in result], [ci.OK, ci.OK])
    self.assertEqual(ci.summarize(result)['importable'], 2)

  def test_same_crn_twice_is_a_duplicate_pointing_to_the_first_row(self):
    result = self.run_validate(course(1, 'CSC', '226', 'A'), course(1, 'CSC', '226', 'A'))
    self.assertEqual(result[1]['status'], ci.DUPLICATE)
    self.assertIn('row 2', result[1]['reason'])

  def test_same_course_with_different_crns_are_separate_sections(self):
    result = self.run_validate(course(1, 'CSC', '226', 'A'), course(2, 'CSC', '226', 'A'))
    self.assertEqual([r['status'] for r in result], [ci.OK, ci.OK])

  def test_same_course_without_crns_is_a_duplicate(self):
    result = self.run_validate(course('', 'CSC', '226', 'A'), course('', 'CSC', '226', 'A'))
    self.assertEqual(result[1]['status'], ci.DUPLICATE)
    self.assertIn('row 2', result[1]['reason'])

  def test_duplicate_of_existing_course(self):
    result = self.run_validate(course(1, 'CSC', '226', 'A'), existing=[('CSC', '226', 'A')])
    self.assertEqual(result[0]['status'], ci.DUPLICATE)

  def test_unknown_prefix(self):
    result = self.run_validate(course(1, 'XYZ', '100', 'A'))
    self.assertEqual(result[0]['status'], ci.ERROR)
    self.assertIn('XYZ', result[0]['reason'])

  def test_missing_instructor_username(self):
    result = self.run_validate(course(1, 'CSC', '226', 'A', user=''))
    self.assertEqual((result[0]['status'], result[0]['reason']), (ci.ERROR, 'Missing values: Username'))
    self.assertEqual(result[0]['missing'], ['username'])

  def test_missing_primary_instructor_names_are_all_reported(self):
    result = self.run_validate([1, 'CSC', '226', 'A', 'T', '', '', '', ''])
    self.assertEqual(result[0]['reason'], 'Missing values: Instructor Last, Instructor First, Username')
    self.assertEqual(result[0]['listed'][0]['missing'], ['last', 'first', 'username'])

  def test_same_crn_on_a_different_course_is_a_duplicate(self):
    result = self.run_validate(course(21541, 'CSC', '236', 'A'), course(21541, 'CSC', '240', 'A'))
    self.assertEqual(result[1]['status'], ci.DUPLICATE)
    self.assertEqual(result[1]['reason'], 'CRN 21541 is already used by CSC 236 (row 2)')

  def test_blank_crn_is_not_a_duplicate(self):
    result = self.run_validate(course('', 'CSC', '236', 'A'), course('', 'CSC', '240', 'A'))
    self.assertEqual([r['status'] for r in result], [ci.OK, ci.OK])

  def test_listed_instructors_follow_the_preview_columns(self):
    result = self.run_validate(course(1, 'CSC', '226', 'A', l2='Doe', f2='Sam', u2='does'))
    self.assertEqual([i['username'] for i in result[0]['listed']], ['smithj', 'does'])
    self.assertEqual([i['username'] for i in result[0]['instructors']], ['smithj', 'does'])

  def test_missing_required_value(self):
    result = self.run_validate(course(1, 'CSC', '', 'A'))
    self.assertEqual(result[0]['status'], ci.ERROR)
    self.assertIn('Course Number', result[0]['reason'])

  def test_second_instructor_without_username_warns(self):
    result = self.run_validate(course(1, 'CSC', '226', 'A', l2='Doe', f2='Sam', u2=''))
    self.assertEqual(result[0]['status'], ci.OK)
    self.assertEqual(len(result[0]['warnings']), 1)

  def test_summary_counts(self):
    result = self.run_validate(course(1, 'CSC', '226', 'A'), course(1, 'CSC', '230', 'A'), course(3, 'XYZ', '1', 'A'))
    self.assertEqual(ci.summarize(result), {'total': 3, 'importable': 1, 'duplicates': 1, 'errors': 1, 'issues': 2})


if __name__ == '__main__':
  unittest.main()
