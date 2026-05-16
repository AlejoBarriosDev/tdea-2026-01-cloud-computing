import unittest
from unittest.mock import patch, MagicMock
import azure.functions as func
import json
from blueprints.pedidos import actualizarEstado

class TestActualizarEstado(unittest.TestCase):

    @patch('blueprints.pedidos.cosmos_service')
    @patch('blueprints.pedidos.notification_service')
    @patch('blueprints.pedidos.blob_service')
    def test_actualizar_estado_success(self, mock_blob_service, mock_notification_service, mock_cosmos_service):
        # Configurar mock de base de datos para devolver un pedido ficticio
        mock_cosmos_service.actualizar_estado_pedido.return_value = {"clienteId": "C-123", "id": "p-123"}
        mock_blob_service.subir_comprobante.return_value = "https://azure.com/blob.jpg"

        req = func.HttpRequest(
            method='PUT',
            url='/api/pedidos/p-123',
            route_params={'id': 'p-123'},
            body=json.dumps({
                "estado": "entregado", 
                "repartidorId": "R-1",
                "evidenciaBase64": "SGVsbG8="
            }).encode('utf8')
        )

        resp = actualizarEstado(req)
        resp_json = json.loads(resp.get_body())

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp_json["notificado"])
        self.assertEqual(resp_json["urlEvidencia"], "https://azure.com/blob.jpg")
        
        mock_cosmos_service.actualizar_estado_pedido.assert_called_once()
        mock_blob_service.subir_comprobante.assert_called_once()
        mock_notification_service.notificar_cambio_estado.assert_called_once()

if __name__ == '__main__':
    unittest.main()
