import io
import unittest

from openpyxl import Workbook

from app.logic import courseImport as ci

HEADERS = ['CRN', 'Subject', 'Course Number', 'Sequence', 'Title', 'CrossList Courses',
           'Primary Instructor Last Name', 'Primary Instructor First Name', 'Primary Instructor Username',
           'Instructor2 Last Name', 'Instructor2 First Name', 'Instructor2 Username']
PREFIXES = {'CSC': 1, 'MAT': 2}


def csvFile(*rows, headers=HEADERS):
  lines = [",".join(headers)] + [",".join(str(c) for c in r) for r in rows]
  return io.BytesIO("\n".join(lines).encode('utf-8'))


def course(crn, prefix, number, section, user='smithj', **extra):
  return [crn, prefix, number, section, 'A Title', '', 'Smith', 'Jo', user, '', '', ''] if not extra else \
         [crn, prefix, number, section, 'A Title', '', 'Smith', 'Jo', user, extra.get('l2', ''), extra.get('f2', ''), extra.get('u2', '')]


class ParseTests(unittest.TestCase):
  def testCsvRowsParseWithSpreadsheetRowNumbers(self):
    rows = ci.parseCourseFile(csvFile(course(1, 'csc', '226', 'a'), course(2, 'MAT', '101', 'B')), 'x.csv')
    self.assertEqual([r['row'] for r in rows], [2, 3])
    self.assertEqual((rows[0]['prefix'], rows[0]['number'], rows[0]['section']), ('CSC', '226', 'A'))
    self.assertEqual(rows[0]['instructors'][0]['username'], 'smithj')

  def testBlankRowsAreDropped(self):
    rows = ci.parseCourseFile(csvFile(course(1, 'CSC', '226', 'A'), ['', '', ''], course(2, 'CSC', '230', 'A')), 'x.csv')
    self.assertEqual(len(rows), 2)
    self.assertEqual(rows[1]['row'], 4)

  def testXlsxNumbersDoNotBecomeFloats(self):
    wb = Workbook()
    ws = wb.active
    ws.append(HEADERS)
    ws.append([21540, 'CSC', 226, 'A', 'Software Engineering', None, 'N', 'A', 'nyabutoa', None, None, None])
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    row = ci.parseCourseFile(buf, 'courses.xlsx')[0]
    self.assertEqual((row['crn'], row['number']), ('21540', '226'))

  def testAlternateHeaderLayouts(self):
    for headers in (['CRN_KEY', 'SUBJ_CODE', 'CRSE_NUMBER', 'SEQ_NUMBER_KEY', 'TITLE', 'PRIMARY_INSTRUCTOR_USERNAME'],
                    ['crn', 'subject', 'course number', 'sequence', 'title', 'primary instructor username']):
      rows = ci.parseCourseFile(csvFile([1, 'CSC', '226', 'A', 'T', 'smithj'], headers=headers), 'x.csv')
      self.assertEqual(rows[0]['instructors'][0]['username'], 'smithj')

  def testWrongFileType(self):
    with self.assertRaises(ci.CourseImportError):
      ci.parseCourseFile(io.BytesIO(b'x'), 'courses.pdf')

  def testMissingRequiredColumn(self):
    with self.assertRaisesRegex(ci.CourseImportError, 'Sequence'):
      ci.parseCourseFile(csvFile([1, 'CSC', '226', 'smithj'], headers=['CRN', 'Subject', 'Course Number', 'Primary Instructor Username']), 'x.csv')

  def testBannerExportWithoutUsernamesIsRejectedWithClearMessage(self):
    with open('courseMasterList.csv', 'rb') as f:
      with self.assertRaisesRegex(ci.CourseImportError, 'Username'):
        ci.parseCourseFile(f, 'courseMasterList.csv')

  def testEmptyFileAndHeaderOnly(self):
    with self.assertRaises(ci.CourseImportError):
      ci.parseCourseFile(io.BytesIO(b''), 'x.csv')
    with self.assertRaisesRegex(ci.CourseImportError, 'no courses'):
      ci.parseCourseFile(csvFile(), 'x.csv')

  def testThreeInstructorsAreReadFromARealFile(self):
    with open('terms_csv/202113.csv', 'rb') as f:
      rows = ci.parseCourseFile(f, '202113.csv')
    self.assertEqual(len(rows), 38)
    multi = [r for r in rows if r['instructors'][1]['username']]
    self.assertEqual(len(multi), 10)
    self.assertEqual(multi[0]['crosslist'], 'ANR 203S/GST 203S')

  def testEverySampleFileParses(self):
    for name in ('Fall2018', 'Spring2017', 'Summer2018', '202113'):
      with open('terms_csv/{0}.csv'.format(name), 'rb') as f:
        self.assertGreater(len(ci.parseCourseFile(f, name + '.csv')), 30, name)


