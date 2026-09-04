from models import Attempt, Challenge, ScoreBreakdown

def score_attempt(challenge: Challenge, attempt: Attempt, commands):
    d, e, f = attempt.diagnosis.lower(), attempt.evidence.lower(), attempt.proposed_fix.lower()
    diagnosis_ok = any(k.lower() in d for k in challenge.expected_fix_keywords + challenge.expected_evidence)
    evidence_ok = any(k.lower() in e for k in challenge.expected_evidence)
    fix_ok = any(k.lower() in f for k in challenge.expected_fix_keywords)
    diagnosis = 25 if diagnosis_ok else 0
    evidence = 25 if evidence_ok else 0
    fix = 25 if fix_ok else 0
    verification = 15 if attempt.verified else 0
    efficiency = max(0, 10 - max(0, len(commands) - 3))
    total = min(100, diagnosis + evidence + fix + verification + efficiency)
    return ScoreBreakdown(
        diagnosis=diagnosis, evidence=evidence, fix=fix,
        verification=verification, efficiency=efficiency, total=total,
        feedback=[
            "✓ Diagnosis is aligned with the scenario." if diagnosis_ok else "△ Make the diagnosis more specific.",
            "✓ Concrete evidence cited." if evidence_ok else "△ Cite the exact command/output that proves the hypothesis.",
            "✓ Proposed fix matches the expected remediation." if fix_ok else "△ Connect the fix directly to the root cause.",
            "✓ Verification marked complete." if attempt.verified else "△ Verify the network after changing configuration.",
            "⚡ Efficient investigation." if len(commands) <= 3 else "Try narrowing the fault domain earlier."
        ]
    )
