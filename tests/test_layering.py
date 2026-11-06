import ast
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parent.parent / "src" / "moviedb"
FORBIDDEN_PREFIX = "moviedb.core.db"
LAYERS_WITHOUT_DB_ACCESS = ["routes", "core/services", "schemas"]


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text())
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            if node.level == 0:
                modules.add(node.module)
            else:
                # Resolve relative imports against the file's package.
                package = path.relative_to(SRC).parent.parts
                base = package[: len(package) - (node.level - 1)]
                modules.add(".".join(("moviedb", *base, node.module)))
    return modules


@pytest.mark.parametrize("layer", LAYERS_WITHOUT_DB_ACCESS)
def test_layer_does_not_import_db_models(layer: str) -> None:
    # Arrange
    files = sorted((SRC / layer).rglob("*.py"))

    # Act
    offenders = {
        str(file.relative_to(SRC)): sorted(
            m for m in _imported_modules(file) if m.startswith(FORBIDDEN_PREFIX)
        )
        for file in files
    }
    offenders = {file: mods for file, mods in offenders.items() if mods}

    # Assert
    assert offenders == {}


FRAMEWORK_PREFIXES = ("fastapi", "starlette", "strawberry")


# TODO(graphql-migration): core/gql is Strawberry glue and must move out of core.
KNOWN_FRAMEWORK_EXCEPTIONS = {"core/gql"}


def _is_framework(module: str) -> bool:
    return module.split(".")[0].startswith(FRAMEWORK_PREFIXES)


def test_core_does_not_import_web_frameworks() -> None:
    # Arrange
    files = [
        file
        for file in sorted((SRC / "core").rglob("*.py"))
        if file.relative_to(SRC).parent.as_posix() not in KNOWN_FRAMEWORK_EXCEPTIONS
    ]

    # Act
    offenders = {
        str(file.relative_to(SRC)): sorted(
            m for m in _imported_modules(file) if _is_framework(m)
        )
        for file in files
    }
    offenders = {file: mods for file, mods in offenders.items() if mods}

    # Assert
    assert offenders == {}
