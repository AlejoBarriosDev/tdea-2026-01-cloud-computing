# Proyecto RapidGo - Backend Serverless en Azure

## Portada
- **Nombre del Proyecto:** RapidGo
- **Materia:** Cloud Computing
- **Estudiantes:** [Nombres de los estudiantes]
- **Docente:** [Nombre del docente]
- **Institución:** Tecnológico de Antioquia (TdeA)

---

## 1. Modelo C4

### 1.1 Diagrama C1 - Contexto
El sistema RapidGo como caja negra, interactuando con actores (cliente, repartidor, administrador) y sistemas externos (app móvil, pasarela de pagos, FCM, APNs).

![Diagrama C1](assets/C1.drawio)

### 1.2 Diagrama C2 - Contenedores
*(Reemplazar con el diagrama C2)*

Contenedores identificados:
- **API Management:** Punto de entrada único para la app móvil. Gestiona autenticación, throttling y versionado.
- **Azure Functions:** Lógica de negocio (registrar pedidos, actualizar estados, consultar historial).
- **Cosmos DB:** Persistencia de pedidos, usuarios y estados de entrega.
- **Blob Storage:** Fotos de comprobantes de entrega e imágenes.
- **Notification Hubs:** Notificaciones push en tiempo real.

### 1.3 Diagrama C3 - Componentes
*(Reemplazar con el diagrama C3)*

Componentes internos de las Azure Functions:
- `registrarPedido`
- `actualizarEstado`
- `consultarHistorial`
- `notificarCliente`

---

## 2. Decisiones Arquitectónicas (ADRs)

### ADR-01: Azure Functions vs App Service para la lógica de negocio
- **Contexto:** El equipo de infraestructura consta de una sola persona, por lo que se requiere minimizar la administración de servidores. Además, la carga de la aplicación puede variar, y el proyecto busca aprovechar el "free tier" (Consumption Plan).
- **Alternativas evaluadas:** 
  1. Azure Functions (Serverless).
  2. Azure App Service (PaaS).
- **Decisión:** [Completar decisión justificada]
- **Consecuencias:** [Completar ventajas obtenidas y trade-offs asumidos]

### ADR-02: Cosmos DB vs Azure SQL Database para la persistencia de pedidos
- **Contexto:** Se requiere flexibilidad para los atributos variables según el tipo de negocio.
- **Alternativas evaluadas:**
  1. Azure Cosmos DB (NoSQL).
  2. Azure SQL Database (Relacional).
- **Decisión:** [Completar decisión justificada]
- **Consecuencias:** [Completar ventajas obtenidas y trade-offs asumidos]

### ADR-03: API Management vs exposición directa de las Functions
- **Contexto:** Se necesita gestionar la autenticación JWT, limitar las peticiones por usuario (throttling) y controlar el versionado de la API móvil existente.
- **Alternativas evaluadas:**
  1. Azure API Management.
  2. Exposición directa de Azure Functions usando function keys.
- **Decisión:** [Completar decisión justificada]
- **Consecuencias:** [Completar ventajas obtenidas y trade-offs asumidos]

### ADR-04: Blob Storage vs Azure Files para almacenamiento de archivos
- **Contexto:** Es necesario guardar fotos de comprobantes de entrega, imágenes de productos y exports. Se busca la opción de menor costo para objetos no estructurados.
- **Alternativas evaluadas:**
  1. Azure Blob Storage.
  2. Azure Files.
- **Decisión:** [Completar decisión justificada]
- **Consecuencias:** [Completar ventajas obtenidas y trade-offs asumidos]

### ADR-05: Notification Hubs vs Azure Communication Services para notificaciones push
- **Contexto:** Se necesita notificar en tiempo real a dispositivos Android (FCM) e iOS (APNs) sobre el cambio de estado de los pedidos, maximizando el free tier.
- **Alternativas evaluadas:**
  1. Azure Notification Hubs.
  2. Azure Communication Services.
- **Decisión:** [Completar decisión justificada]
- **Consecuencias:** [Completar ventajas obtenidas y trade-offs asumidos]

---

## 3. Implementación del Flujo Crítico (Evidencias)

A continuación, se documentarán las evidencias visuales (capturas de pantalla) del funcionamiento de extremo a extremo:

1. **Grupo de recursos en Azure:**
   *(Insertar captura con los 5 servicios desplegados)*
2. **Logs de ejecución exitosa:**
   *(Insertar captura de logs de las Functions en el Portal de Azure)*
3. **Documento en Cosmos DB:**
   *(Insertar captura mostrando la estructura JSON del pedido)*
4. **Notificación enviada (Notification Hubs):**
   *(Insertar captura de la prueba o envío simulado)*
5. **Pruebas de la API:**
   *(Colección de Postman exportada en `/src/` con las llamadas documentadas y/o capturas de respuesta exitosa)*

---

## 4. Conclusiones
[Escribir las conclusiones finales del proyecto, hallazgos, retos presentados y lecciones aprendidas]