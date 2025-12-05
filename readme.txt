2/12/25
Proyecto: Sistema de gestión de biblioteca + préstamos + analítica

gestionar libros
gestionar lectores
registrar préstamos de libros
manejar disponibilidad
generar estadísticas
tener historial de quién tomó qué
tener roles y permisos
exponer rutas API profesional REST
autenticar usuarios
guardar logs
manejar errores
paginación
seguridad
documentación (Swagger / OpenAPI)


(Semana 1 - Arquitectura)

Tarea1. Setup  
Crear repositorio. ✅
Crear Venv. ✅
Crear requirements  ✅

Crear proyecto en Django. ✅
Crear aplicacion inicial(Users) (Escalabilidad desde el incio.)✅

Tarea2. Modelos, ORM, Shaping. 
Objetivo ? Diseñar modelos de la aplicacion.

Modelos: 
Book, loans y readers. ✅
Poder crear los books, loans y readers desde la GUI de admin junto con un superuser✅

Tarea3. 
Iniciar con Django Rest Framework. ✅
Arrancar entiendo conceptos claves como:
Serializers → ViewSets → Routers → Validaciones → Lógica de negocio.

Serializer: Puente entre el modelo (datos en el BD) y la API (JSON que se dirige al front)

ViewSets: Un viewSet es una vista que DRF llená con logica de CRUD, permitiendo operaciones como:
list → GET /api/books/
retrieve → GET /api/books/1/
create → POST /api/books/
update → PUT /api/books/1/
partial_update → PATCH /api/books/1/
destroy → DELETE /api/books/1/

Router: Un router expone automáticamente las rutas REST sin que tú las crees a mano.
(El router se creo en urls de Users haciendo un include en el proyecto. )

Tarea4. 
Crear el archivo Serializer.py✅
Crear ViewSets✅
crear Urls.py con Routers✅
probar endpoints(Postman)✅

Tarea5. Implementar reglas de negocio (lógica de backend)



Se generaran las reglas propias de la APi, osea, de la capa del backend.
Reglas por implementar : 

Poder consultar los usuarios,libros y prestamos creados✅

Hacer
No permitir prestar un libro si no está disponible
No permitir prestar un libro si ya tiene un préstamo activo
Marcar el libro como unavailable cuando se presta
Marcar el libro como available al devolverlo
No permitir devolver dos veces el mismo préstamo
Validaciones claras + mensajes de error profesionales

