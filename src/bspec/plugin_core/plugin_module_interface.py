"""Plugin ModuleInterface, adapted from: https://youtu.be/iCE1bDoit9Q"""
from abc import ABC, abstractstaticmethod


class ModuleInterface(ABC):
    """Represents a plugin interface using ABC.
    a plugin has a single register function."""

    @abstractstaticmethod
    def register() -> None:
        """Register the necessary items in the plugin component or system factory."""
        pass
