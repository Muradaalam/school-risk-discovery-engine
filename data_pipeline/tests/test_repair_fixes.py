
import unittest

from data_pipeline.extraction.repair_rows import get_row_groups, parse_school_row
from data_pipeline.quality.repair_audit import page_rows


PAGE = {
    "page_number": 2,
    "pdf_sha256": "testhash",
    "source_url": "https://example.org/pdf"
}


class TestRepairCorrections(unittest.TestCase):

    def test_known_categories(self):
        prefix = "12     AJMER     PUSHKAR     AJMER RURAL     GPS SCHOOL"

        for raw, expected in [("GPS", "PS"), ("GUPS", "UPS"), ("GSSS", "SSS")]:
            line = f"{prefix}     8210304401     {raw}     24     2     4.00"
            row = parse_school_row([line], PAGE)

            self.assertEqual(row["school_type"], expected)
            self.assertEqual(row["school_type_raw"], raw)

    def test_extra_name_spacing(self):
        line = "275     AJMER     KISHANGARH     ARAIN     GUPS JAKHDO KI DHANI  KATSURA     8210212702     UPS     47     1     5.00"

        row = parse_school_row([line], PAGE)

        self.assertEqual(row["school_name"], "GUPS JAKHDO KI DHANI KATSURA")
        self.assertEqual(row["parse_note"], "JOINED_SCHOOL_NAME_SEGMENTS")

    def test_wrapped_constituency(self):
        lines = [
            "148     AJMER     AJMER",
            "SOUTH     AJMER URBAN     MGGS TRAMBE AJMER     8211500601     SSS     78     11     10.79"
        ]

        row = parse_school_row(lines, PAGE)

        self.assertEqual(row["constituency"], "AJMER SOUTH")
        self.assertEqual(row["school_name"], "MGGS TRAMBE AJMER")

    def test_wrapped_school_name(self):
        lines = [
            "111     SHAHID DEEPENDRA SINGH RATHORE GOVT. SENIOR SECONDARY     8210404901     SSS     179     11     15.00",
            "        AJMER     PUSHKAR     AJMER RURAL     SCHOOL LESWA (214319)"
        ]

        row = parse_school_row(lines, PAGE)

        self.assertTrue(row["school_name"].endswith("SCHOOL LESWA (214319)"))

    def test_unknown_category_stays_in_review(self):
        line = "12     AJMER     PUSHKAR     AJMER RURAL     SCHOOL     8210304401     SR     24     2     4.00"

        with self.assertRaisesRegex(ValueError, "Unexpected school category"):
            parse_school_row([line], PAGE)

    def test_long_number_not_serial(self):
        text = (
            "8211503001     SSS     250     5     10.00\n"
            "702704     UPS     7     1     2.00\n"
            "12     AJMER     SCHOOL"
        )

        self.assertEqual(page_rows(text), [12])
        self.assertEqual(len(list(get_row_groups(text))), 1)

    def test_missing_school_name_rejected(self):
        line = "162     AJMER     AJMER NORTH     AJMER URBAN     8211502609     SSS     823     15     8.00"

        with self.assertRaises(ValueError):
            parse_school_row([line], PAGE)

    def test_written_out_categories(self):
        for category, expected in [
            ("PRIMARY", "PS"),
            ("PRIMERY", "PS"),
            ("UPPER PRIMARY", "UPS"),
            ("UPPER PRIMERY", "UPS")
        ]:
            line = f"12     AJMER     PUSHKAR     AJMER RURAL     GOVT SCHOOL     8210304401     {category}     24     2     4.00"
            row = parse_school_row([line], PAGE)

            self.assertEqual(row["school_type"], expected)


    def test_wrapped_constituency_with_split_school_name(self):
        lines = [
            "157     AJMER                   AJMER",
            "SOUTH           AJMER URBAN          GSSS DIGGI LOCAL  AJMER                                                      8211501705              SSS              350              6               25.00"
        ]

        row = parse_school_row(lines, PAGE)

        self.assertEqual(row["constituency"], "AJMER SOUTH")
        self.assertEqual(row["school_name"], "GSSS DIGGI LOCAL AJMER")
        self.assertEqual(row["enrollment"], 350)

if __name__ == "__main__":
    unittest.main()
