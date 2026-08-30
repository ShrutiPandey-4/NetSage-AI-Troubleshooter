import pytest
from pydantic import ValidationError
from backend.models.troubleshooting import ReviewInput
def test_review_decisions():
 for decision in ('ACCEPTED','REJECTED'): assert ReviewInput(diagnosis_id=1,decision=decision).decision==decision
def test_edited_requires_correction():
 with pytest.raises(ValidationError): ReviewInput(diagnosis_id=1,decision='EDITED')
