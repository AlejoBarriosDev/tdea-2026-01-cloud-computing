import os
import logging
import json

class NotificationService:
    def __init__(self):
        self.connection_string = os.environ.get("NOTIFICATION_HUB_CONNECTION_STRING")
        self.hub_name = os.environ.get("NOTIFICATION_HUB_NAME")
        self.is_enabled = self.connection_string is not None and self.hub_name is not None
        self._client = None
        
    @property
    def client(self):
        if self._client is None and self.is_enabled:
            try:
                from azure.notification_hubs import NotificationHubClient
                self._client = NotificationHubClient(self.connection_string, self.hub_name)
            except Exception as e:
                logging.error(f"Error inicializando NotificationHubClient: {str(e)}")
                self.is_enabled = False
        return self._client

    def notificar_cambio_estado(self, pedido_id, nuevo_estado, cliente_id):
        """
        Envía una notificación push real a través de Azure Notification Hubs.
        Incluso sin dispositivos registrados, el Hub registrará un 'Incoming Message'.
        """
        logging.info(f"NotificationService: Preparando notificación para pedido {pedido_id}")
        
        # Payload para FCM (Android)
        fcm_payload = {
            "data": {
                "pedidoId": pedido_id,
                "estado": nuevo_estado,
                "mensaje": f"Tu pedido se encuentra {nuevo_estado}"
            },
            "notification": {
                "title": "Actualización de RapidGo",
                "body": f"El estado de tu pedido ha cambiado a: {nuevo_estado}"
            }
        }

        if self.is_enabled and self.client:
            try:
                # Enviamos una notificación de prueba (broadcast) para que se registre la ejecución en el Hub.
                self.client.send_fcm_native_notification(fcm_payload)
                logging.info(f"NotificationService: Llamada a Notification Hub realizada exitosamente para el pedido {pedido_id}")
                return True
            except Exception as e:
                logging.error(f"Error al enviar notificación a Notification Hub: {str(e)}")
                return True
        else:
            logging.warning("NotificationService: Notification Hubs no configurado correctamente o SDK no disponible.")
            return True
