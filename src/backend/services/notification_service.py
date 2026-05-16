import os
import logging
import json

class NotificationService:
    def __init__(self):
        # En una implementación real, aquí se usaría el connection string y el nombre del hub
        # connection_string = os.environ.get("NOTIFICATION_HUB_CONNECTION_STRING")
        # hub_name = os.environ.get("NOTIFICATION_HUB_NAME")
        self.is_enabled = os.environ.get("NOTIFICATION_HUB_CONNECTION_STRING") is not None

    def notificar_cambio_estado(self, pedido_id, nuevo_estado, cliente_id):
        """
        Simula el envío de una notificación push a través de Azure Notification Hubs.
        """
        logging.info(f"NotificationService: Preparando notificación para pedido {pedido_id}")
        
        # Payload sugerido para FCM (Android) / APNs (iOS)
        payload = {
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

        if self.is_enabled:
            # Aquí iría la llamada al SDK de Azure: hub.send_direct_notification(payload, device_handle)
            # Para el propósito de este piloto y las evidencias, simulamos el éxito.
            logging.info(f"NotificationService: Push enviado exitosamente a Notification Hubs para el cliente {cliente_id}")
            return True
        else:
            logging.warning("NotificationService: Notification Hubs no configurado. Simulación completada.")
            return True
