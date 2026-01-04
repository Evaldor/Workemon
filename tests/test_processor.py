import unittest
from unittest.mock import patch
from app.processor import Processor

class TestProcessor(unittest.TestCase):
    @patch('app.llm_handler.LLMHandler.call_llm')
    @patch('app.database.SessionLocal')
    def test_process_api(self, mock_db, mock_llm):
        mock_llm.return_value = "Mock response"
        p = Processor()
        result = p.process('api', 'test content')
        self.assertEqual(result, "Mock response")
        mock_llm.assert_called_once()