class ValidateTests(unittest.TestCase):
  def runValidate(self, *rows, existing=()):
    parsed = ci.parseCourseFile(csvFile(*rows), 'x.csv')
    return ci.validateRows(parsed, PREFIXES, existing)

  def testGoodRowsAreOk(self):
    result = self.runValidate(course(1, 'CSC', '226', 'A'), course(2, 'MAT', '101', 'A'))
    self.assertEqual([r['status'] for r in result], [ci.OK, ci.OK])
    self.assertEqual(ci.summarize(result)['importable'], 2)

  def testSameCrnTwiceIsADuplicatePointingToTheFirstRow(self):
    result = self.runValidate(course(1, 'CSC', '226', 'A'), course(1, 'CSC', '226', 'A'))
    self.assertEqual(result[1]['status'], ci.DUPLICATE)
    self.assertIn('row 2', result[1]['reason'])

  def testSameCourseWithDifferentCrnsAreSeparateSections(self):
    result = self.runValidate(course(1, 'CSC', '226', 'A'), course(2, 'CSC', '226', 'A'))
    self.assertEqual([r['status'] for r in result], [ci.OK, ci.OK])

  def testSameCourseWithoutCrnsIsADuplicate(self):
    result = self.runValidate(course('', 'CSC', '226', 'A'), course('', 'CSC', '226', 'A'))
    self.assertEqual(result[1]['status'], ci.DUPLICATE)
    self.assertIn('row 2', result[1]['reason'])

  def testDuplicateOfExistingCourse(self):
    result = self.runValidate(course(1, 'CSC', '226', 'A'), existing=[('CSC', '226', 'A')])
    self.assertEqual(result[0]['status'], ci.DUPLICATE)

  def testUnknownPrefix(self):
    result = self.runValidate(course(1, 'XYZ', '100', 'A'))
    self.assertEqual(result[0]['status'], ci.ERROR)
    self.assertIn('XYZ', result[0]['reason'])

  def testMissingInstructorUsername(self):
    result = self.runValidate(course(1, 'CSC', '226', 'A', user=''))
    self.assertEqual((result[0]['status'], result[0]['reason']), (ci.ERROR, 'Missing values: Username'))
    self.assertEqual(result[0]['missing'], ['username'])

  def testMissingPrimaryInstructorNamesAreAllReported(self):
    result = self.runValidate([1, 'CSC', '226', 'A', 'T', '', '', '', ''])
    self.assertEqual(result[0]['reason'], 'Missing values: Instructor Last, Instructor First, Username')
    self.assertEqual(result[0]['listed'][0]['missing'], ['last', 'first', 'username'])

  def testSameCrnOnADifferentCourseIsADuplicate(self):
    result = self.runValidate(course(21541, 'CSC', '236', 'A'), course(21541, 'CSC', '240', 'A'))
    self.assertEqual(result[1]['status'], ci.DUPLICATE)
    self.assertEqual(result[1]['reason'], 'CRN 21541 is already used by CSC 236 (row 2)')

  def testBlankCrnIsNotADuplicate(self):
    result = self.runValidate(course('', 'CSC', '236', 'A'), course('', 'CSC', '240', 'A'))
    self.assertEqual([r['status'] for r in result], [ci.OK, ci.OK])

  def testListedInstructorsFollowThePreviewColumns(self):
    result = self.runValidate(course(1, 'CSC', '226', 'A', l2='Doe', f2='Sam', u2='does'))
    self.assertEqual([i['username'] for i in result[0]['listed']], ['smithj', 'does'])
    self.assertEqual([i['username'] for i in result[0]['instructors']], ['smithj', 'does'])

  def testMissingRequiredValue(self):
    result = self.runValidate(course(1, 'CSC', '', 'A'))
    self.assertEqual(result[0]['status'], ci.ERROR)
    self.assertIn('Course Number', result[0]['reason'])

  def testSecondInstructorWithoutUsernameWarns(self):
    result = self.runValidate(course(1, 'CSC', '226', 'A', l2='Doe', f2='Sam', u2=''))
    self.assertEqual(result[0]['status'], ci.OK)
    self.assertEqual(len(result[0]['warnings']), 1)

  def testSummaryCounts(self):
    result = self.runValidate(course(1, 'CSC', '226', 'A'), course(1, 'CSC', '230', 'A'), course(3, 'XYZ', '1', 'A'))
    self.assertEqual(ci.summarize(result), {'total': 3, 'importable': 1, 'duplicates': 1, 'errors': 1, 'issues': 2})


if __name__ == '__main__':
  unittest.main()
