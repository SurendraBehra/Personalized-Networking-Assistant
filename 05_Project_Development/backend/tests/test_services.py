import unittest
from unittest.mock import patch, MagicMock
from backend.services.theme_extractor import ThemeExtractor
from backend.services.text_generator import TextGenerator
from backend.services.fact_verifier import FactVerifier

class TestServices(unittest.TestCase):
    def test_theme_extractor_fallback(self):
        """
        Test that theme extractor fallback successfully extracts themes from event description and interests.
        """
        event_desc = "AI for Sustainable Cities. Building green grids."
        interests = "climate change, machine learning"
        
        themes = ThemeExtractor.extract_fallback(event_desc, interests)
        
        self.assertIsInstance(themes, list)
        self.assertTrue(len(themes) > 0)
        # Check that extracted themes are capitalized (title case)
        for t in themes:
            self.assertEqual(t, t.title())
            
    def test_text_generator_fallback(self):
        """
        Test that text generator fallback builds starters based on themes.
        """
        themes = ["AI Ethics", "Urban Planning"]
        starters = TextGenerator.generate_fallback(themes, "Event", "Interests")
        
        self.assertIsInstance(starters, list)
        self.assertEqual(len(starters), 3)
        for s in starters:
            self.assertIsInstance(s, str)
            self.assertTrue(len(s) > 10)
            
    @patch('requests.get')
    def test_fact_verifier_success(self, mock_get):
        """
        Test that fact verifier successfully processes Wikipedia searches and page summary retrieval.
        """
        # Mock search response
        mock_search_res = MagicMock()
        mock_search_res.status_code = 200
        mock_search_res.json.return_ok = True
        mock_search_res.json.return_value = {
            "query": {
                "search": [
                    {"title": "Blockchain in healthcare"}
                ]
            }
        }
        
        # Mock REST summary response
        mock_summary_res = MagicMock()
        mock_summary_res.status_code = 200
        mock_summary_res.json.return_value = {
            "title": "Blockchain in healthcare",
            "extract": "Blockchain technology is increasingly applied in healthcare to secure electronic medical records.",
            "content_urls": {
                "desktop": {
                    "page": "https://en.wikipedia.org/wiki/Blockchain_in_healthcare"
                }
            }
        }
        
        # Configure requests.get to return search mock first, and summary mock second
        mock_get.side_effect = [mock_search_res, mock_summary_res]
        
        result = FactVerifier.verify_fact("blockchain healthcare")
        
        self.assertTrue(result["found"])
        self.assertEqual(result["topic"], "Blockchain in healthcare")
        self.assertIn("secure electronic medical records", result["summary"])
        self.assertEqual(result["source_url"], "https://en.wikipedia.org/wiki/Blockchain_in_healthcare")

    @patch('requests.get')
    def test_fact_verifier_not_found(self, mock_get):
        """
        Test fact verifier when no matching articles are found on Wikipedia.
        """
        mock_search_res = MagicMock()
        mock_search_res.status_code = 200
        mock_search_res.json.return_value = {
            "query": {
                "search": []
            }
        }
        mock_get.return_value = mock_search_res
        
        result = FactVerifier.verify_fact("nonexistenttopic12345")
        
        self.assertFalse(result["found"])
        self.assertIn("Could not find any Wikipedia articles", result["summary"])
        self.assertIsNone(result["source_url"])

if __name__ == '__main__':
    unittest.main()
