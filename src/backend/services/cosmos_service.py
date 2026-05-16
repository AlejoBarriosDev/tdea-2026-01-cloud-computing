import os
import logging
from azure.cosmos import CosmosClient, exceptions

class CosmosService:
    def __init__(self):
        self.connection_string = os.environ.get("COSMOS_DB_CONNECTION_STRING")
        self.database_name = "rapidgo-db"
        self.container_name = "pedidos"
        self._container = None

    @property
    def container(self):
        if self._container is None:
            try:
                client = CosmosClient.from_connection_string(self.connection_string)
                database = client.get_database_client(self.database_name)
                self._container = database.get_container_client(self.container_name)
            except Exception as e:
                logging.error(f"Error conectando a Cosmos DB: {str(e)}")
                raise e
        return self._container

    def crear_pedido(self, pedido_data):
        try:
            return self.container.create_item(body=pedido_data)
        except exceptions.CosmosHttpResponseError as e:
            logging.error(f"Error al crear pedido en Cosmos DB: {str(e)}")
            raise e

    def obtener_pedidos_cliente(self, cliente_id):
        try:
            query = "SELECT * FROM c WHERE c.clienteId = @clienteId"
            parameters = [{"name": "@clienteId", "value": cliente_id}]
            items = self.container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=True
            )
            return list(items)
        except exceptions.CosmosHttpResponseError as e:
            logging.error(f"Error al consultar historial: {str(e)}")
            raise e

    def actualizar_estado_pedido(self, pedido_id, nuevo_estado, repartidor_id=None):
        try:
            # En Cosmos DB SQL API v4, read_item requiere partition_key
            # Según terraform, el partition key es "/id" (que es el mismo id)
            item = self.container.read_item(item=pedido_id, partition_key=pedido_id)
            
            item["estado"] = nuevo_estado
            if repartidor_id:
                item["repartidorId"] = repartidor_id
            
            import datetime
            item["fechaActualizacion"] = datetime.datetime.utcnow().isoformat()

            return self.container.replace_item(item=pedido_id, body=item)
        except exceptions.CosmosResourceNotFoundError:
            raise exceptions.CosmosResourceNotFoundError(message=f"Pedido {pedido_id} no encontrado")
        except exceptions.CosmosHttpResponseError as e:
            logging.error(f"Error al actualizar pedido: {str(e)}")
            raise e
