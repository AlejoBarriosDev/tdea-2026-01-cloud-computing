import unittest
from unittest.mock import patch, MagicMock
import azure.functions as func
import json
from blueprints.pedidos import registrarPedido

class TestRegistrarPedido(unittest.TestCase):

    @patch('blueprints.pedidos.cosmos_service')
    def test_registrar_pedido_success(self, mock_cosmos_service):
        # Datos de prueba
        pedido_data = {
            "clienteId": "12345",
            "items": [{"productoId": "A1", "cantidad": 1}],
            "direccion": "Calle Falsa 123",
            "metodoPago": "efectivo"
        }
        
        req = func.HttpRequest(
            method='POST',
            url='/api/pedidos',
            body=json.dumps(pedido_data).encode('utf8')
        )

        # Ejecutar función
        resp = registrarPedido(req)

        # Verificaciones
        self.assertEqual(resp.status_code, 201)
        resp_json = json.loads(resp.get_body())
        self.assertEqual(resp_json["mensaje"], "Pedido registrado exitosamente")
        
        # Verificar que se llamó al servicio
        mock_cosmos_service.crear_pedido.assert_called_once()

    def test_registrar_pedido_missing_fields(self):
        req = func.HttpRequest(
            method='POST',
            url='/api/pedidos',
            body=json.dumps({"clienteId": "12345"}).encode('utf8')
        )
        resp = registrarPedido(req)
        self.assertEqual(resp.status_code, 400)

if __name__ == '__main__':
    unittest.main()
