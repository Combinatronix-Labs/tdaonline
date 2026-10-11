"""Design previews change presentation while preserving page text and controls."""

from html.parser import HTMLParser
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import app
from test_results_navigation import make_result


class PageContent(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.hidden = 0
        self.words = []
        self.controls = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag in ('head', 'script', 'style', 'svg'):
            self.hidden += 1
        attrs = dict(attrs)
        if tag in ('input', 'select', 'form', 'button'):
            self.controls.append((tag, attrs.get('name'), attrs.get('type'),
                                  attrs.get('action'), attrs.get('method'), attrs.get('target')))

    def handle_endtag(self, tag):
        if tag in ('head', 'script', 'style', 'svg'):
            self.hidden -= 1

    def handle_data(self, data):
        if not self.hidden:
            self.words.extend(data.split())


class DesignAttemptTests(unittest.TestCase):
    def setUp(self):
        previous = app.config['UI_DESIGN_ATTEMPT']
        self.addCleanup(app.config.__setitem__, 'UI_DESIGN_ATTEMPT', previous)
        self.client = app.test_client()
        with self.client.session_transaction() as session:
            session['last_result'] = make_result('A').toJSON()

    def test_designs_preserve_page_text_and_form_controls(self):
        for route in ('/', '/analyzer', '/instructions', '/analyzer/results', '/privacy', '/terms'):
            with self.subTest(route=route):
                app.config['UI_DESIGN_ATTEMPT'] = '1'
                original = self.client.get(route)
                self.assertEqual(original.status_code, 200)
                content = PageContent(original.get_data(as_text=True))
                for attempt in ('2', '3'):
                    with self.subTest(attempt=attempt):
                        app.config['UI_DESIGN_ATTEMPT'] = attempt
                        response = self.client.get(route)
                        self.assertEqual(response.status_code, 200)
                        html = response.get_data(as_text=True)
                        preview = PageContent(html)
                        self.assertEqual(preview.words, content.words)
                        self.assertEqual(preview.controls, content.controls)
                        self.assertIn(f'/static/css/design-{attempt}.css', html)
                        with self.client.get(f'/static/css/design-{attempt}.css') as stylesheet:
                            self.assertEqual(stylesheet.status_code, 200)

    def test_unknown_design_uses_attempt_one(self):
        app.config['UI_DESIGN_ATTEMPT'] = '1'
        original = self.client.get('/').get_data(as_text=True)
        for value in ('', '4', '../../privacy'):
            with self.subTest(value=value):
                app.config['UI_DESIGN_ATTEMPT'] = value
                response = self.client.get('/')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.get_data(as_text=True), original)


if __name__ == '__main__':
    unittest.main()
