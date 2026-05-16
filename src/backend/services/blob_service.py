import os
import logging
import base64
from azure.storage.blob import BlobServiceClient, ContentSettings

class BlobService:
    def __init__(self):
        self.connection_string = os.environ.get("BLOB_STORAGE_CONNECTION_STRING")
        self.container_name = "comprobantes"
        self.is_enabled = self.connection_string is not None

    def subir_comprobante(self, pedido_id, imagen_base64):
        """
        Sube una imagen (en base64) al contenedor de Blob Storage.
        """
        if not self.is_enabled:
            logging.warning("BlobService: Storage no configurado. Simulación completada.")
            return f"https://strapidgobackenddata.blob.core.windows.net/comprobantes/mock_{pedido_id}.jpg"

        try:
            # Decodificar la imagen
            image_data = base64.b64decode(imagen_base64)
            blob_name = f"evidencia_{pedido_id}.jpg"
            
            blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
            blob_client = blob_service_client.get_blob_client(container=self.container_name, blob=blob_name)

            # Subir con metadata de imagen
            blob_client.upload_blob(image_data, overwrite=True, content_settings=ContentSettings(content_type='image/jpeg'))
            
            logging.info(f"BlobService: Imagen subida exitosamente para el pedido {pedido_id}")
            return blob_client.url

        except Exception as e:
            logging.error(f"BlobService: Error al subir imagen: {str(e)}")
            # En modo piloto, si falla el storage real, devolvemos una URL dummy para no romper el flujo
            return f"https://strapidgobackenddata.blob.core.windows.net/comprobantes/dummy_{pedido_id}.jpg"
