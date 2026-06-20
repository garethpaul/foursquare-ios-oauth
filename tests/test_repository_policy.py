import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "check.yml"
MAKEFILE = ROOT / "Makefile"
README = ROOT / "README.md"
APP_DELEGATE = ROOT / "FSExampleOAuth" / "FSExampleOAuth" / "FSAppDelegate.m"


class RepositoryPolicyTests(unittest.TestCase):
    def test_obsolete_travis_configuration_is_removed(self):
        self.assertFalse((ROOT / ".travis.yml").exists())

    def test_workflow_is_pinned_read_only_and_provider_free(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("permissions:\n  contents: read", workflow)
        self.assertIn("runs-on: macos-15", workflow)
        self.assertRegex(
            workflow,
            r"actions/checkout@[0-9a-f]{40}\s+# v7\.0\.0",
        )
        self.assertIn("persist-credentials: false", workflow)
        self.assertIn("run: make check", workflow)

        for forbidden in (
            "pull_request_target",
            "self-hosted",
            "${{ secrets.",
            "curl ",
            "wget ",
            "foursquare.com",
            "api.foursquare.com",
        ):
            self.assertNotIn(forbidden, workflow)

    def test_make_check_is_unsigned_isolated_and_static(self):
        makefile = MAKEFILE.read_text(encoding="utf-8")

        self.assertIn("python3 -m unittest discover -s tests -v", makefile)
        self.assertIn("xcodebuild analyze", makefile)
        self.assertIn("xcodebuild build", makefile)
        self.assertIn("CODE_SIGNING_ALLOWED=NO", makefile)
        self.assertIn("CODE_SIGNING_REQUIRED=NO", makefile)
        self.assertIn("IPHONEOS_DEPLOYMENT_TARGET=12.0", makefile)
        self.assertIn("PRODUCT_BUNDLE_IDENTIFIER=com.foursquare.FSExampleOAuth", makefile)
        self.assertIn('-destination "generic/platform=iOS Simulator"', makefile)
        self.assertIn("-derivedDataPath \"$(DERIVED_DATA)\"", makefile)
        self.assertNotRegex(makefile, re.compile(r"\b(curl|wget)\b"))

    def test_shared_scheme_is_committed(self):
        scheme = (
            ROOT
            / "FSExampleOAuth"
            / "FSExampleOAuth.xcodeproj"
            / "xcshareddata"
            / "xcschemes"
            / "FSExampleOAuth.xcscheme"
        )
        self.assertTrue(scheme.is_file())

    def test_legacy_oauth_risks_are_prominent(self):
        readme = README.read_text(encoding="utf-8")

        for warning in (
            "legacy sample",
            "Do not use it for a new production integration",
            "client secret",
            "PKCE",
            "state parameter",
            "never contacts Foursquare",
        ):
            self.assertIn(warning, readme)

    def test_universal_link_callback_matches_the_current_delegate_contract(self):
        app_delegate = APP_DELEGATE.read_text(encoding="utf-8")

        self.assertIn(
            "NSArray<id<UIUserActivityRestoring>> * _Nullable restorableObjects",
            app_delegate,
        )


if __name__ == "__main__":
    unittest.main()
