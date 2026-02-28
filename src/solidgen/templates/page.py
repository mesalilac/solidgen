from io import StringIO


class PageTemplate:
    def __init__(self, name: str) -> None:
        self.kind = "page"
        self.name = name + "Page"
        self.indent_width = 4
        self.b = StringIO()

    def build(self) -> str:
        self._write_imports()
        self._write_types()
        self._write_component()

        return self.b.getvalue()

    def _w(self, line="", indent=0) -> None:
        self.b.write(" " * self.indent_width * indent + line + "\n")

    def _write_imports(self) -> None:
        self._w("import { useParams } from '@solidjs/router';")
        self._w("import type { Component } from 'solid-js';")
        self._w()
        self._w(f"import styles from './{self.name}.module.css';")
        self._w()

    def _write_types(self) -> None:
        self._w("type Params = {")
        self._w("id: string;", 1)
        self._w("}")
        self._w()

    def _write_component(self) -> None:
        self._w(f"export const {self.name}: Component = () => {{")
        self._w("const params = useParams<Params>();", 1)
        self._w()
        self._w("return <div>", 1)
        self._w(f"{self.name}: {{params.id}}", 2)
        self._w("</div>;", 1)

        self._w("};")
