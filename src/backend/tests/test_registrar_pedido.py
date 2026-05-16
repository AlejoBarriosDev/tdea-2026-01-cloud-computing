import unittest
from unittest.mock import patch, MagicMock
import azure.functions as func
import json
from function_app import registrarPedido

class TestRegistrarPedido(unittest.TestCase):

    @patch('function_app.CosmosClient')
    @patch('os.environ.get')
    def test_registrar_pedido_success(self, mock_env_get, mock_cosmos_client):
        # Configurar mocks
        mock_env_get.return_value = "AccountEndpoint=https://test.documents.azure.com:443/;AccountKey=test;"
        
        mock_container = MagicMock()
        mock_database = MagicMock()
        mock_client_instance = MagicMock()
        
        mock_cosmos_client.from_connection_string.return_value = mock_client_instance
        mock_client_instance.get_database_client.return_value = mock_database
        mock_database.get_container_client.return_value = mock_container

        # Datos de prueba
        pedido_data = {
            "clienteId": "12345",
            "items": [{"productoId": "A1", "cantidad": 1}],
            "direccion": "Calle Falsa 123",
            "metodoPago": "efectivo"
        }
        
        req = func.HttpRequest(
            method='POST',
            body=json.dumps(pedido_data).encode('utf8'),
            url='/api/pedidos'
        )

        # Ejecutar función
        resp = registrarPedido(req)

        # Verificaciones
        self.assertEqual(resp.status_code, 201)
        resp_json = json.loads(resp.get_body())
        self.assertEqual(resp_json["mensaje"], "Pedido registrado exitosamente")
        self.assertTrue("pedidoId" in resp_json)
        
        # Verificar que se llamó a Cosmos DB
        mock_container.create_item.assert_called_once()

    def test_registrar_pedido_missing_fields(self):
        # Datos incompletos
        pedido_data = {
            "clienteId": "12345"
        }
        
        req = func.HttpRequest(
            method='POST',
            body=json.dumps(pedido_data).encode('utf8'),
            url='/api/pedidos'
        )

        # Ejecutar función
        resp = registrarPedido(req)

        # Verificaciones
        self.assertEqual(resp.status_code, 400)
        resp_json = json.loads(resp.get_body())
        self.assertTrue("error" in resp_json)
        self.assertIn("es obligatorio", resp_json["error"])

if __name__ == '__main__':
    unittest.main()
