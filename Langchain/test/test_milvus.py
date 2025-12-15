import unittest
import sys
import os
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.milvus import upload_document, get_document, create_milvus_collection

##Para correr los test de milvus se necesita tener la bsdd de datos de milvus corriendo localmente
class TestMilvusOperations(unittest.TestCase):
    """Tests unitarios para operaciones de Milvus"""
    
    @patch('app.db.milvus.async_client')
    def test_upload_document(self, mock_async_client):
        """Test: upload_document inserta documentos correctamente en Milvus"""
        # Arrange
        mock_async_client.insert = AsyncMock(return_value={'insert_count': 2})
        test_data = [
            {'text_chunk': 'Texto 1', 'metadata': {'page': 1}, 'vector_chunk': [0.1] * 3072},
            {'text_chunk': 'Texto 2', 'metadata': {'page': 2}, 'vector_chunk': [0.2] * 3072}
        ]
        
        # Act
        asyncio.run(upload_document(data=test_data, collection_name='test_collection'))
        
        # Assert - Llamada correcta al método insert
        mock_async_client.insert.assert_called_once_with(
            collection_name='test_collection',
            data=test_data
        )
        
        # Assert - Caso edge: datos vacíos
        mock_async_client.reset_mock()
        mock_async_client.insert = AsyncMock(return_value={'insert_count': 0})
        asyncio.run(upload_document(data=[], collection_name='test_collection'))
        mock_async_client.insert.assert_called_once_with(
            collection_name='test_collection',
            data=[]
        )
    
    @patch('app.db.milvus.async_client')
    def test_get_document(self, mock_async_client):
        """Test: get_document busca y retorna documentos correctamente"""
        # Arrange
        mock_hit1 = MagicMock()
        mock_hit2 = MagicMock()
        mock_async_client.search = AsyncMock(return_value=[[mock_hit1, mock_hit2]])
        query_vector = [0.5] * 3072
        filter_expr = "metadata['page'] > 5"
        
        # Act
        result = asyncio.run(get_document(
            query_vector=query_vector,
            collection_name='test_collection',
            filter=filter_expr
        ))
        
        # Assert - Llamada correcta al método search
        mock_async_client.search.assert_called_once_with(
            collection_name='test_collection',
            anns_field='vector_chunk',
            data=[query_vector],
            limit=5,
            search_params={'metric_type': 'COSINE'},
            filter=filter_expr,
            output_fields=['text_chunk']
        )
        
        # Assert - Formato y estructura del resultado
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        
        # Assert - Caso edge: sin resultados
        mock_async_client.reset_mock()
        mock_async_client.search = AsyncMock(return_value=[[]])
        empty_result = asyncio.run(get_document(
            query_vector=query_vector,
            collection_name='test_collection',
            filter=''
        ))
        self.assertEqual(empty_result, [])
    
    @patch('app.db.milvus.client_db')
    def test_create_milvus_collection(self, mock_client_db):
        """Test: create_milvus_collection maneja creación y existencia de colecciones"""
        # Arrange - Colección no existe
        mock_client_db.list_collections.return_value = []
        mock_client_db.create_collection = MagicMock()
        mock_client_db.get_load_state = MagicMock(return_value={'state': 'Loaded'})
        
        # Act
        create_milvus_collection('new_collection')
        
        # Assert - Crea colección nueva
        mock_client_db.list_collections.assert_called()
        mock_client_db.create_collection.assert_called_once()
        
        # Arrange - Colección ya existe
        mock_client_db.reset_mock()
        mock_client_db.list_collections.return_value = ['existing_collection']
        mock_client_db.create_collection = MagicMock()
        
        # Act
        result = create_milvus_collection('existing_collection')
        
        # Assert - No crea colección existente y retorna None
        self.assertIsNone(result)
        mock_client_db.create_collection.assert_not_called()


if __name__ == '__main__':
    unittest.main()
