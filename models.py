from typing import List, Literal
from pydantic import BaseModel, Field

class Challenge(BaseModel):
    id: str
    title: str
    difficulty: Literal["Beginner","Intermediate"]
    topic: str
    description: str
    symptom: str
    topology: str
    device: str
    hidden_fault: str
    root_cause: str
    expected_evidence: List[str]
    expected_commands: List[str]
    expected_fix_keywords: List[str]
    verification_command: str
    learning_objective: str
    hints: List[str]

class CommandResult(BaseModel):
    command: str
    output: str
    success: bool = True
    changed_state: bool = False

class Attempt(BaseModel):
    diagnosis: str = ""
    evidence: str = ""
    proposed_fix: str = ""
    verified: bool = False

class ScoreBreakdown(BaseModel):
    diagnosis: int = 0
    evidence: int = 0
    fix: int = 0
    verification: int = 0
    efficiency: int = 0
    total: int = 0
    feedback: List[str] = Field(default_factory=list)

class CoachResponse(BaseModel):
    message: str
    next_hint: str
    misconception: str = ""
    encouragement: str = ""
