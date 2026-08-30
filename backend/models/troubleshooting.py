from pydantic import BaseModel, Field, model_validator
from typing import Literal

class TroubleshootInput(BaseModel):
    case_id: str | None = None
    symptom: str = Field(min_length=3)
    topology_notes: str = ""
    show_outputs: str = ""

class RuleFinding(BaseModel):
    rule: str
    status: Literal['PASS', 'FAIL', 'INSUFFICIENT_EVIDENCE']
    severity: str
    evidence: str
    message: str

class Diagnosis(BaseModel):
    root_cause: str
    confidence: float = Field(ge=0, le=1)
    osi_layer: str
    evidence: list[str]
    next_command: str
    fix_steps: list[str]
    mode: Literal['LLM', 'DEMO_FALLBACK'] = 'DEMO_FALLBACK'

class ReviewInput(BaseModel):
    diagnosis_id: int
    decision: Literal['ACCEPTED', 'EDITED', 'REJECTED']
    correction: Diagnosis | None = None
    @model_validator(mode='after')
    def edited_requires_correction(self):
        if self.decision == 'EDITED' and self.correction is None:
            raise ValueError('An edited review requires a corrected diagnosis')
        return self

class VerificationInput(BaseModel):
    diagnosis_id: int
    status: Literal['Fixed', 'Not Fixed', 'Needs More Investigation']
    note: str = ''
