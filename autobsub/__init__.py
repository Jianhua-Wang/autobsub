"""Top-level package for autobsub."""

import logging

from autobsub.autobsub import LSFPool
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.WARNING,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, show_path=False)],
)
__author__ = """Jianhua Wang"""
__email__ = "jianhua.mert@gmail.com"
__version__ = "0.0.1"
