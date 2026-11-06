# Movie DB GraphQL Python

## Install Dependencies

Ensure [uv package manager](https://docs.astral.sh/uv/getting-started/installation/) is installed in your development environment

```shell
uv sync
```

## Run the app

```shell
uv run fastapi dev
```

REST is served under `/rest` (interactive docs at `/docs`).
GraphQL is served at `/graphql`.

## Architecture

Requests flow from a router or resolver, to a service, to a repository, to db backend.
REST and GraphQL share the same services.

```text
src/moviedb/
  core/              framework-agnostic: domain models, services, repositories, db
  rest/              REST transport: routers (rest/routes/) and Pydantic schemas
  gql/               GraphQL transport: schema, Strawberry types and dataloaders
  main.py            creates the app and registers both transports
  dependencies.py    wires sessions, repositories and services for the routes
```

Each transport maps the domain models returned by services to its own transport models.
The layering rules are enforced by `tests/test_layering.py`.
See [CLAUDE.md](CLAUDE.md) for the full architecture and code rules.

## Format code and run linting

```shell
uv run ruff format ./
```

```shell
uv run ruff check ./
```

## Type check

```shell
uv run ty check
```

## Run unit tests

```shell
uv run pytest
```
