# 📦 Inventory System (Prueba Técnica)

Este proyecto implementa un sistema de **gestión de inventario** con un backend en **FastAPI** y un frontend en **React (Vite + TypeScript + Tailwind CSS)**.  
Incluye autenticación con **JWT Bearer**, control de roles (**admin / user**), CRUD completo de productos, búsqueda, filtrado, ordenamiento y dockerización con PostgreSQL.

Por Jairo Adolfo Céspedes Plata

La documentación interactiva del backend está disponible en:
- **Swagger UI:** `http://localhost:8000/docs`

La documentación técnica se encuentra en el pdf **SistemaInventario_Documentacion.pdf**
---

## 📦 Requisitos Previos

Asegúrate de tener instalado:

- **Docker** y **Docker Compose**
- **Git**

---

## 🚀 Ejecución del Proyecto

### 1. Clonar el repositorio
    git clone https://github.com/jacespedes2019/Inventory-System.git
    cd inventory-system

### 2. Construir y levantar los servicios con Docker
    docker-compose up --build
En la carpeta base

### Registro y Roles de Usuario

⚠️ No existen usuarios pre-creados.
Cada usuario debe registrarse en /auth/register indicando su correo, contraseña y el rol que tendrá (user o admin).
	•	Rol user:
	•	Puede iniciar sesión y autenticarse con JWT.
	•	Puede consultar productos (listar, buscar, filtrar, ordenar).
	•	No tiene permisos para crear, editar ni eliminar productos.
	•	Rol admin:
	•	Tiene todas las capacidades de un usuario normal.
	•	Además, puede crear, actualizar y eliminar productos.
	•	Puede gestionar completamente el inventario.

### 🖥️ Cómo probar la funcionalidad

1. Acceder al frontend

Ir a http://localhost:5173 en tu navegador.

2. Autenticación
	•	Registrarse en la pantalla de login seleccionando un rol.
	•	Iniciar sesión con el correo y contraseña registrados.
	•	El sistema guardará el token JWT en el navegador.

3. Dashboard de Inventario
	•	Ver tabla de productos con nombre, descripción, precio, cantidad e imagen.
	•	Funcionalidades avanzadas:
	•	Búsqueda por nombre.
	•	Filtrado por precio mínimo/máximo y por existencia de imagen.
	•	Ordenamiento por nombre, precio, cantidad o fecha.
	•	Paginación automática cuando hay más de 5 productos.

4. CRUD de Productos
	•	Crear productos (solo admin).
	•	Editar productos (solo admin).
	•	Eliminar productos (solo admin).
	•	Ver detalle de un producto en modal (todos los roles).

###  Endpoints principales del backend
	•	POST /auth/register → Registrar usuario (admin o user).
	•	POST /auth/login → Iniciar sesión, retorna JWT.
	•	GET /products → Listar productos (con búsqueda, filtro y orden).
	•	POST /products → Crear producto (solo admin).
	•	GET /products/{id} → Ver producto por ID.
	•	PUT /products/{id} → Actualizar producto (solo admin).
	•	DELETE /products/{id} → Eliminar producto (solo admin).

### Patrones y buenas prácticas aplicadas
	•	Backend:
	•	Patrón Repository para acceso a datos.
	•	Capa de Servicios para lógica de negocio.
	•	DTOs con Pydantic para validación robusta.
	•	Autenticación con JWT Bearer y RBAC.
	•	Pruebas automatizadas con PyTest.
	•	Cumplimiento de PEP8.
	•	Frontend:
	•	Manejo de estado con Zustand.
	•	Formularios y validación con react-hook-form + zod.
	•	Diseño responsivo con Tailwind CSS.
	•	Patrón Repository en frontend (auth.repo.ts, products.repo.ts) para desacoplar lógica de API.
	•	Paginación y modales para CRUD de productos.
	•	Infraestructura:
	•	Dockerización completa (backend, frontend, db).
	•	Proxy con Nginx para enrutar /api al backend.
	•	Base de datos PostgreSQL con healthcheck.
 
 ### Notas finales
	•	La documentación completa se encuentra en el documento Word adjunto.
	•	El sistema ya incluye autenticación JWT con roles, validación de inputs y arquitectura modular.
	•	Preparado para extenderse con migraciones (Alembic), CI/CD y almacenamiento de imágenes en la nube.
