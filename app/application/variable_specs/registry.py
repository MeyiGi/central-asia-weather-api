from app.application.variable_specs.builder import VariableSpecBuilder
from app.application.variable_specs.director import VariableSpecDirector
from app.domain.exceptions import VariableNotFoundError
from app.domain.entities import VariableSpec

_BUILDERS: dict[str, type[VariableSpecBuilder]] = {}

def register_builder(name: str):
    def decorator(cls: type[VariableSpecBuilder]) -> type[VariableSpecBuilder]:
        if name in _BUILDERS:
            raise ValueError(f"Builder '{name}' is already registered")
        
        _BUILDERS[name] = cls
        return cls
    
    return decorator

def get_variable_spec(name: str) -> VariableSpec:
    builder_cls = _BUILDERS.get(name)
    
    if builder_cls is None:
        raise VariableNotFoundError(f"Unknown variable '{name}'. Available: {list(_BUILDERS)}")
    
    builder = builder_cls()
    director = VariableSpecDirector(builder)

    return director.construct()

def all_variable_names() -> list[str]:
    return list(_BUILDERS)