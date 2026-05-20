import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Añadir el path para importar los servicios
sys.path.append(os.path.join(os.getcwd(), 'src', 'backend'))

from services.notification_service import NotificationService

class TestNotificationService(unittest.TestCase):
    def setUp(self):
        self.env_patcher = patch.dict(os.environ, {
            "NOTIFICATION_HUB_CONNECTION_STRING": "Endpoint=sb://test-ns.servicebus.windows.net/;SharedAccessKeyName=test-key;SharedAccessKey=test-secret",
            "NOTIFICATION_HUB_NAME": "test-hub"
        })
        self.env_patcher.start()
        self.service = NotificationService()

    def tearDown(self):
        self.env_patcher.stop()

    def test_sas_token_generation(self):
        uri = "https://test-ns.servicebus.windows.net/test-hub/messages/?api-version=2015-01"
        token = self.service._generate_sas_token(uri)
        
        self.assertTrue(token.startswith("SharedAccessSignature "))
        # Azure quote usa mayúsculas para los escapes (e.g. %3A en lugar de %3a)
        self.assertIn("sr=https%3A%2F%2Ftest-ns.servicebus.windows.net%2Ftest-hub%2Fmessages%2F", token)
        self.assertIn("skn=test-key", token)
        # Verificar que el query string NO esté en el token
        self.assertNotIn("api-version", token)


    @patch('requests.post')
    def test_notificar_cambio_estado_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response
        
        result = self.service.notificar_cambio_estado("123", "entregado", "user1")
        
        self.assertTrue(result)
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['headers']['ServiceBusNotification-Format'], 'gcm')
        self.assertIn('Authorization', kwargs['headers'])

if __name__ == '__main__':
    unittest.main()
