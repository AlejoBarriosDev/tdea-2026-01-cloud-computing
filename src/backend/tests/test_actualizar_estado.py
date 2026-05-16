import unittest
from unittest.mock import patch, MagicMock
import azure.functions as func
import json
from function_app import actualizarEstado

class TestActualizarEstado(unittest.TestCase):

    @patch('function_app.CosmosClient')
    @patch('os.environ.get')
    def test_actualizar_estado_success(self, mock_env_get, mock_cosmos_client):
        # Configurar mocks
        mock_env_get.return_value = "AccountEndpoint=https://test.documents.azure.com:443/;AccountKey=test;"
        
        mock_container = MagicMock()
        mock_database = MagicMock()
        mock_client_instance = MagicMock()
        
        mock_cosmos_client.from_connection_string.return_value = mock_client_instance
        mock_client_instance.get_database_client.return_value = mock_database
        mock_database.get_container_client.return_value = mock_container

        # Simular item existente
        mock_item = {"id": "p-123", "clienteId": "c-1", "estado": "pendiente"}
        mock_container.read_item.return_value = mock_item

        req = func.HttpRequest(
            method='PUT',
            body=json.dumps({"estado": "entregado"}).encode('utf8'),
            url='/api/pedidos/p-123',
            route_params={'id': 'p-123'}
        )

        # Ejecutar función
        resp = actualizarEstado(req)

        # Verificaciones
        self.assertEqual(resp.status_code, 200)
        resp_json = json.loads(resp.get_body())
        self.assertEqual(resp_json["nuevoEstado"], "entregado")
        
        # Verificar que se llamó a Cosmos DB para leer y luego reemplazar
        mock_container.read_item.assert_called_once()
        mock_container.replace_item.assert_called_once()

    def test_actualizar_estado_missing_field(self):
        req = func.HttpRequest(
            method='PUT',
            body=json.dumps({}).encode('utf8'),
            url='/api/pedidos/p-123',
            route_params={'id': 'p-123'}
        )

        # Ejecutar función
        resp = actualizarEstado(req)

        # Verificaciones
        self.assertEqual(resp.status_code, 400)
        resp_json = json.loads(resp.get_body())
        self.assertTrue("error" in resp_json)

if __name__ == '__main__':
    unittest.main()
