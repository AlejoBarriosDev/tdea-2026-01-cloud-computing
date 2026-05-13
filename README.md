# Proyecto RapidGo - Backend Serverless en Azure

## Portada
- **Nombre del Proyecto:** RapidGo
- **Materia:** Cloud Computing
- **Estudiantes:** Diego Alejandro Barrios, Andrés Camilo Diaz, Jose Alejandro Colorado
- **Docente:** Julián David Flórez Sánchez
- **Institución:** Tecnológico de Antioquia (TdeA)

---

## 1. Modelo C4

### 1.1 Diagrama C1 - Contexto
Este diagrama representa la arquitectura de RapidGo en su nivel más alto de abstracción. El backend serverless se modela como un sistema central aislado (caja negra) para ilustrar explícitamente sus límites y las interacciones con las entidades externas al modelo de dominio.

**Elementos clave del diagrama:**
- **Sistema Central:** Sistema RapidGo (nueva arquitectura Cloud).
- **Actores Operativos:**
  - **Cliente:** Actor que inyecta la demanda transaccional (creación y monitoreo de pedidos).
  - **Repartidor:** Actor logístico que consume y actualiza los estados de entrega.
  - **Administrador:** Actor con privilegios de supervisión sobre la plataforma.
- **Dependencias de Software Externas:**
  - **App Móvil:** Cliente Frontend (React Native) que actúa como interfaz de usuario consumiendo la API de RapidGo.
  - **Pasarela de Pagos:** Servicio de terceros requerido para la autorización y captura de transacciones.
  - **FCM / APNs:** Proveedores de infraestructura externa (Google y Apple) utilizados para el enrutamiento y entrega de notificaciones push asíncronas hacia los dispositivos finales.

![C1](assets/images/C1.svg)
[Diagrama C1](assets/C4_Diagrams.drawio)

### 1.2 Diagrama C2 - Contenedores
Este diagrama expone la arquitectura interna del backend de RapidGo, reemplazando el monolito anterior por una arquitectura Serverless en Microsoft Azure orientada a alta disponibilidad, tolerancia a fallos y pago por uso.

**Componentes principales:**
- **Azure API Management:** Actúa como API Gateway y fachada para los clientes móviles, centralizando la seguridad (validación JWT) y protegiendo el sistema de sobrecargas mediante políticas de throttling.
- **Azure Functions:** Contenedor de procesamiento stateless que aloja la lógica de negocio escrita en Node.js o Python. Maneja elásticamente la concurrencia en los picos de demanda sin intervención manual.
- **Azure Cosmos DB:** Repositorio de datos NoSQL que sustituye al esquema relacional rígido anterior. Permite guardar la información de pedidos de forma documental, facilitando el registro de atributos variables.
- **Azure Blob Storage:** Destino de almacenamiento para objetos binarios pesados (imágenes y comprobantes).
- **Azure Notification Hubs:** Servicio de mensajería responsable del broadcasting e inserción unificada de notificaciones hacia Apple (APNs) y Google (FCM), resolviendo la baja tasa de entrega del sistema legado.  

![C2](assets/images/C2.svg)
[Diagrama C2](assets/C4_Diagrams.drawio)

### 1.3 Diagrama C3 - Componentes
*(Pendiente diagrama C3)*

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