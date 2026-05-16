import unittest
from unittest.mock import patch, MagicMock
import azure.functions as func
import json
from blueprints.pedidos import actualizarEstado

class TestActualizarEstado(unittest.TestCase):

    @patch('blueprints.pedidos.cosmos_service')
    def test_actualizar_estado_success(self, mock_cosmos_service):
        req = func.HttpRequest(
            method='PUT',
            body=json.dumps({"estado": "entregado"}).encode('utf8'),
            url='/api/pedidos/p-123',
            route_params={'id': 'p-123'}
        )

        resp = actualizarEstado(req)

        self.assertEqual(resp.status_code, 200)
        mock_cosmos_service.actualizar_estado_pedido.assert_called_once()

if __name__ == '__main__':
    unittest.main()
