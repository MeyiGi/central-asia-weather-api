
def register_all_variable_spec_builders() -> None:
    from .temperature_builder import TemperatureBuilder
    from .humidity import HumidityBuilder
    from .precipitation_builder import PrecipitationBuilder
    from .pressure_builder import PressureBuilder
    from .wind_direction_builder import WindDirectionBuilder
    from .wind_speed_builder import WindSpeedBuilder