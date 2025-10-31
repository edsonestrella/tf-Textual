"""tf-textual - A practical TUI for Terraform operations."""

__version__ = "0.1.0"
__author__ = "Edson Estrella and Claude from Anthropic"
__email__ = "edson.estrella@gmail.com"

from .app import TFTextualApp, main

__all__ = ["TFTextualApp", "main"]