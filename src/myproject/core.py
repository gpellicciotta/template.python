"""Provide the greeting logic used by the CLI and package API."""


def greet(name: str) -> str:
    """Return a greeting for name."""
    return f"Hello, {name}"
