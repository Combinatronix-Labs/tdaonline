"""Results navigation regression, using the application's real sessions.

Run from the repository root:
    python -m unittest discover -s flask/tests -v

``make_result`` provides results fixtures without invoking or changing the
analysis engine.
"""

import base64
from html.parser import HTMLParser
from pathlib import Path
import sys
import unittest
from urllib.parse import urljoin, urlsplit

import numpy


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import app
from models.result.successful import SuccessfulResult


def make_result(name):
    """Return two recognizable results with distinct tables and SVG graphs."""
    if name == "A":
        betti = [
            [0, 0.5, 0.75, 1.25, 1.5, 1.75, 2.5],
            [3, 3, 3, 2, 2, 2, 1],
            [0, 1, 2, 2, 1, 0, 0],
            [3, 2, 1, 0, 1, 2, 1],
        ]
        stats = [[3, 1.25, 2.5, 1.875, 1.875], [2, 1, 1, 1, 1], [1.5, 1.875]]
        raw = [
            numpy.array([[0, 1.25], [0, 2.5], [0, numpy.inf]]),
            numpy.array([[0.5, 1.5], [0.75, 1.75]]),
        ]
    elif name == "B":
        betti = [
            [0, 1, 2, 3, 4, 5, 6, 8],
            [4, 4, 4, 4, 3, 3, 2, 1],
            [0, 1, 2, 1, 1, 0, 0, 0],
            [4, 3, 2, 3, 2, 3, 2, 1],
        ]
        stats = [[4, 4, 8, 6, 6], [2, 2, 3, 2.5, 2.5], [2, 2.4]]
        raw = [
            numpy.array([[0, 4], [0, 6], [0, 8], [0, numpy.inf]]),
            numpy.array([[1, 3], [2, 5]]),
        ]
    else:
        raise ValueError("Unknown result fixture")

    def graph(kind):
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="160">'
            '<rect width="400" height="160" fill="#eaf2ed"/>'
            '<text x="24" y="80" font-size="28" fill="#17332f">'
            f"Result {name} {kind}</text></svg>"
        )
        return base64.b64encode(svg.encode()).decode()

    return SuccessfulResult(graph("diagram"), graph("barcode"), betti, stats, raw, [0, 1])


class ResultsPage(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.links = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a":
            self.links.append(attrs)


class ResultsNavigationTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def render_result(self, result):
        with self.client.session_transaction() as session:
            session["last_result"] = result.toJSON()
        response = self.client.get("/analyzer/results")
        self.assertEqual(response.status_code, 200)
        return ResultsPage(response.get_data(as_text=True))

    def test_results_navigation_resolves_to_existing_top_level_routes(self):
        page = self.render_result(make_result("B"))
        expected = {
            "Try it: TDA Online Analyzer": "/analyzer",
            "(how it works): TDA Online instructions": "/instructions",
            "Privacy Policy: TDA Online": "/privacy",
            "Terms of Service: TDA Online": "/terms",
        }
        links = {link.get("aria-label"): link.get("href") for link in page.links}
        for label, destination in expected.items():
            with self.subTest(label=label):
                self.assertEqual(links[label], destination)
                resolved = urlsplit(urljoin("https://tda.example/analyzer/results", links[label])).path
                self.assertEqual(resolved, destination)
                app.url_map.bind("tda.example").match(resolved, method="GET")

        for destination in set(expected.values()):
            with self.subTest(destination=destination):
                self.assertEqual(self.client.get(destination).status_code, 200)


if __name__ == "__main__":
    unittest.main()
