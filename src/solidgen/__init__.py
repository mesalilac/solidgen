from solidgen.scaffold import scaffold_template
from solidgen.templates import ComponentTemplate, PageTemplate
import click

from pathlib import Path
from .logger import logger
from .types import ComponentType

BIOME_DISABLE_IMPORT_SORT = (
    "/** biome-ignore-all assist/source/organizeImports: false */\n\n"
)

COMPONENTS_DIR_PATH = Path("src/components")
COMPONENTS_INDEX_FILE_PATH = COMPONENTS_DIR_PATH / "index.ts"

PAGES_DIR_PATH = Path("src/pages")
PAGES_INDEX_FILE_PATH = PAGES_DIR_PATH / "index.ts"


def toPascalCase(s: str) -> str:
    s = s.strip().lower().replace("-", " ").replace("_", " ")

    return "".join(word.capitalize() for word in s.split())


def init_comp(skip_confirm: bool):
    if COMPONENTS_DIR_PATH.exists():
        logger.error(
            f"Initialization: Components directory already exists at '{COMPONENTS_DIR_PATH}'"
        )
        return

    if skip_confirm:
        confirm = True
    else:
        confirm = click.confirm(
            f"Do you want to init components directory '{COMPONENTS_DIR_PATH}'?",
            default=True,
        )

    if not confirm:
        return

    if not COMPONENTS_DIR_PATH.exists():
        logger.success(
            f"Initialization: Creating components directory at '{COMPONENTS_DIR_PATH}'"
        )
        COMPONENTS_DIR_PATH.mkdir(parents=True)

    if not COMPONENTS_INDEX_FILE_PATH.exists():
        logger.success(
            f"Initialization: Creating index file at '{COMPONENTS_INDEX_FILE_PATH}'"
        )
        COMPONENTS_INDEX_FILE_PATH.write_text(
            BIOME_DISABLE_IMPORT_SORT,
            encoding="utf-8",
        )


def init_pages(skip_confirm: bool):
    if PAGES_DIR_PATH.exists():
        logger.error(
            f"Initialization: Pages directory already exists at '{PAGES_DIR_PATH}'"
        )
        return

    if skip_confirm:
        confirm = True
    else:
        confirm = click.confirm(
            f"Do you want to init pages directory '{PAGES_DIR_PATH}'?",
            default=True,
        )
    if not confirm:
        return

    if not PAGES_DIR_PATH.exists():
        logger.success(
            f"Initialization: Creating pages directory at '{PAGES_DIR_PATH}'"
        )
        PAGES_DIR_PATH.mkdir(parents=True)

    if not PAGES_INDEX_FILE_PATH.exists():
        logger.success(
            f"Initialization: Creating index file at '{PAGES_INDEX_FILE_PATH}'"
        )
        PAGES_INDEX_FILE_PATH.write_text(
            BIOME_DISABLE_IMPORT_SORT,
            encoding="utf-8",
        )


@click.group()
def cli():
    pass


@cli.command(help="Initialization components directory")
@click.argument("target", type=click.Choice(["comps", "pages"], case_sensitive=False))
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
def init(target: str, yes: bool):
    if target == "comps":
        init_comp(yes)
    elif target == "pages":
        init_pages(yes)


@cli.command(help="Generate components")
@click.argument("component_name", type=str)
@click.option(
    "--type",
    "-t",
    type=click.Choice(ComponentType),
    default=ComponentType.base,
    help="SolidJS Component Type",
)
@click.option(
    "--dry-run",
    type=bool,
    is_flag=True,
    help="Print generated code without writing to filesystem",
)
def comp(component_name: str, type: ComponentType, dry_run: bool):
    name = toPascalCase(component_name)

    template = ComponentTemplate(name, type)

    scaffold_template(template, COMPONENTS_DIR_PATH, COMPONENTS_INDEX_FILE_PATH)


@cli.command(help="Generate pages")
@click.argument("page_name", type=str)
@click.option(
    "--dry-run",
    type=bool,
    is_flag=True,
    help="Print generated code without writing to filesystem",
)
def page(page_name: str, dry_run: bool):
    name = toPascalCase(page_name)

    template = PageTemplate(name)

    scaffold_template(template, PAGES_DIR_PATH, PAGES_INDEX_FILE_PATH)


if __name__ == "__main__":
    cli()
