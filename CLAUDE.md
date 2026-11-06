# Project: Movie DB GraphQL (FastAPI)

## Stack
- Python 3.14+ (modern syntax, type unions like `str | None`)
- FastAPI 0.141+ with `fastapi-pagination`
- GraphQL: Strawberry (`strawberry-graphql[fastapi]`)
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
- Routers (`rest/routes`, `gql`): Strictly HTTP/GraphQL routing, status codes, and input validation. No DB calls.
- Services: Pure business logic shared by REST and GraphQL. They take and return domain models only. No HTTP types, FastAPI dependencies or Pydantic.
- Repositories: Direct SQLAlchemy access through the models in `core/db/models.py`. They are the only place that maps ORM rows to domain models. Sessions are managed here or injected, never opened in routers.
- Domain models: frozen dataclasses in `core/domain/` (`Actor`, `NewActor`, ...) are the transport-agnostic currency of repositories and services. Never hand SQLAlchemy models to routers.
- Transport models: each transport owns its models and its own mapping from domain models. REST uses Pydantic models in `rest/schemas/` (`from_domain()` / `to_domain()`); GraphQL uses hand-written Strawberry types in `gql/types.py` (`from_domain()`). The two transports never import each other.
- `core/` holds all framework-agnostic business logic and domain models (`domain/`, `db/`, `services/`, `repositories/`, `errors.py`, `pagination.py`). It must not import FastAPI, Starlette, Strawberry, fastapi-pagination or Pydantic. Framework adapters live in `rest/`, `gql/`, `main.py` (app wiring) and `dependencies.py`.
- Services, domain models and routers must not import `moviedb.core.db` models directly, and routers must not import repositories (all enforced by `tests/test_layering.py`).
- Dependency Injection: Always use FastAPI's `Depends()` with `Annotated`.
- New code follows this layering. When touching existing routes that query the DB directly, migrate them to the layered structure.

## GraphQL Rules
- Strawberry types are declared by hand in `gql/types.py` and mapped from domain models; never import ORM models or REST schemas in `gql`.
- Prevent N+1 queries: resolve relationships through per-request dataloaders (`gql/loaders.py`) that call batch service methods.
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
