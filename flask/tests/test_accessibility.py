"""Check accessible relationships in pages rendered by the real Flask app.

Keyboard focus, responsive menu state, table toggling, zoom, and motion still
need browser verification; these tests do not certify accessibility compliance.
"""

from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import app, captcha
from test_results_navigation import make_result


@dataclass
class Element:
    tag: str
    attrs: dict
    children: list = field(default_factory=list)

    def all(self, tag=None):
        for child in self.children:
            if isinstance(child, Element):
                if tag is None or child.tag == tag:
                    yield child
                yield from child.all(tag)

    def text(self):
        return " ".join("".join(
            child.text() if isinstance(child, Element) else child
            for child in self.children
        ).split())


class Page(HTMLParser):
    VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self, markup):
        super().__init__()
        self.root = Element("document", {})
        self.stack = [self.root]
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        element = Element(tag, dict(attrs))
        self.stack[-1].children.append(element)
        if tag not in self.VOID_TAGS:
            self.stack.append(element)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)

    def all(self, tag=None):
        return list(self.root.all(tag))

    def ids(self):
        return {element.attrs["id"]: element for element in self.all() if "id" in element.attrs}


class AccessibilityTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        with self.client.session_transaction() as session:
            session["last_result"] = make_result("A").toJSON()

    def page(self, route):
        response = self.client.get(route)
        self.assertEqual(response.status_code, 200)
        return Page(response.get_data(as_text=True))

    def test_shared_landmarks_and_keyboard_bypass(self):
        for route in ("/", "/analyzer", "/instructions", "/analyzer/results", "/privacy", "/terms"):
            with self.subTest(route=route):
                page = self.page(route)
                main = page.all("main")
                self.assertEqual(len(main), 1)
                self.assertEqual(main[0].attrs.get("id"), "main-content")
                self.assertEqual(main[0].attrs.get("tabindex"), "-1")
                first_link = page.all("a")[0]
                self.assertEqual(first_link.text(), "Skip to main content")
                self.assertEqual(first_link.attrs.get("href"), "#main-content")

                names = [nav.attrs.get("aria-label") for nav in page.all("nav")]
                self.assertTrue(all(names))
                self.assertEqual(len(names), len(set(names)))
                self.assertIn("hidden", page.ids()["GoToTopButton"].attrs)
                all_ids = [element.attrs["id"] for element in page.all() if "id" in element.attrs]
                self.assertEqual(len(all_ids), len(set(all_ids)))

    def test_link_accessible_names_include_visible_wording(self):
        for route in ("/", "/analyzer", "/instructions", "/analyzer/results"):
            with self.subTest(route=route):
                for link in self.page(route).all("a"):
                    visible_name = link.text()
                    accessible_name = link.attrs.get("aria-label")
                    if accessible_name and visible_name:
                        self.assertIn(visible_name.casefold(), accessible_name.casefold())

    def test_page_and_guide_heading_levels(self):
        for route, title in [("/", "Welcome to TDA Online"), ("/analyzer", "Tell me how it works!"),
                             ("/instructions", "How It Works!"), ("/analyzer/results", "Results")]:
            with self.subTest(route=route):
                headings = self.page(route).all("h1")
                self.assertEqual([heading.text() for heading in headings], [title])
        guide = self.page("/instructions")
        steps = [element for element in guide.all() if "GuideStepTitle" in element.attrs.get("class", "").split()]
        self.assertTrue(steps)
        self.assertTrue(all(element.tag == "h2" for element in steps))

    def test_analyzer_fields_have_associated_labels(self):
        page = self.page("/analyzer")
        labels = {label.attrs.get("for"): label.text() for label in page.all("label")}
        fields = page.all("input") + page.all("select")
        for element in fields:
            if element.attrs.get("type") not in ("hidden", "submit"):
                with self.subTest(field=element.attrs.get("name")):
                    self.assertTrue(labels.get(element.attrs.get("id")))
        self.assertEqual(labels["captcha"], "Please type the numbers above in the box below.")
        self.assertEqual(page.ids()["captcha"].attrs.get("name"), "captcha")
        self.assertNotIn("aria-label", page.ids()["captcha"].attrs)

    def test_enabled_captcha_keeps_one_labeled_challenge_and_answer(self):
        with patch.object(captcha, "enabled", True):
            page = self.page("/analyzer")
            images = [image for image in page.all("img") if image.attrs.get("src", "").startswith("data:image/png")]
            self.assertEqual(len(images), 1)
            self.assertEqual(images[0].attrs.get("alt"), "Numeric verification challenge")
            with self.client.session_transaction() as session:
                answer = session.get(captcha.session_key)
                self.assertTrue(answer.isdigit())
                self.assertEqual(len(answer), captcha.digits)

    def test_disabled_captcha_keeps_existing_behavior(self):
        with patch.object(captcha, "enabled", False):
            page = self.page("/analyzer")
            self.assertFalse(any(image.attrs.get("src", "").startswith("data:image/png")
                                 for image in page.all("img")))
            with self.client.session_transaction() as session:
                self.assertNotIn(captcha.session_key, session)

    def test_result_tables_and_graphs_have_named_relationships(self):
        page = self.page("/analyzer/results")
        ids = page.ids()
        for table in page.all("table"):
            name = ids[table.attrs["aria-labelledby"]]
            self.assertEqual(name.tag, "h2")
            self.assertTrue(name.text())
            self.assertEqual(len(list(table.all("colgroup"))), 1)
            for header in table.all("th"):
                self.assertIn(header.attrs.get("scope"), ("col", "colgroup"))
        regions = [element for element in page.all() if element.attrs.get("role") == "region"]
        self.assertEqual(len(regions), 3)
        for region in regions:
            self.assertEqual(region.attrs.get("tabindex"), "0")
            self.assertTrue(ids[region.attrs["aria-labelledby"]].text())
        plots = [image for image in page.all("img") if image.attrs.get("src", "").startswith("data:image/svg+xml")]
        self.assertEqual([plot.attrs.get("alt") for plot in plots], ["Persistence diagram", "Persistence barcode"])
        for plot in plots:
            self.assertEqual(plot.attrs.get("aria-describedby"), "raw-data-heading")

    def test_static_collapse_controls_identify_valid_targets_and_state(self):
        page = self.page("/analyzer/results")
        ids = page.ids()
        controls = [element for element in page.all("input") if element.attrs.get("id", "").startswith("Collapse")]
        self.assertEqual(len(controls), 3)
        names = []
        for control in controls:
            name = control.attrs["aria-label"]
            self.assertTrue(name.startswith(control.attrs["value"] + " "))
            names.append(name)
            self.assertEqual(control.attrs["aria-expanded"], "true")
            targets = control.attrs["aria-controls"].split()
            self.assertEqual(len(targets), 2)
            self.assertTrue(all(target in ids for target in targets))
        self.assertEqual(len(names), len(set(names)))


if __name__ == "__main__":
    unittest.main()
