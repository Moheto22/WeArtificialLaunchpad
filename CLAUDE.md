# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development with Docker (primary workflow)
```bash
docker-compose up --build          # Start all services
docker-compose up                  # Start without rebuilding
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell
```

### Local development (without Docker)
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Testing
```bash
python manage.py test              # Run all tests
python manage.py test apps.users   # Run tests for a specific app
```

### Database
```bash
python manage.py makemigrations <app_name>
python manage.py migrate
```

## Architecture

Django 5.0.2 monolith with domain-driven structure. Six domain apps under `apps/`, each self-contained with models, serializers, views, and URLs.

### Domain Apps (`apps/`)

- **`core/`** — Abstract `TimeStampedModel` (provides `created_at`, `updated_at`) used as base by all other models
- **`users/`** — Custom `User` model (extends `AbstractUser`) with `name`, `surname`, `company`, roles (`is_administrator`, `is_consumer`), and soft-delete (`deleted_at`)
- **`phases/`** — `InnovationPhase`, `PhaseField` (dynamic form fields), `PromptChunk` (static text fragments). Contains `utils.py` with `generate_prompt()` — the core algorithm
- **`projects/`** — `Project` model owned by a user; container for phase responses
- **`responses/`** — `PhaseResponse` stores form input (`form_data` JSON) and the resulting AI prompt (`generated_prompt`)
- **`activity/`** — Read-only `ActivityLog` with audit trail for `CREATE_PROJECT` and `GENERATE_PROMPT` actions

### Key Algorithm: Prompt Generation (`apps/phases/utils.py`)

`generate_prompt(phase, form_data)` interleaves `PromptChunk` objects with `PhaseField` values in order-based fashion: `Chunk[0] + Field[0] value + Chunk[1] + Field[1] value + ...`. Optional chunks are skipped if their corresponding field is empty.

### URL Structure

All API endpoints under `/api/`:
- `/api/users/`, `/api/phases/`, `/api/projects/`, `/api/responses/`, `/api/activity/`
- `/api/docs/` — Swagger UI (drf-spectacular)
- `/api/redoc/` — ReDoc
- `/admin/` — Django admin panel

### Authentication & Authorization

- **Auth:** `SessionAuthentication` + `BasicAuthentication` (no JWT/tokens)
- **Default:** All endpoints require `IsAuthenticated`
- **Roles:** `is_administrator` (manage phases, view all activity) vs `is_consumer` (own projects/responses only)
- Custom `IsAdministrator` permission class used for admin-only viewsets

### Patterns

- **ViewSets use `DefaultRouter`** — CRUD routes auto-generated
- **Activity logging** — Manual `ActivityLog.objects.create()` inside `perform_create()` / `create()` methods in ProjectViewSet and PhaseResponseViewSet; includes `ip_address` from `request.META.get('REMOTE_ADDR')`
- **Hidden user injection** — `serializers.HiddenField(default=serializers.CurrentUserDefault())` used in ProjectSerializer to auto-assign current user
- **Queryset filtering** — ViewSets filter by `request.user` ownership before returning data

### Configuration

- Settings: `config/settings.py` (env vars via `.env` + `python-dotenv`)
- `CORS_ALLOW_ALL_ORIGINS = True` — must change for production
- Custom user model: `AUTH_USER_MODEL = 'users.User'`
- API title: "Innovation Platform API" v1.0.0
