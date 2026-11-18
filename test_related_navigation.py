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
        self.assertIn("encodeURIComponent(quoteMatch[1])", self.source)
        self.assertIn("const quoteMatch = /^([0-9]+)$/.exec", self.source)
        self.assertIn("path.split('/').filter(Boolean).length === 2", self.source)
        self.assertIn("startsWith('/quoting/')", self.source)

    def test_all_related_navigation_targets_have_actual_menu_links(self):
        import re
        menu = self.source.split('CONTEXT_HTML = r"""', 1)[1].split('<script>', 1)[0]
        targets = set(re.findall(r'href="(/[^"]*)"', menu))
        self.assertIn('/rma', targets)
        self.assertIn('/clocking', targets)
        related = self.source.split('function setRelated(path)', 1)[1].split('function decorate()', 1)[0]
        for target in ('/rma', '/clocking'):
            self.assertIn(target, related)
            self.assertIn(target, targets)

if __name__ == "__main__":
    unittest.main()
