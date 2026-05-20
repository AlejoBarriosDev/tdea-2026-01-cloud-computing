import azure.functions as func
from blueprints.pedidos import pedidos_bp

# Inicialización de la aplicación de funciones
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Función de salud directa para diagnóstico
@app.route(route="health", methods=["GET"])
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("RapidGo Backend is Online and Modular", status_code=200)

# Registro de Blueprints (Modularización)
app.register_blueprint(pedidos_bp)
