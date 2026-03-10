from solidgen.types import ComponentType
from io import StringIO


class ComponentTemplate:
    def __init__(self, name: str, type: ComponentType) -> None:
        self.kind = "component"
        self.name = name
        self.type = type
        self.indent_width = 4
        self.b = StringIO()

    def _component_type(self) -> str:
        match self.type:
            case ComponentType.void:
                return "VoidComponent"
            case ComponentType.parent:
                return "ParentComponent"
            case _:
                return "Component"

    def build(self) -> str:
        comp_type = self._component_type()
        has_children = self.type != ComponentType.void

        self._write_imports(comp_type, has_children)
        self._write_types(has_children)
        self._write_component(comp_type, has_children)

        return self.b.getvalue()

    def _w(self, line="", indent=0) -> None:
        self.b.write(" " * self.indent_width * indent + line + "\n")

    def _write_imports(self, comp_type: str, has_children: bool) -> None:
        self._w("import type {")
        self._w(f"{comp_type},", 1)
        if has_children:
            self._w("JSX,", 1)
        self._w("} from 'solid-js';")
        self._w()

        self._w(f"import styles from './{self.name}.module.css';")
        self._w()

    def _write_types(self, has_children: bool) -> None:
        self._w("type Props = {")
        self._w("ref?: HTMLDivElement | ((el: HTMLDivElement) => void);", 1)
        if has_children:
            if self.type == ComponentType.parent:
                self._w("children: JSX.Element;", 1)
            else:
                self._w("children?: JSX.Element;", 1)
        self._w("};")
        self._w()

    def _write_component(self, comp_type: str, has_children: bool) -> None:
        self._w(f"export const {self.name}: {comp_type}<Props> = (props) => {{")
        self._w("return (", 1)
        self._w("<div ref={props.ref}>", 2)
        self._w(self.name, 3)
        if has_children:
            self._w("{props.children}", 3)
        self._w("</div>", 2)
        self._w(");", 1)
        self._w("};")
