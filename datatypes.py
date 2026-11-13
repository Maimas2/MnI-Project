from dataclasses import dataclass, field


@dataclass
class OrderedPair:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


@dataclass
class Body:
    name: str = ""
    mass: float = 0.0
    position: OrderedPair = field(default_factory=OrderedPair)
    velocity: OrderedPair = field(default_factory=OrderedPair)
    acceleration: OrderedPair = field(default_factory=OrderedPair)
    radius: float = 0.0
    density: float = 0.0
    red: int = 0
    green: int = 0
    blue: int = 0


@dataclass
class Universe:
    bodies: list[Body] = field(default_factory=list)  
    width: float = 1000.0
    gravitational_constant: float = 6.674e-11
