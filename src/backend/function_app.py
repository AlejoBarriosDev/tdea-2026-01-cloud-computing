import azure.functions as func
from blueprints.pedidos import pedidos_bp

# Inicialización de la aplicación de funciones
# El auth_level ANONYMOUS se usa porque la seguridad la maneja Azure API Management mediante JWT
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Registro de Blueprints (Modularización)
app.register_blueprint(pedidos_bp)
