import unittest
from unittest.mock import patch, MagicMock
import azure.functions as func
import json
from function_app import consultarHistorial

class TestConsultarHistorial(unittest.TestCase):

    @patch('function_app.CosmosClient')
    @patch('os.environ.get')
    def test_consultar_historial_success(self, mock_env_get, mock_cosmos_client):
        # Configurar mocks
        mock_env_get.return_value = "AccountEndpoint=https://test.documents.azure.com:443/;AccountKey=test;"
        
        mock_container = MagicMock()
        mock_database = MagicMock()
        mock_client_instance = MagicMock()
        
        mock_cosmos_client.from_connection_string.return_value = mock_client_instance
        mock_client_instance.get_database_client.return_value = mock_database
        mock_database.get_container_client.return_value = mock_container

        # Simular respuesta de la query
        mock_items = [
            {"id": "1", "clienteId": "12345", "estado": "pendiente"},
            {"id": "2", "clienteId": "12345", "estado": "en camino"}
        ]
        mock_container.query_items.return_value = iter(mock_items)

        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/pedidos',
            params={'clienteId': '12345'}
        )

        # Ejecutar función
        resp = consultarHistorial(req)

        # Verificaciones
        self.assertEqual(resp.status_code, 200)
        resp_json = json.loads(resp.get_body())
        self.assertEqual(len(resp_json), 2)
        self.assertEqual(resp_json[0]["id"], "1")

    def test_consultar_historial_missing_clienteId(self):
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/pedidos',
            params={}
        )

        # Ejecutar función
        resp = consultarHistorial(req)

        # Verificaciones
        self.assertEqual(resp.status_code, 400)
        resp_json = json.loads(resp.get_body())
        self.assertTrue("error" in resp_json)

if __name__ == '__main__':
    unittest.main()
