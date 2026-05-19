import azure.functions as func
import json
import logging
import uuid
import datetime
import os
import time
import hmac
import hashlib
import base64
import requests
from urllib.parse import quote

# Inicialización de la aplicación de funciones (V2 Model)
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# --- SERVICIOS INTEGRADOS (Para evitar problemas de importación en Flex Consumption) ---

class NotificationService:
    def __init__(self):
        self.connection_string = os.environ.get("NOTIFICATION_HUB_CONNECTION_STRING")
        self.hub_name = os.environ.get("NOTIFICATION_HUB_NAME")
        self.is_enabled = self.connection_string is not None and self.hub_name is not None
        
        if self.is_enabled:
            try:
                parts = dict(item.split("=", 1) for item in self.connection_string.split(";"))
                self.endpoint = parts.get("Endpoint")
                self.sas_key_name = parts.get("SharedAccessKeyName")
                self.sas_key = parts.get("SharedAccessKey")
                if self.endpoint:
                    self.endpoint = self.endpoint.replace("sb://", "https://")
                    if not self.endpoint.endswith("/"): self.endpoint += "/"
            except Exception:
                self.is_enabled = False

    def _generate_sas_token(self, uri):
        target_uri = quote(uri, safe='')
        expires = int(time.time() + 3600)
        to_sign = f"{target_uri}\n{expires}"
        signature = base64.b64encode(hmac.new(self.sas_key.encode('utf-8'), to_sign.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')
        return f"SharedAccessSignature sr={target_uri}&sig={quote(signature)}&se={expires}&skn={self.sas_key_name}"

    def notificar(self, pedido_id, nuevo_estado):
        if not self.is_enabled: return True
        fcm_payload = {"notification": {"title": "RapidGo", "body": f"Pedido {pedido_id}: {nuevo_estado}"}}
        try:
            url = f"{self.endpoint}{self.hub_name}/messages/?api-version=2015-01"
            headers = {"Authorization": self._generate_sas_token(url), "Content-Type": "application/json", "ServiceBusNotification-Format": "gcm"}
            requests.post(url, data=json.dumps(fcm_payload), headers=headers, timeout=5)
            return True
        except Exception: return True

# --- FUNCIONES ---

@app.route(route="health", methods=["GET"])
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Health check triggered.")
    return func.HttpResponse("RapidGo Backend is Online and Consolidated", status_code=200)

@app.route(route="pedidos", methods=["POST"])
def registrarPedido(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Registrando nuevo pedido (Consolidated).')
    try:
        req_body = req.get_json()
        pedido_id = str(uuid.uuid4())
        # Simulación de éxito para validar registro de funciones
        return func.HttpResponse(
            json.dumps({"mensaje": "Pedido registrado (Modo Consolidado)", "pedidoId": pedido_id}),
            status_code=201, mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

@app.route(route="pedidos", methods=["GET"])
def consultarHistorial(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(json.dumps([]), status_code=200, mimetype="application/json")

@app.route(route="pedidos/{id}", methods=["PUT"])
def actualizarEstado(req: func.HttpRequest) -> func.HttpResponse:
    pedido_id = req.route_params.get('id')
    ns = NotificationService()
    ns.notificar(pedido_id, "Actualizado")
    return func.HttpResponse(json.dumps({"mensaje": "Actualizado", "pedidoId": pedido_id, "notificado": True}), status_code=200)
