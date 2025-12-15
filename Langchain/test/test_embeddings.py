import unittest
import sys
import os
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.embbedings import EmbeddingGenerator


class TestEmbeddingGenerator(unittest.TestCase):
    """Tests unitarios para EmbeddingGenerator"""
    
    @patch('app.utils.embbedings.GoogleGenerativeAIEmbeddings')
    def setUp(self, mock_embeddings):
        self.mock_embeddings_instance = MagicMock()
        mock_embeddings.return_value = self.mock_embeddings_instance
        self.embedding_generator = EmbeddingGenerator()
    
    def test_get_document_embedding(self):
        """Test: get_document_embedding genera embeddings correctos para documentos"""
        # Arrange
        expected_embeddings = [[0.1] * 3072, [0.2] * 3072]
        self.mock_embeddings_instance.aembed_documents = AsyncMock(return_value=expected_embeddings)
        texts = ["Texto de prueba 1", "Texto de prueba 2"]
        
        # Act
        result = asyncio.run(self.embedding_generator.get_document_embedding(texts))
        
        # Assert - Llamada correcta al método
        self.mock_embeddings_instance.aembed_documents.assert_called_once_with(
            texts=texts,
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=3072
        )
        
        # Assert - Formato y estructura del resultado
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(len(result[0]), 3072)
        self.assertEqual(len(result[1]), 3072)
        self.assertEqual(result, expected_embeddings)
    
    def test_get_query_embedding(self):
        """Test: get_query_embedding genera embedding correcto para consultas"""
        # Arrange
        expected_embedding = [0.5] * 3072
        self.mock_embeddings_instance.aembed_query = AsyncMock(return_value=expected_embedding)
        text = "¿Qué es Python?"
        
        # Act
        result = asyncio.run(self.embedding_generator.get_query_embedding(text))
        
        # Assert - Llamada correcta al método
        self.mock_embeddings_instance.aembed_query.assert_called_once_with(
            text=text,
            task_type="SEMANTIC_SIMILARITY",
            output_dimensionality=3072
        )
        
        # Assert - Formato y estructura del resultado
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3072)
        self.assertEqual(result, expected_embedding)
    
    def test_format_database(self):
        """Test: format_database formatea correctamente chunks y vectores con todos los tipos y formatos"""
        # Arrange
        text_chunks = [
            {'text': 'Chunk 1', 'metadata': {'page': 1, 'source': 'test.pdf'}},
            {'text': 'Chunk 2', 'metadata': {'page': 2, 'author': 'Test'}}
        ]
        vector_chunks = [[0.1] * 3072, [0.2] * 3072]
        
        # Act
        result = self.embedding_generator.format_database(text_chunks, vector_chunks)
        
        # Assert - Estructura y tipos
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        
        # Assert - Primer elemento completo
        self.assertIn('text_chunk', result[0])
        self.assertIn('metadata', result[0])
        self.assertIn('vector_chunk', result[0])
        self.assertEqual(result[0]['text_chunk'], 'Chunk 1')
        self.assertIsInstance(result[0]['metadata'], dict)
        self.assertEqual(result[0]['metadata']['page'], 1)
        self.assertEqual(result[0]['metadata']['source'], 'test.pdf')
        self.assertIsInstance(result[0]['vector_chunk'], list)
        self.assertEqual(len(result[0]['vector_chunk']), 3072)
        
        # Assert - Segundo elemento
        self.assertEqual(result[1]['text_chunk'], 'Chunk 2')
        self.assertEqual(result[1]['metadata']['page'], 2)
        
        # Assert - Caso edge: listas vacías
        empty_result = self.embedding_generator.format_database([], [])
        self.assertEqual(empty_result, [])


if __name__ == '__main__':
    unittest.main()
