from solidgen.logger import logger
from solidgen.templates import Template
from solidgen.format import format

from pathlib import Path

BIOME_DISABLE_IMPORT_SORT = (
    "/** biome-ignore-all assist/source/organizeImports: false */\n\n"
)


def scaffold_template(
    template: Template,
    base_dir: Path,
    root_index_path: Path,
) -> None:
    assert isinstance(template, Template)

    kind = template.kind
    name = template.name
    content = format(template.build())
    scaffold_dir = base_dir / name

    if scaffold_dir.exists():
        logger.error(f"{kind} already exists '{scaffold_dir}'")
        return

    scaffold_dir.mkdir(parents=True)

    (scaffold_dir / f"{name}.module.css").touch()
    (scaffold_dir / f"{name}.tsx").write_text(content, encoding="utf-8")

    local_index_path = scaffold_dir / "index.ts"
    local_index_path.write_text(
        BIOME_DISABLE_IMPORT_SORT + f"export * from './{name}';\n", encoding="utf-8"
    )

    with open(root_index_path, "a", encoding="utf-8") as f:
        f.write(f"export * from './{name}';\n")

    logger.success(f"Created {kind} '{scaffold_dir}'")
