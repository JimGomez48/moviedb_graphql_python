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
