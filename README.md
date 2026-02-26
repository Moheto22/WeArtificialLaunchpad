# WeArtificial Innovation Launchpad Backend

Este es el backend de la plataforma de innovación, desarrollado con Django, Django Rest Framework, PostgreSQL y Docker.

## Características

- **Autenticación y Roles**: Sistema de usuarios con roles de Administrador y Consumidor.
- **Fases Dinámicas**: Los administradores pueden crear fases de innovación con formularios personalizados.
- **Generador de Prompts (PromptChunks)**: Sistema que intercala fragmentos de texto estáticos con campos dinámicos.
- **Historial de Proyectos**: Los usuarios pueden organizar sus respuestas en proyectos.
- **Trazabilidad**: Registro exhaustivo de actividad (Activity Log).
- **Dockerizado**: Entorno de desarrollo listo con Docker Compose.

## Estructura del Proyecto (Dominio)

El proyecto está organizado por dominios dentro de la carpeta `apps/`:

- `apps/users`: Gestión de usuarios, autenticación y roles.
- `apps/phases`: Definición de fases de innovación, campos de formulario y fragmentos de prompts (`PromptChunks`).
- `apps/projects`: Gestión de proyectos de los usuarios.
- `apps/responses`: Almacenamiento de respuestas y prompts generados.
- `apps/activity`: Registro de actividad y auditoría.
- `apps/core`: Utilidades y modelos base (TimeStampedModel).

## Requisitos

- Docker
- Docker Compose

## Instalación y Despliegue con Docker

Este proyecto está configurado para ejecutarse en contenedores separados para la API (`web`) y la base de datos (`db`).

### 1. Configurar el entorno
Crea un archivo `.env` en la raíz (puedes usar el existente como base) asegurándote de que `DATABASE_HOST=db`.

### 2. Construir y levantar los contenedores
```bash
docker-compose up --build
```
Esto levantará:
- **db**: Base de datos PostgreSQL en el puerto 5432.
- **web**: Servidor de desarrollo Django en el puerto 8000.


### 3. Preparar la base de datos
En una nueva terminal, ejecuta las migraciones:
```bash
docker-compose exec web python manage.py migrate
```

### 4. Crear un superusuario (Administrador)
```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Acceso
- **Backend API**: [http://localhost:8000/api/](http://localhost:8000/api/)
- **Panel de Admin**: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- **Documentación Swagger**: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)

---

## Desarrollo Local (Sin Docker)

Si prefieres trabajar localmente:

1. **Crear entorno virtual**: `python -m venv venv`
2. **Activar**: `source venv/bin/activate` (Mac/Linux) o `venv\Scripts\activate` (Windows)
3. **Instalar dependencias**: `pip install -r requirements.txt`
4. **Ejecutar**: `python manage.py runserver`
