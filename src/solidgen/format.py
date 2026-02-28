from solidgen.logger import logger
import subprocess


def format(text: str) -> str:

    p = subprocess.run(
        ["pnpm", "biome", "check", "--write", "--stdin-file-path", "filename.tsx"],
        text=True,
        input=text,
        capture_output=True,
        shell=True,
        encoding="utf-8",
    )

    if p.returncode == 0:
        return p.stdout
    else:
        logger.error(p)
        return text
