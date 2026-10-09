"""Deployment-owned legal documents stay outside the template repository."""

from pathlib import Path
import sys
import tempfile
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import app


class LegalContentTests(unittest.TestCase):
    def setUp(self):
        self.original_directory = app.config['LEGAL_CONTENT_DIR']
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.addCleanup(app.config.__setitem__, 'LEGAL_CONTENT_DIR', self.original_directory)
        app.config['LEGAL_CONTENT_DIR'] = self.directory.name
        self.client = app.test_client()

    def test_configured_documents_render_as_html_without_executing_jinja(self):
        for document, title in [('privacy', 'Privacy Notice'), ('terms', 'Terms & Conditions')]:
            with self.subTest(document=document):
                content = '<h1>Operator document</h1><p>{{ 6 * 7 }}</p><a href="#section">Section</a>'
                Path(self.directory.name, document + '.html').write_text(content, encoding='utf-8')

                response = self.client.get('/' + document)
                html = response.get_data(as_text=True)
                self.assertEqual(response.status_code, 200)
                self.assertIn(content, html)
                self.assertIn(title.replace('&', '&amp;'), html)
                self.assertNotIn('This document is currently unavailable.', html)

    def test_missing_documents_keep_pages_and_navigation_available(self):
        for document in ['privacy', 'terms']:
            with self.subTest(document=document):
                response = self.client.get('/' + document)
                html = response.get_data(as_text=True)
                self.assertEqual(response.status_code, 200)
                self.assertIn('This document is currently unavailable.', html)
                self.assertIn('href="/analyzer"', html)

    def test_file_edits_appear_on_the_next_request(self):
        document = Path(self.directory.name, 'privacy.html')
        document.write_text('<h1>First document</h1>', encoding='utf-8')
        self.assertIn('First document', self.client.get('/privacy').get_data(as_text=True))
        document.write_text('<h1>Updated document</h1>', encoding='utf-8')
        response = self.client.get('/privacy').get_data(as_text=True)
        self.assertIn('Updated document', response)
        self.assertNotIn('First document', response)


if __name__ == '__main__':
    unittest.main()
