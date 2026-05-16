import azure.functions as func
import json
import logging
import os
import uuid
from azure.cosmos import CosmosClient, exceptions

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Configuración de Cosmos DB desde variables de entorno
COSMOS_DB_CONNECTION_STRING = os.environ.get("COSMOS_DB_CONNECTION_STRING")
DATABASE_NAME = "rapidgo-db"
CONTAINER_NAME = "pedidos"

@app.route(route="pedidos", methods=["POST"])
def registrarPedido(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Procesando solicitud para registrar un nuevo pedido.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
             json.dumps({"error": "Cuerpo de solicitud inválido, debe ser JSON."}),
             status_code=400,
             mimetype="application/json"
        )

    # Validación básica de campos obligatorios
    required_fields = ["clienteId", "items", "direccion", "metodoPago"]
    for field in required_fields:
        if field not in req_body:
            return func.HttpResponse(
                json.dumps({"error": f"El campo '{field}' es obligatorio."}),
                status_code=400,
                mimetype="application/json"
            )

    # Generar ID único y estado inicial
    pedido_id = str(uuid.uuid4())
    req_body["id"] = pedido_id
    req_body["estado"] = "pendiente"
    req_body["fechaCreacion"] = func.datetime.datetime.utcnow().isoformat()

    try:
        # Inicializar cliente de Cosmos DB
        client = CosmosClient.from_connection_string(COSMOS_DB_CONNECTION_STRING)
        database = client.get_database_client(DATABASE_NAME)
        container = database.get_container_client(CONTAINER_NAME)

        # Insertar documento en Cosmos DB
        container.create_item(body=req_body)

        logging.info(f"Pedido {pedido_id} registrado exitosamente en Cosmos DB.")

        return func.HttpResponse(
            json.dumps({
                "mensaje": "Pedido registrado exitosamente",
                "pedidoId": pedido_id,
                "estado": "pendiente"
            }),
            status_code=201,
            mimetype="application/json"
        )

    except exceptions.CosmosHttpResponseError as e:
        logging.error(f"Error de Cosmos DB: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Error al persistir el pedido en la base de datos."}),
            status_code=500,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Ocurrió un error interno en el servidor."}),
            status_code=500,
            mimetype="application/json"
        )

@app.route(route="pedidos", methods=["GET"])
def consultarHistorial(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Consultando historial de pedidos.')

    cliente_id = req.params.get('clienteId')
    if not cliente_id:
        return func.HttpResponse(
            json.dumps({"error": "El parámetro 'clienteId' es obligatorio en la consulta."}),
            status_code=400,
            mimetype="application/json"
        )

    try:
        # Inicializar cliente de Cosmos DB
        client = CosmosClient.from_connection_string(COSMOS_DB_CONNECTION_STRING)
        database = client.get_database_client(DATABASE_NAME)
        container = database.get_container_client(CONTAINER_NAME)

        # Consultar pedidos del cliente
        query = "SELECT * FROM c WHERE c.clienteId = @clienteId ORDER BY c.fechaCreacion DESC"
        parameters = [{"name": "@clienteId", "value": cliente_id}]
        
        items = list(container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))

        return func.HttpResponse(
            json.dumps(items),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Error al consultar historial: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Ocurrió un error al recuperar el historial de pedidos."}),
            status_code=500,
            mimetype="application/json"
        )

@app.route(route="pedidos/{id}", methods=["PUT"])
def actualizarEstado(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Actualizando estado del pedido.')

    pedido_id = req.route_params.get('id')
    
    try:
        req_body = req.get_json()
        nuevo_estado = req_body.get('estado')
        repartidor_id = req_body.get('repartidorId')
    except ValueError:
        return func.HttpResponse(
             json.dumps({"error": "Cuerpo de solicitud inválido."}),
             status_code=400,
             mimetype="application/json"
        )

    if not nuevo_estado:
        return func.HttpResponse(
            json.dumps({"error": "El campo 'estado' es obligatorio."}),
            status_code=400,
            mimetype="application/json"
        )

    try:
        # Inicializar cliente de Cosmos DB
        client = CosmosClient.from_connection_string(COSMOS_DB_CONNECTION_STRING)
        database = client.get_database_client(DATABASE_NAME)
        container = database.get_container_client(CONTAINER_NAME)

        # Leer el item actual (necesario para actualizar en Cosmos DB SQL API si no se usa patch)
        # Usamos el id como partition key según la configuración de Terraform
        item = container.read_item(item=pedido_id, partition_key=pedido_id)
        
        # Actualizar campos
        item["estado"] = nuevo_estado
        if repartidor_id:
            item["repartidorId"] = repartidor_id
        item["fechaActualizacion"] = func.datetime.datetime.utcnow().isoformat()

        # Persistir cambios
        container.replace_item(item=pedido_id, body=item)

        logging.info(f"Pedido {pedido_id} actualizado a estado: {nuevo_estado}")

        # --- Lógica Adicional (C3 Diagram) ---
        # TODO: Cargar comprobante a Blob Storage si se incluye en el request
        # TODO: Enviar notificación push mediante Azure Notification Hubs
        
        return func.HttpResponse(
            json.dumps({
                "mensaje": "Estado del pedido actualizado exitosamente",
                "pedidoId": pedido_id,
                "nuevoEstado": nuevo_estado
            }),
            status_code=200,
            mimetype="application/json"
        )

    except exceptions.CosmosResourceNotFoundError:
        return func.HttpResponse(
            json.dumps({"error": f"No se encontró el pedido con ID {pedido_id}."}),
            status_code=404,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error al actualizar estado: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Ocurrió un error al actualizar el estado del pedido."}),
            status_code=500,
            mimetype="application/json"
        )
