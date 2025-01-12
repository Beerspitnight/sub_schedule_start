import unittest
from parsing_utils import parse_aesop_report_names

class TestParsingUtils(unittest.TestCase):
    def test_parse_aesop_report_names(self):
        # For a real test, you'd supply a sample docx or mock data
        # and check that the result is what you expect.
        result = parse_aesop_report_names("fake_docx_path.docx")
        self.assertIsNotNone(result)
        # self.assertIn("some_teachers_name", result)

if __name__ == '__main__':
    unittest.main()
