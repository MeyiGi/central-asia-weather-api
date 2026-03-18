from app.application.variable_specs.builder import VariableSpecBuilder
from app.application.variable_specs.registry import register_builder
 

@register_builder("humidity")
class HumidityBuilder(VariableSpecBuilder):
    def build_name(self) -> None:
        self._name = "humidity"
 
    def build_colormap(self) -> None:
        self._colormap = "YlGnBu"
 
    def build_unit_label(self) -> None:
        self._unit_label = "Specific Humidity (kg/kg)"