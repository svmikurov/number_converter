"""Abstract Base Classes."""

from abc import ABC, abstractmethod

from .types import CaseType


class NumberConverterABC(ABC):
    """The converter of integer to numeral."""

    @abstractmethod
    def get_text(self, number: int) -> str:
        """Get the text representation of number."""


class PeriodConvertorABC(ABC):
    """The converter of number period to numeral."""

    @abstractmethod
    def get_text(self, number: int, case: CaseType) -> str:
        """Get the number period numeral."""
