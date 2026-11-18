"""Regression checks for progressive ForgeQC related navigation."""
import unittest
from pathlib import Path

class RelatedNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (Path(__file__).parent / "ui_context_menu.py").read_text(encoding="utf-8")

    def test_breadcrumbs_and_links_are_installed_on_page_load(self):
        self.assertIn("installRelatedNavigation();", self.source)
        self.assertIn("aria-current", self.source)
        self.assertIn("related-actions", self.source)
        self.assertIn("main.insertBefore(section, main.firstChild)", self.source)

    def test_navigation_is_idempotent_and_uses_text_nodes(self):
        self.assertIn("document.getElementById('related-navigation')", self.source)
        self.assertIn("link.textContent = a.textContent", self.source)
        self.assertIn("current.textContent = labelForPath(path)", self.source)

    def test_native_text_context_menu_is_preserved(self):
        self.assertIn("window.getSelection()?.toString()", self.source)
        self.assertIn("input, textarea, select, [contenteditable], a, button", self.source)

    def test_quote_material_link_is_scoped_to_numeric_quote_ids(self):
        self.assertIn("quote-materials/", self.source)
        self.assertIn("encodeURIComponent(quoteId)", self.source)
        self.assertIn("startsWith('/quoting/')", self.source)

if __name__ == "__main__":
    unittest.main()
