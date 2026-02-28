from typing import Protocol, runtime_checkable


@runtime_checkable
class Template(Protocol):
    kind: str
    name: str

    def build(self) -> str: ...
