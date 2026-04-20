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
            BIOME_DISABLE_IMPORT_SORT, encoding="utf-8", newline="\n"
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
            BIOME_DISABLE_IMPORT_SORT, encoding="utf-8", newline="\n"
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
    "--css",
    "-c",
    type=bool,
    is_flag=True,
    help="Generate CSS file for the component",
)
@click.option(
    "--dir",
    "-d",
    type=click.Path(path_type=Path, dir_okay=True, file_okay=False, writable=True),
    default=".",
    help=f"Subdirectory relative to '{COMPONENTS_DIR_PATH}'",
)
@click.option(
    "--base",
    "-b",
    type=click.Path(path_type=Path, dir_okay=True, file_okay=False, writable=True),
    default=COMPONENTS_DIR_PATH,
    help="Base directory",
)
def comp(component_name: str, type: ComponentType, css: bool, dir: Path, base: Path):
    name = toPascalCase(component_name)

    template = ComponentTemplate(name, type, css)

    base_dir = base / dir

    base_dir.mkdir(parents=True, exist_ok=True)

    scaffold_template(template, css, base_dir, base_dir / "index.ts")


@cli.command(help="Generate pages")
@click.argument("page_name", type=str)
@click.option(
    "--css",
    "-c",
    type=bool,
    is_flag=True,
    help="Generate CSS file for the page",
)
@click.option(
    "--dir",
    "-d",
    type=click.Path(path_type=Path, dir_okay=True, file_okay=False, writable=True),
    default=".",
    help=f"Subdirectory relative to '{PAGES_DIR_PATH}'",
)
@click.option(
    "--base",
    "-b",
    type=click.Path(path_type=Path, dir_okay=True, file_okay=False, writable=True),
    default=PAGES_DIR_PATH,
    help="Base directory",
)
def page(page_name: str, css, dir: Path, base: Path):
    name = toPascalCase(page_name)

    template = PageTemplate(name)

    base_dir = base / dir

    base_dir.mkdir(parents=True, exist_ok=True)

    scaffold_template(template, css, base_dir, base_dir / "index.ts")


if __name__ == "__main__":
    cli()
