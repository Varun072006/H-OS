"""Placeholder unit test for package validation."""

from ai import __version__


def test_package_version() -> None:
    """Ensure package version string is defined."""
    assert __version__ == "0.1.0"
