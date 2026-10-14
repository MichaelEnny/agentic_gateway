"""Trajectories: what the agent proposed, what each tool returned, and any injected fault."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any


@dataclass
class Step:
    index: int
    tool: str
    args: dict[str, Any]
    output: Any
    clock: float  # seconds since the start of the episode
    # Seen by the gateway, never by the LLM: probability, embedding, group, risk tier.
    hidden: dict[str, Any] = field(default_factory=dict)
    # Tokens the agent spent proposing this step (None for the scripted policy).
    tokens: int | None = None


@dataclass
class Fault:
    kind: str
    step: int  # first step at which a gate could see the fault
    origin_step: int  # step whose output was corrupted first
    context: str = "normal"  # gateway state while this trajectory runs
    effect: float | None = None  # |p_fault - y| - |p_clean - y|; > 0 means the risk got worse
    detail: dict[str, Any] = field(default_factory=dict)


@dataclass
class Trajectory:
    trajectory_id: str
    case_id: str
    patient_id: str
    y: int
    group: str
    seed: int
    policy: str
    steps: list[Step]
    fault: Fault | None = None
    completed: bool = True
    notes: list[str] = field(default_factory=list)

    @property
    def kind(self) -> str:
        return self.fault.kind if self.fault else "clean"

    def first(self, tool: str) -> Step | None:
        return next((s for s in self.steps if s.tool == tool), None)

    def copy(self) -> Trajectory:
        steps = [replace(s, args=dict(s.args), hidden=dict(s.hidden),
                         output=dict(s.output) if isinstance(s.output, dict) else s.output)
                 for s in self.steps]
        return replace(self, steps=steps, notes=list(self.notes))
