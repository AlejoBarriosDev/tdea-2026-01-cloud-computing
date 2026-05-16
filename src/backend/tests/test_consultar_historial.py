import unittest
from unittest.mock import patch, MagicMock
import azure.functions as func
import json
from blueprints.pedidos import consultarHistorial

class TestConsultarHistorial(unittest.TestCase):

    @patch('blueprints.pedidos.cosmos_service')
    def test_consultar_historial_success(self, mock_cosmos_service):
        mock_cosmos_service.obtener_pedidos_cliente.return_value = [{"id": "1"}]
        
        req = func.HttpRequest(
            method='GET',
            url='/api/pedidos',
            params={'clienteId': '12345'},
            body=b''
        )

        resp = consultarHistorial(req)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(json.loads(resp.get_body())), 1)

if __name__ == '__main__':
    unittest.main()
