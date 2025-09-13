# Class for data classes used in the application
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ServiceResponse:
    success: bool
    message: str
    data: Optional[dict] = field(default_factory=dict)
    status_code: int = 400


@dataclass
class RepositoryResponse:
    success: bool
    message: str
    data: Any = None
    error: Optional[str] = None
