import azure.functions as func
import json
import logging
import uuid
import datetime
from services.cosmos_service import CosmosService
from services.notification_service import NotificationService
from services.blob_service import BlobService
from azure.cosmos import exceptions

pedidos_bp = func.Blueprint()
cosmos_service = CosmosService()
notification_service = NotificationService()
blob_service = BlobService()

@pedidos_bp.route(route="pedidos", methods=["POST"])
def registrarPedido(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Blueprint: Registrando nuevo pedido.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(json.dumps({"error": "JSON inválido"}), status_code=400, mimetype="application/json")

    # Validación
    required = ["clienteId", "items", "direccion", "metodoPago"]
    for field in required:
        if field not in req_body:
            return func.HttpResponse(json.dumps({"error": f"Falta {field}"}), status_code=400, mimetype="application/json")

    # Enriquecer datos
    req_body["id"] = str(uuid.uuid4())
    req_body["estado"] = "pendiente"
    req_body["fechaCreacion"] = datetime.datetime.utcnow().isoformat()

    try:
        cosmos_service.crear_pedido(req_body)
        return func.HttpResponse(
            json.dumps({"mensaje": "Pedido registrado exitosamente", "pedidoId": req_body["id"]}),
            status_code=201,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, mimetype="application/json")

@pedidos_bp.route(route="pedidos", methods=["GET"])
def consultarHistorial(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Blueprint: Consultando historial.')
    cliente_id = req.params.get('clienteId')

    if not cliente_id:
        return func.HttpResponse(json.dumps({"error": "clienteId requerido"}), status_code=400, mimetype="application/json")

    try:
        pedidos = cosmos_service.obtener_pedidos_cliente(cliente_id)
        return func.HttpResponse(json.dumps(pedidos), status_code=200, mimetype="application/json")
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, mimetype="application/json")

@pedidos_bp.route(route="pedidos/{id}", methods=["PUT"])
def actualizarEstado(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Blueprint: Actualizando estado.')
    pedido_id = req.route_params.get('id')
    
    try:
        req_body = req.get_json()
        nuevo_estado = req_body.get('estado')
        repartidor_id = req_body.get('repartidorId')
        evidencia_b64 = req_body.get('evidenciaBase64')
    except ValueError:
        return func.HttpResponse(json.dumps({"error": "JSON inválido"}), status_code=400, mimetype="application/json")

    if not nuevo_estado:
        return func.HttpResponse(json.dumps({"error": "estado requerido"}), status_code=400, mimetype="application/json")

    try:
        # 1. Subir evidencia opcional a Blob Storage (Paso 4 C4)
        url_evidencia = None
        if evidencia_b64:
            url_evidencia = blob_service.subir_comprobante(pedido_id, evidencia_b64)

        # 2. Actualizar en Base de Datos
        pedido_actualizado = cosmos_service.actualizar_estado_pedido(pedido_id, nuevo_estado, repartidor_id)
        
        # 3. Notificar al cliente (Paso 5 C4)
        cliente_id = pedido_actualizado.get('clienteId', 'desconocido')
        notification_service.notificar_cambio_estado(pedido_id, nuevo_estado, cliente_id)

        return func.HttpResponse(
            json.dumps({
                "mensaje": "Actualizado exitosamente y notificación enviada", 
                "pedidoId": pedido_id,
                "notificado": True,
                "urlEvidencia": url_evidencia
            }),
            status_code=200,
            mimetype="application/json"
        )
    except exceptions.CosmosResourceNotFoundError:
        return func.HttpResponse(json.dumps({"error": "No encontrado"}), status_code=404, mimetype="application/json")
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, mimetype="application/json")
