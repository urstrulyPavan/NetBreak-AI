from config import GEMINI_API_KEY, GEMINI_MODEL
from models import CoachResponse

def local_coach(challenge, student_message, command_history, hints_used):
    hint = challenge.hints[min(hints_used, len(challenge.hints)-1)]
    misconception = ""
    if "dns" in student_message.lower() and challenge.topic not in ("DNS","Mixed"):
        misconception = "Do not jump to DNS before proving lower-layer connectivity."
    return CoachResponse(
        message="Build a hypothesis from evidence before changing configuration. Narrow the fault domain step by step.",
        next_hint=hint,
        misconception=misconception,
        encouragement="Observe → isolate → fix → verify."
    )

def get_coaching(challenge, student_message, command_history, transcript, hints_used):
    if not GEMINI_API_KEY:
        return local_coach(challenge, student_message, command_history, hints_used)
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt = f'''You are NetBreak AI, a patient Cisco/network troubleshooting instructor.
Coach without immediately revealing the hidden fault. Use only supplied scenario and CLI output.
Do not invent output. Encourage layered troubleshooting.

Scenario: {challenge.title}
Difficulty: {challenge.difficulty}
Topic: {challenge.topic}
Symptom: {challenge.symptom}
Learning objective: {challenge.learning_objective}
Expected evidence: {challenge.expected_evidence}
Commands used: {command_history}
CLI transcript:
{transcript}
Student message: {student_message}
Hints already used: {hints_used}

Return concise JSON fields: message, next_hint, misconception, encouragement.
'''
        response = client.models.generate_content(
            model=GEMINI_MODEL, contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=CoachResponse,
                temperature=0.2,
            )
        )
        return CoachResponse.model_validate_json(response.text)
    except Exception:
        return local_coach(challenge, student_message, command_history, hints_used)
