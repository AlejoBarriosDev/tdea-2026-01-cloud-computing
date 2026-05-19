import os
import logging
import json
import time
import hmac
import hashlib
import base64
import requests
from urllib.parse import quote

class NotificationService:
    def __init__(self):
        self.connection_string = os.environ.get("NOTIFICATION_HUB_CONNECTION_STRING")
        self.hub_name = os.environ.get("NOTIFICATION_HUB_NAME")
        self.is_enabled = self.connection_string is not None and self.hub_name is not None
        
        if self.is_enabled:
            # Parse connection string to get Endpoint and SasKeyName/SasKey
            try:
                parts = dict(item.split("=", 1) for item in self.connection_string.split(";"))
                self.endpoint = parts.get("Endpoint")
                self.sas_key_name = parts.get("SharedAccessKeyName")
                self.sas_key = parts.get("SharedAccessKey")
                
                # Normalize endpoint (ensure https and no trailing slash)
                if self.endpoint:
                    self.endpoint = self.endpoint.replace("sb://", "https://")
                    if not self.endpoint.endswith("/"):
                        self.endpoint += "/"
            except Exception as e:
                logging.error(f"Error parseando connection string: {str(e)}")
                self.is_enabled = False

    def _generate_sas_token(self, uri):
        """Genera un token SAS para autenticarse con el REST API de Notification Hubs."""
        target_uri = quote(uri, safe='')
        expires = int(time.time() + 3600)  # Expira en 1 hora
        to_sign = f"{target_uri}\n{expires}"
        
        signature = base64.b64encode(
            hmac.new(self.sas_key.encode('utf-8'), to_sign.encode('utf-8'), hashlib.sha256).digest()
        ).decode('utf-8')
        
        return f"SharedAccessSignature sr={target_uri}&sig={quote(signature)}&se={expires}&skn={self.sas_key_name}"

    def notificar_cambio_estado(self, pedido_id, nuevo_estado, cliente_id):
        """
        Envía una notificación push a través de la API REST de Azure Notification Hubs.
        Esto genera métricas de 'Incoming Messages' en el portal.
        """
        logging.info(f"NotificationService: Preparando notificación para pedido {pedido_id}")
        
        if not self.is_enabled:
            logging.warning("NotificationService: Notification Hubs no configurado. Simulación completada.")
            return True

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

        try:
            # URL para enviar notificaciones de tipo FCM (Google)
            # Formato: https://{namespace}.servicebus.windows.net/{hubName}/messages/?api-version=2015-01
            url = f"{self.endpoint}{self.hub_name}/messages/?api-version=2015-01"
            
            headers = {
                "Authorization": self._generate_sas_token(url),
                "Content-Type": "application/json;charset=utf-8",
                "ServiceBusNotification-Format": "gcm" # GCM es el formato para FCM en la API REST
            }

            response = requests.post(url, data=json.dumps(fcm_payload), headers=headers, timeout=10)
            
            if response.status_code in [200, 201]:
                logging.info(f"NotificationService: API REST llamada exitosamente (Status {response.status_code})")
                return True
            else:
                logging.error(f"Error en API de Notification Hubs: {response.status_code} - {response.text}")
                return True # Retornamos True para no bloquear el flujo
                
        except Exception as e:
            logging.error(f"Error al enviar notificación via REST: {str(e)}")
            return True
