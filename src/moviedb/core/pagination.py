"""Framework-agnostic paging primitives shared by repositories and services."""

from dataclasses import dataclass

DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 100


@dataclass(frozen=True, slots=True)
class PageParams:
    """1-based page number and page size requested by a caller."""

    page: int = 1
    size: int = DEFAULT_PAGE_SIZE

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size


@dataclass(frozen=True, slots=True)
class PageResult[T]:
    """One page of items plus the total row count across all pages."""

    items: list[T]
    total: int
    params: PageParams
