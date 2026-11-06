import ast
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parent.parent / "src" / "moviedb"


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


WEB_FRAMEWORKS = (
    "fastapi",
    "fastapi_pagination",
    "starlette",
    "strawberry",
    "strawberry_sqlalchemy_mapper",
)
TRANSPORT_MODELS = ("pydantic",)
DATABASE = ("sqlalchemy", "moviedb.core.db")

# (directory under src/moviedb, import prefixes it must not use, why)
RULES = [
    (
        "core",
        WEB_FRAMEWORKS + TRANSPORT_MODELS,
        "core is framework-agnostic: no web framework or Pydantic transport models",
    ),
    (
        "core/domain",
        DATABASE,
        "domain models know nothing about persistence",
    ),
    (
        "core/services",
        DATABASE,
        "services reach data only through repositories",
    ),
    (
        "rest",
        ("moviedb.core.db", "moviedb.core.repositories"),
        "routers reach data only through services (wired in dependencies.py)",
    ),
    (
        "gql",
        ("moviedb.core.db", "moviedb.core.repositories"),
        "resolvers reach data only through services (wired in dependencies.py)",
    ),
    (
        "rest",
        ("moviedb.gql",),
        "transports must not depend on each other",
    ),
    (
        "gql",
        ("moviedb.rest",),
        "transports must not depend on each other",
    ),
]


def _matches(module: str, prefix: str) -> bool:
    return module == prefix or module.startswith(f"{prefix}.")


@pytest.mark.parametrize(
    ("layer", "forbidden", "reason"),
    RULES,
    ids=[f"{layer}-must-not-import-{'+'.join(f)}" for layer, f, _ in RULES],
)
def test_layer_respects_import_rules(
    layer: str, forbidden: tuple[str, ...], reason: str
) -> None:
    # Arrange
    files = sorted((SRC / layer).rglob("*.py"))

    # Act
    offenders = {
        str(file.relative_to(SRC)): sorted(
            module
            for module in _imported_modules(file)
            if any(_matches(module, prefix) for prefix in forbidden)
        )
        for file in files
    }
    offenders = {file: modules for file, modules in offenders.items() if modules}

    # Assert
    assert files, f"no files found under {layer}"
    assert offenders == {}, reason
