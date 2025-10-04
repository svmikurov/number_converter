"""Abstract Base Classes."""

from abc import ABC, abstractmethod

from .types import CaseType, Factor


class NumberConverterABC(ABC):
    """The converter of integer to numeral."""

    @abstractmethod
    def get_text(self, number: int) -> str:
        """Get the text representation of number."""


class PeriodConvertorABC(ABC):
    """The converter of number period to numeral."""

    @abstractmethod
    def get_text(
        self,
        number: int,
        case: CaseType,
        range_name: Factor,
    ) -> str:
        """Get the number period numeral."""
