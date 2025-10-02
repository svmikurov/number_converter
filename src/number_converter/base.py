"""Abstract Base Classes."""

from abc import ABC, abstractmethod


class NumberConverterABC(ABC):
    """The converter of integer to numeral."""

    @abstractmethod
    def get_text(self, number: int) -> str:
        """Get the text representation of number."""
