import unittest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.splitter import Splitter


class TestSplitter(unittest.TestCase):
    """Tests unitarios para Splitter"""
    
    def setUp(self):
        self.splitter = Splitter()
    
    @patch('app.utils.splitter.PyPDFLoader')
    def test_split_document(self, mock_loader):
        """Test: split_document divide correctamente PDFs en chunks con estructura válida"""
        # Arrange
        mock_doc = MagicMock()
        mock_doc.page_content = "Contenido de prueba. " * 100
        mock_doc.metadata = {'page': 1, 'source': 'test.pdf', 'author': 'Test Author'}
        
        mock_instance = MagicMock()
        mock_instance.load.return_value = [mock_doc]
        mock_loader.return_value = mock_instance
        
        # Act
        result = self.splitter.split_document("test.pdf")
        
        # Assert - Llamada correcta al loader
        mock_loader.assert_called_once_with("test.pdf")
        mock_instance.load.assert_called_once()
        
        # Assert - Estructura del resultado
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        
        # Assert - Estructura de cada chunk
        for chunk in result:
            self.assertIsInstance(chunk, dict)
            self.assertIn('text', chunk)
            self.assertIn('metadata', chunk)
            self.assertIsInstance(chunk['text'], str)
            self.assertIsInstance(chunk['metadata'], dict)
        
        # Assert - Preservación de metadatos
        first_chunk = result[0]
        self.assertEqual(first_chunk['metadata']['page'], 1)
        self.assertEqual(first_chunk['metadata']['source'], 'test.pdf')
        self.assertEqual(first_chunk['metadata']['author'], 'Test Author')
        
        # Assert - Caso edge: contenido vacío
        mock_doc_empty = MagicMock()
        mock_doc_empty.page_content = ""
        mock_doc_empty.metadata = {'page': 1}
        mock_instance.load.return_value = [mock_doc_empty]
        
        empty_result = self.splitter.split_document("empty.pdf")
        self.assertIsInstance(empty_result, list)


if __name__ == '__main__':
    unittest.main()
