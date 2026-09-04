import streamlit as st
from ai.gemini_coach import get_coaching
from core.challenge_engine import load_challenges
from core.scoring import score_attempt
from core.session import ensure_session, simulator, start_challenge
from models import Attempt
from ui.components import header, inject_css, command_history, score_card

st.set_page_config(page_title="NetBreak AI", page_icon="🌐", layout="wide")
inject_css(); ensure_session(); header()
challenges=load_challenges(); current=st.session_state.challenge; sim=simulator()

with st.sidebar:
    st.markdown("## 🎯 Challenges")
    group=[c for c in challenges if c.difficulty==current.difficulty]
    selected=st.selectbox("Difficulty",["Beginner","Intermediate"],index=0 if current.difficulty=="Beginner" else 1)
    group=[c for c in challenges if c.difficulty==selected]
    choice=st.selectbox("Scenario",[c.id for c in group],format_func=lambda x: next(c.title for c in group if c.id==x))
    if st.button("Start challenge",use_container_width=True,type="primary"):
        start_challenge(choice); st.rerun()
    st.divider()
    st.metric("Commands",len(sim.history)); st.metric("Hints",st.session_state.hints_used)
    st.caption("30 scenarios • 15 Beginner • 15 Intermediate")

st.markdown(f"### {current.title}")
st.caption(f"{current.difficulty}  •  {current.topic}  •  Device: {current.device}")

a,b=st.columns([1,1.35])
with a:
    st.markdown("#### 🧩 Mission"); st.info(current.symptom)
    st.markdown("**Topology**"); st.code(current.topology)
    st.markdown("**Learning objective**"); st.write(current.learning_objective)
with b:
    st.markdown("#### 💻 Cisco-style CLI")
    with st.form("cli",clear_on_submit=True):
        cmd=st.text_input("Enter a command",placeholder="show ip route")
        run=st.form_submit_button("Run command",use_container_width=True)
    if run and cmd.strip():
        r=sim.run(cmd)
        if r.changed_state: st.success(r.output)
    command_history(sim.history)

st.divider(); st.markdown("### 🤖 AI Coach")
x,y=st.columns([3,1])
with x: msg=st.text_input("Your hypothesis",placeholder="I think the problem is...")
with y: hint=st.button("💡 Progressive hint",use_container_width=True)
if hint:
    i=st.session_state.hint_index
    if i<len(current.hints):
        st.info(current.hints[i]); st.session_state.hints_used+=1; st.session_state.hint_index+=1
    else: st.warning("All progressive hints used.")
if msg and st.button("Ask AI Coach"):
    transcript="\n\n".join(f"R1# {r.command}\n{r.output}" for r in sim.history[-10:])
    st.session_state.coach=get_coaching(current,msg,[r.command for r in sim.history],transcript,st.session_state.hints_used)
if st.session_state.coach:
    r=st.session_state.coach; st.write(r.message); st.info("Next step: "+r.next_hint)
    if r.misconception: st.warning(r.misconception)
    st.success(r.encouragement)

st.divider(); st.markdown("### 🧠 Your Diagnosis")
with st.form("reasoning"):
    diagnosis=st.text_area("1. What is wrong?")
    evidence=st.text_area("2. What proves it?")
    fix=st.text_area("3. What would you change?")
    verified=st.checkbox("4. I verified the fix.")
    submit=st.form_submit_button("Submit troubleshooting report",type="primary",use_container_width=True)
if submit:
    st.session_state.last_score=score_attempt(current,Attempt(diagnosis=diagnosis,evidence=evidence,proposed_fix=fix,verified=verified),[r.command for r in sim.history])

if st.session_state.last_score:
    s=st.session_state.last_score
    st.divider(); st.markdown("### 🏁 Troubleshooting Report"); score_card(s)
    st.progress(s.total/100,text=f"Overall score: {s.total}/100")
    for f in s.feedback: st.write(f)
    with st.expander("🔎 Investigation path",expanded=True):
        for i,r in enumerate(sim.history,1): st.write(f"**{i}.** `{r.command}`")
    if s.total>=85: st.success("Excellent troubleshooting. You isolated and verified the fix.")
    elif s.total>=60: st.info("Good attempt. Strengthen evidence and efficiency.")
    else: st.warning("Keep investigating and use the CLI evidence.")
