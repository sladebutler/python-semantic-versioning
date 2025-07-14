import unittest
from pysemver import sanitize_branch

class TestSemVer(unittest.TestCase):
    def test_sanitize_branch(self):
        # Test sanitizing branch names
        self.assertEqual(sanitize_branch("feature/new-feature"), "feature.new-feature")
        self.assertEqual(sanitize_branch("bugfix/issue-123"), "bugfix.issue-123")
        self.assertEqual(sanitize_branch("release/v1.0.0"), "release.v1.0.0")
        self.assertEqual(sanitize_branch("hotfix/urgent_fix"), "hotfix.urgent_fix")

if __name__ == "__main__":
    unittest.main()
