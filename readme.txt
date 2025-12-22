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

Serializer: Puente entre el modelo (datos en el BD) y la API (JSON que se dirige al front), reglas del negocio(Relaciones entre modelos, lanzar errores, validaciones).

ViewSets: Un viewSet es una vista que DRF llená con logica de CRUD, permitiendo operaciones como:
list → GET /api/books/
retrieve → GET /api/books/1/
create → POST /api/books/
update → PUT /api/books/1/
partial_update → PATCH /api/books/1/
destroy → DELETE /api/books/1/
Solo controla request-response, permisos y ruteo.

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
No permitir prestar un libro si no está disponible✅
No permitir prestar un libro si ya tiene un préstamo activo✅
Marcar el libro como unavailable cuando se presta✅
Marcar el libro como available al devolverlo✅
No permitir devolver dos veces el mismo préstamo✅
Validaciones claras + mensajes de error profesionales✅

Tarea6. 
Vamos a hacer los Serializer Mejorados, haciendo :

BookSerializer con información útil del estado real del libro.✅
ReadSerializer con todos los prestamos de ese lector.✅
LoanSerializer mostrando datos completos del libro y el del lector✅

Tarea7 parte A.
AUTHENTICATION → ¿Quién eres?
AUTHORIZATION → ¿Qué puedes hacer?

Definicion de permisos para el software: 
Reader = Cliente/usuario final que pide los prestamos
Admin = Usuario que puede autenticarse para las API.
Librarian = Usurio que puede administrar los prestamos.

JWT = JSON Web Token es un token que el backend genera para los inicios de Sesion.

Tarea: Implementar Autenticacion + roles + permisos(JWT)
Objetivo:

Proteger la API para que:
Sin autenticación:
No puedes crear, editar, eliminar nada✅

Solo puedes ver libros (GET /books)
Con autenticación + roles:

Admin → controla todo✅
Librarian → presta / devuelve / crea lectores
Reader (modelo aparte) → solo consulta info

Tarea7 Parte B.
Crear permisos personalizados✅
Aplicar permisos por ViewSet✅

¿Por qué NO es buena idea usar permission_classes = [...] fijo en estos ViewSets?

Porque un ViewSet expone múltiples acciones con niveles de riesgo distintos.
Usar permission_classes fijo obliga a aplicar el mismo nivel de acceso a operaciones que 
deberían tener reglas diferentes, rompiendo el principio de menor privilegio y la escalabilidad del sistema.

Tarea8.
Agregar trazabilidad al sistema sin romper:
Modelos✅
Lógica✅
Permisos✅

Auditoría de préstamos (Loan):
Quién creó el préstamo✅
Quién marcó como devuelto✅
Cuándo pasó cada cosa✅

TAREA 9 — Problema N+1
El problema N+1 ocurre cuando:

Hacemos 1 query principal y luego N queries adicionales
para obtener relaciones de esos resultados.

Ejemplo en contexto:
Teniendo este endpoint:

GET /api/loans/ Y se encuentran 100 préstamos.

En el serializer:

loan.book.title
loan.reader.first_name

¿Qué hace Django?
Query para traer loans:    SELECT * FROM loan;
Por cada loan:
SELECT * FROM book WHERE id = X;
SELECT * FROM reader WHERE id = Y;

Resultado:

1 query principal
+100 libros
+100 lectores
= 201 queries 

Si accedes a una FK → usa select_related
Si accedes a ManyToMany / reverse → prefetch_related