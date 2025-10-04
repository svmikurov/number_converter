"""Abstract Base Classes."""

from abc import ABC, abstractmethod

from .types import CaseType, Factor, GenderType


class NumberConverterABC(ABC):
    """The converter of integer to numeral."""

    @abstractmethod
    def get_text(
        self,
        case_number: int,
        gender: GenderType,
        case: CaseType,
    ) -> str:
        """Get the text representation of number."""


class FactorConverterABC(ABC):
    """The converter of number period to numeral."""

    @abstractmethod
    def get_text(
        self,
        number: int,
        case: CaseType,
        factor: Factor,
    ) -> str:
        """Get the number period numeral."""
