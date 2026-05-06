import schemdraw
import schemdraw.elements as elm
import io
import base64
import re
import json
from typing import Optional


CIRCUIT_SYSTEM_PROMPT = """When asked to draw or sketch a circuit, respond with a JSON block in this exact format:

```circuit
{
  "title": "Circuit name",
  "elements": [
    {"type": "resistor", "label": "R1", "value": "10kΩ", "direction": "right"},
    {"type": "capacitor", "label": "C1", "value": "100nF", "direction": "down"},
    {"type": "led", "label": "LED1", "direction": "right"},
    {"type": "wire", "direction": "left"},
    {"type": "ground"},
    {"type": "source", "label": "VCC", "value": "5V", "direction": "up"},
    {"type": "dot"},
    {"type": "line", "direction": "right", "length": 2}
  ]
}
```

Supported element types: resistor, capacitor, inductor, diode, led, zener, transistor_npn, transistor_pnp, source, battery, ground, wire, line, dot, switch, opamp, transformer, antenna, motor, lamp.
Directions: right, left, up, down.
After the circuit block, explain the circuit in detail."""


ELEMENT_MAP = {
    "resistor": elm.Resistor,
    "capacitor": elm.Capacitor,
    "inductor": elm.Inductor,
    "diode": elm.Diode,
    "led": elm.LED,
    "zener": elm.Zener,
    "source": elm.SourceV,
    "battery": elm.Battery,
    "ground": elm.Ground,
    "wire": elm.Line,
    "line": elm.Line,
    "dot": elm.Dot,
    "switch": elm.Switch,
    "antenna": elm.Antenna,
    "lamp": elm.Lamp,
}

DIRECTION_MAP = {
    "right": "right",
    "left": "left",
    "up": "up",
    "down": "down",
}


def parse_circuit_json(text: str) -> Optional[dict]:
    """Extract circuit JSON from assistant response."""
    pattern = r"```circuit\s*([\s\S]*?)```"
    match = re.search(pattern, text)
    if not match:
        return None
    try:
        return json.loads(match.group(1).strip())
    except json.JSONDecodeError:
        return None


def render_circuit_to_svg(circuit_data: dict) -> Optional[str]:
    """Render circuit JSON to SVG string."""
    try:
        with schemdraw.Drawing(show=False) as d:
            d.config(fontsize=12)

            for elem_data in circuit_data.get("elements", []):
                elem_type = elem_data.get("type", "line").lower()
                direction = DIRECTION_MAP.get(elem_data.get("direction", "right"), "right")
                label = elem_data.get("label", "")
                value = elem_data.get("value", "")
                length = elem_data.get("length", None)

                # Build display label
                display_label = label
                if value:
                    display_label = f"{label}\n{value}" if label else value

                elem_class = ELEMENT_MAP.get(elem_type, elm.Line)

                # Build element
                elem_kwargs = {"d": direction}
                if length:
                    elem_kwargs["l"] = float(length)

                element = elem_class(**elem_kwargs)

                if display_label and elem_type not in ("ground", "dot", "wire", "line"):
                    element = element.label(display_label)

                d.add(element)

            # Export to SVG string
            buf = io.StringIO()
            d.save(buf, fmt="svg")
            svg_content = buf.getvalue()
            return svg_content

    except Exception as e:
        print(f"Circuit render error: {e}")
        return None


def extract_and_render_circuit(response_text: str) -> tuple[str, Optional[str]]:
    """
    Parse circuit block from response, render SVG.
    Returns (cleaned_text, svg_string_or_none)
    """
    circuit_data = parse_circuit_json(response_text)
    svg = None

    if circuit_data:
        svg = render_circuit_to_svg(circuit_data)
        # Remove the raw circuit block from the text shown to user
        cleaned = re.sub(r"```circuit[\s\S]*?```", "", response_text).strip()
        return cleaned, svg

    return response_text, None
