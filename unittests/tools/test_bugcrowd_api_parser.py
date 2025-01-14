import datetime

from django.test import TestCase
from dojo.tools.bugcrowd_api.parser import BugcrowdApiParser
from dojo.models import Test


class TestBugcrowdApiParser(TestCase):
    def test_parse_file_with_no_vuln_has_no_findings(self):
        with open("unittests/scans/bugcrowd_api/bugcrowd_empty.json") as testfile:
            parser = BugcrowdApiParser()
            findings = parser.get_findings(testfile, Test())
            self.assertEqual(0, len(findings))

    def test_parse_file_with_one_vuln_has_one_findings(self):
        with open("unittests/scans/bugcrowd_api/bugcrowd_one.json") as testfile:

            #             description = """
            # Vulnerability Name: JWT alg none

            # Bugcrowd details:
            # - Severity: P5
            # - Bug Url: https://example.com/

            # Bugcrowd link: /submissions/a4201d47-62e1-4287-9ff6-30807ae9d36a"""
            parser = BugcrowdApiParser()
            findings = parser.get_findings(testfile, Test())
            self.assertEqual(1, len(findings))
            finding = findings[0]
            self.assertEqual(finding.title, "JWT Alg none")
            self.assertEqual(
                datetime.datetime.date(finding.date), datetime.date(2002, 4, 1)
            )
            self.assertEqual(str(finding.unsaved_endpoints[0]), "https://example.com")
            self.assertEqual(finding.severity, "Info")
            # self.assertEqual(finding.description, description)
            self.assertEqual(finding.mitigation, "Properly do JWT")
            self.assertEqual(finding.active, True)
            self.assertEqual(
                finding.unique_id_from_tool, "a4201d47-62e1-4287-9ff6-30807ae9d36a"
            )
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()

    def test_parse_file_with_multiple_vuln_has_multiple_finding(self):
        with open("unittests/scans/bugcrowd_api/bugcrowd_many.json") as testfile:
            parser = BugcrowdApiParser()
            findings = parser.get_findings(testfile, Test())
            self.assertEqual(3, len(findings))
            finding_1 = findings[0]
            finding_2 = findings[1]
            finding_3 = findings[2]

            self.assertEqual(finding_1.title, "Big bad problem")
            self.assertEqual(finding_2.title, "you did something wrong")
            self.assertEqual(finding_3.title, "you did something wrong (returned)")

            self.assertEqual(
                datetime.datetime.date(finding_1.date), datetime.date(2000, 1, 1)
            )
            self.assertEqual(
                datetime.datetime.date(finding_2.date), datetime.date(2000, 1, 2)
            )
            self.assertEqual(
                datetime.datetime.date(finding_3.date), datetime.date(2000, 1, 3)
            )

            self.assertEqual(
                str(finding_1.unsaved_endpoints[0]), "https://example.com/1"
            )
            self.assertEqual(
                str(finding_2.unsaved_endpoints[0]), "https://example.com/2"
            )
            self.assertEqual(
                str(finding_3.unsaved_endpoints[0]), "https://example.com/3"
            )
            for endpoint in finding_1.unsaved_endpoints:
                endpoint.clean()
            for endpoint in finding_2.unsaved_endpoints:
                endpoint.clean()
            for endpoint in finding_3.unsaved_endpoints:
                endpoint.clean()
            self.assertEqual(finding_1.severity, "Info")
            self.assertEqual(finding_2.severity, "Critical")
            self.assertEqual(finding_3.severity, "Medium")

            self.assertEqual(finding_1.mitigation, "Do things properly1")
            self.assertEqual(finding_2.mitigation, "Do things properly2")
            self.assertEqual(finding_3.mitigation, "Do things properly3")

            self.assertEqual(finding_1.active, False)
            self.assertEqual(finding_2.active, True)
            self.assertEqual(finding_3.active, True)

            self.assertEqual(finding_1.is_mitigated, True)
            self.assertEqual(finding_2.is_mitigated, False)
            self.assertEqual(finding_3.is_mitigated, False)

            self.assertEqual(
                finding_1.unique_id_from_tool, "3b0e6b2a-c21e-493e-bd19-de40f525016e"
            )
            self.assertEqual(
                finding_2.unique_id_from_tool, "b2f1066a-6188-4479-bab8-39cc5434f06f"
            )
            self.assertEqual(
                finding_3.unique_id_from_tool, "335a7ba5-57ba-485a-b40e-2f9aa4e19786"
            )
