import requests
import time
import json
import base64
import hmac
import hashlib

def base64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def generate_jwt(secret):
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": "12345",
        "name": "RapidGo Test User",
        "exp": int(time.time()) + 3600
    }
    
    segments = [
        base64url_encode(json.dumps(header).encode('utf-8')),
        base64url_encode(json.dumps(payload).encode('utf-8'))
    ]
    
    signing_input = ".".join(segments).encode('utf-8')
    signature = hmac.new(secret.encode('utf-8'), signing_input, hashlib.sha256).digest()
    segments.append(base64url_encode(signature))
    
    return ".".join(segments)

base_url = "https://apim-rapidgo-gateway.azure-api.net/api"
sub_key = "80820f490cf742cc87e85681cbd84a96"
secret = "jwt_secret_dummy"

jwt = generate_jwt(secret)
headers = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": sub_key,
    "Authorization": f"Bearer {jwt}"
}

print("--- Step 1: Registrar Pedido ---")
body = {
    "clienteId": "12345",
    "items": [{"productoId": "A01", "cantidad": 1}],
    "direccion": "Calle Test",
    "metodoPago": "efectivo"
}
r1 = requests.post(f"{base_url}/pedidos", json=body, headers=headers)
print(f"Status: {r1.status_code}")
print(f"Response: {r1.text}")
pedido_id = r1.json().get("pedidoId")

print("\n--- Waiting 5 seconds for consistency ---")
time.sleep(5)

print("\n--- Step 2: Consultar Historial ---")
r2 = requests.get(f"{base_url}/pedidos?clienteId=12345", headers=headers)
print(f"Status: {r2.status_code}")
print(f"Response: {r2.text}")

found = any(p.get("id") == pedido_id for p in r2.json())
print(f"Pedido {pedido_id} found in history: {found}")
