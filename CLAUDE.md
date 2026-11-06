# Project: Movie DB GraphQL (FastAPI)

## Stack
- Python 3.14+ (modern syntax, type unions like `str | None`)
- FastAPI 0.141+ with `fastapi-pagination`
- GraphQL: Strawberry (`strawberry-graphql[fastapi]`, `strawberry-sqlalchemy-mapper`)
- Package Manager: uv (Use `uv add` and `uv run`)
- Linters/Formatters: Ruff (Run `uv run ruff check ./` and `uv run ruff format ./`)
- Type Checker: ty (Run `uv run ty check`)
- Database: SQLite via SQLAlchemy 2.0 (`src/moviedb/core/db/`)

## Commands
- Run Server: See README.md
- Test Suite: See README.md
- Lint & Format: See README.md
- Type Check: See README.md

## Architecture & Layers
- Layout: Router -> Service -> Repository
- Routers (`routes/rest`, `routes/gql`): Strictly HTTP/GraphQL routing, status codes, and input validation. No DB calls.
- Services: Pure business logic. No HTTP types or FastAPI dependencies.
- Repositories: Direct SQLAlchemy access through the models in `core/db/models.py`. Sessions are managed here or injected, never opened in routers.
- Schemas: Pydantic models in `schemas/` are the transport layer. Repositories and services hand back schemas or plain data, never SQLAlchemy models, to routers.
- `core/` holds all framework-agnostic business logic and domain models (`db/`, `services/`, `repositories/`, `errors.py`, `pagination.py`). It must not import FastAPI, Starlette, Strawberry or fastapi-pagination (enforced by a layering test). Framework adapters live in `routes/` and `dependencies.py`.
- Services and routers must not import `moviedb.core.db` models directly (enforce with a layering test).
- Dependency Injection: Always use FastAPI's `Depends()` with `Annotated`.
- New code follows this layering. When touching existing routes that query the DB directly, migrate them to the layered structure.

## GraphQL Rules
- Derive Strawberry types from SQLAlchemy models with `strawberry-sqlalchemy-mapper` where possible; do not hand-duplicate fields.
- Prevent N+1 queries: use dataloaders or eager loading (`selectinload`/`joinedload`) for relationships.
- GraphQL resolvers call services, same as REST routers.

## Code Rules
- Use `Annotated` types for all router dependencies and parameters.
- Explicitly declare `response_model` or return types for all endpoints.
- No `Any` types allowed without a justifying comment.
- No `print()` statements in production. Use a structured logger (e.g., Loguru).
- Never use mutable default arguments (e.g., `def f(items=[])`).
- Ruff and ty must pass cleanly before work is considered done.

## Generated Files
- Never hand-edit `uv.lock`; change dependencies with `uv add` / `uv remove`.
- Never hand-edit or commit the SQLite database file (`core/db/moviedb.sqlite`). Change data through `seed.py` or migrations code.

## Testing Guidelines
- Use Test-Driven Development (TDD): Write a failing test before writing the code.
- Frame tests using the AAA pattern (Arrange, Act, Assert).
- Stack: `pytest` + `pytest-asyncio` (require `@pytest.mark.asyncio` or asyncio-mode set to auto).
- Tests live in `tests/`, mirroring the `src/moviedb` layout.
- Keep test databases completely separate: use an in-memory (or temp-file) SQLite database created per test; never point tests at `moviedb.sqlite`.
