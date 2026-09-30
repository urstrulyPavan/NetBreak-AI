# NetBreak-AI

### **Break. Investigate. Fix. Learn.**

**AI-Guided Network Troubleshooting Lab**

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-NetBreak--AI-brightgreen)](https://netbreak.streamlit.app/)

NetBreak-AI is an interactive network troubleshooting learning simulator that helps learners develop **evidence-driven troubleshooting skills** through realistic network failure scenarios.

Instead of simply providing commands or solutions, NetBreak-AI guides learners through a structured troubleshooting process:

**Observe → Investigate → Isolate → Fix → Verify**

Learners receive a broken network, investigate it using a Cisco-style CLI, collect evidence, identify the root cause, propose a fix, and verify whether the network has been restored.

---

## 🚀 Live Demo

**Try NetBreak-AI:**
https://netbreak.streamlit.app/

---

## ✨ Features

### 🌐 Scenario-Based Troubleshooting

Work through realistic network failures covering:

* IP addressing and connectivity
* VLAN configuration
* Trunking
* Routing
* Interface failures
* ACL and security issues
* DHCP
* DNS
* Mixed network faults

### 💻 Cisco-Style Simulated CLI

Investigate network devices using familiar commands such as:

```text
show ip interface brief
show ip route
show vlan
show interfaces trunk
ping
```

The CLI operates against a **deterministic simulated network state**, allowing learners to investigate failures without requiring physical Cisco equipment.

### 🧠 Gemini AI Coach

The Gemini-powered coach provides context-aware guidance based on the learner's investigation.

It focuses on **reasoning and evidence rather than directly giving away the solution**.

### 💡 Progressive Hints

Learners can request hints progressively:

1. Identify what to investigate
2. Narrow down the affected area
3. Interpret the available evidence
4. Determine the likely root cause

### 📊 Troubleshooting Evaluation

Each investigation is evaluated based on factors such as:

* Diagnosis
* Evidence collected
* Correctness of the proposed fix
* Verification
* Investigation efficiency

A structured troubleshooting report is generated at the end of the scenario.

### 🔄 Local AI Fallback

The application remains usable even when Gemini is unavailable by using deterministic local coaching and scenario logic.

---

## 📦 Final MVP

The current MVP contains:

* **30 network troubleshooting scenarios**

  * 15 Beginner
  * 15 Intermediate
* Multiple networking fault categories
* Cisco-style simulated CLI
* Deterministic network state
* Deterministic scoring
* Gemini AI coaching
* Local fallback coaching
* Progressive hints
* Investigation path tracking
* Troubleshooting reports

---

## 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │       Learner       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Streamlit UI      │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
             Scenario Engine   Simulated CLI   AI Coach
                    │               │               │
                    │               │        ┌──────┴──────┐
                    │               │        │             │
                    │               │        ▼             ▼
                    │               │     Gemini API   Local Fallback
                    │               │
                    └───────────────┼───────────────┐
                                    ▼               │
                             Evaluation Engine      │
                                    │               │
                                    ▼               │
                          Troubleshooting Report ◄──┘
```

---

## 🛠️ Tech Stack

| Technology            | Purpose                                    |
| --------------------- | ------------------------------------------ |
| **Python**            | Core application and troubleshooting logic |
| **Streamlit**         | Interactive web interface                  |
| **Google Gemini API** | AI-powered troubleshooting coaching        |
| **Pydantic**          | Structured scenario and data validation    |
| **Git / GitHub**      | Version control and collaboration          |

---

## 📁 Project Structure

```text
NetBreak-AI/
│
├── app.py
├── requirements.txt
├── .env.example
├── README.md
│
├── scenarios/
│   ├── beginner/
│   └── intermediate/
│
├── engine/
│   ├── scenario_engine.py
│   ├── cli.py
│   ├── troubleshooting.py
│   └── scoring.py
│
├── ai/
│   └── gemini_coach.py
│
└── ...
```

> The exact structure may vary depending on the current implementation.

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/urstrulyPavan/NetBreak-AI.git
cd NetBreak-AI
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini

Copy the example environment file:

```bash
cp .env.example .env
```

On Windows, you can also simply create a `.env` file manually.

Add your Gemini API configuration:

```text
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-2.5-flash
```

**Never commit `.env` or expose your API key publicly.**

### 5. Start the application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## ☁️ Deployment

NetBreak-AI is deployed using **Streamlit Community Cloud**.

### Production Demo

**https://netbreak.streamlit.app/**

The Gemini API key is configured through Streamlit's secret management rather than being stored in the public repository.

---

## 🎯 Troubleshooting Methodology

NetBreak-AI is designed around a structured troubleshooting workflow:

```text
        OBSERVE
           │
           ▼
       INVESTIGATE
           │
           ▼
         ISOLATE
           │
           ▼
           FIX
           │
           ▼
         VERIFY
```

The goal is not to memorize commands.

The goal is to learn **how to reason from network evidence to a root cause**.

---

## 🧪 Example Investigation

A scenario might present a topology such as:

```text
PC1 ─── R1 ═════ R2 ─── Server
```

with a symptom such as:

```text
PC1 cannot reach Server
```

The learner can investigate using commands such as:

```text
show ip interface brief
show ip route
ping
```

The system evaluates the investigation path and determines whether the learner correctly identified and fixed the underlying fault.

---

## 🔐 Security

API credentials should never be committed to GitHub.

Make sure `.env` is included in `.gitignore`:

```text
.env
.venv/
__pycache__/
```

Use `.env.example` to document the required environment variables without exposing secrets.

---

## 📌 Project Status

**Status: MVP Complete**

Current version includes 30 troubleshooting scenarios across beginner and intermediate difficulty levels.

Future improvements may include:

* More advanced scenarios
* Additional Cisco commands
* Larger network topologies
* Multiplayer troubleshooting
* Persistent learner progress
* More detailed analytics
* Additional AI providers
* Docker-based deployment
* AWS deployment

---

## 👨‍💻 Contribution

Contributions, suggestions, and improvements are welcome.

If you find a bug or have an idea for a new troubleshooting scenario, feel free to open an issue or submit a pull request.

---

## 📄 License

Add your preferred open-source license here, such as **MIT License**, if you intend to distribute the project under that license.
