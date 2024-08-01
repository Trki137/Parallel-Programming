from dataclasses import dataclass


@dataclass
class TaskResult:
    score: float
    node_id: str

    def __init__(self, score: float, node_id: str):
        self.score = score
        self.node_id = node_id
