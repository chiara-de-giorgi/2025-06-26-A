from dataclasses import dataclass

from model.circuit import Circuit


@dataclass
class Arco:
    c1: Circuit
    c2: Circuit
    peso: int