# NetBreak AI
**Break. Investigate. Fix. Learn.**

NetBreak AI is an interactive network-troubleshooting learning simulator. Learners receive a broken network, investigate it through a Cisco-style CLI, use progressive hints or Gemini coaching, propose a diagnosis and fix, and verify the repair.

## Final MVP
- 30 scenarios: 15 Beginner + 15 Intermediate
- IP/connectivity, VLANs, trunking, routing, interfaces, ACL/security, DHCP, DNS, mixed faults
- Cisco-style simulated CLI
- Deterministic network state and scoring
- Gemini AI coach with local fallback
- Progressive hints
- Investigation path and troubleshooting report

## Run
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your own Gemini key:
```text
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-2.5-flash
```
Never submit `.env` or a real API key.

Run:
```bash
streamlit run app.py
```

The application remains usable without Gemini using local deterministic coaching.
