from app.application.variable_specs.builder import VariableSpecBuilder
from app.application.variable_specs.registry import register_builder


@register_builder("wind_direction")
class WindDirectionBuilder(VariableSpecBuilder):
    def build_name(self) -> None:
        self._name = "wind_direction"

    def build_colormap(self) -> None:
        self._colormap = "hsv"

    def build_unit_label(self) -> None:
        self._unit_label = "Wind Direction (°)"