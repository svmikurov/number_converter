"""Mapping of number with it text representation."""

from .types import Case, Gender

simple_numbers: dict[int, Case] = {
    1: Case(
        Gender('один', 'одна', 'одно'),
        Gender('одного', 'одной', 'одного'),
        Gender('одному', 'одной', 'одному'),
        Gender('один', 'одну', 'одно'),
        Gender('одним', 'одной', 'одним'),
        Gender('одном', 'одной', 'одном'),
    )
}
