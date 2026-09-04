import streamlit as st
def inject_css():
    st.markdown('''<style>
    .block-container{max-width:1250px;padding-top:1.4rem}
    .hero{padding:1.15rem 1.4rem;border:1px solid rgba(128,128,128,.25);border-radius:16px;margin-bottom:1rem}
    .hero h1{margin:0;font-size:2.25rem}.hero p{margin:.25rem 0 0;opacity:.72}
    </style>''',unsafe_allow_html=True)
def header():
    st.markdown('<div class="hero"><h1>🌐 NetBreak AI</h1><p><b>Break. Investigate. Fix. Learn.</b> — an AI-guided network troubleshooting lab.</p></div>',unsafe_allow_html=True)
def command_history(history):
    if not history: st.caption("No commands yet. Start by investigating the symptom.")
    for x in history: st.code(f"R1# {x.command}\n{x.output}",language="text")
def score_card(s):
    for col,label,value in zip(st.columns(5),["Diagnosis","Evidence","Fix","Verify","Efficiency"],[s.diagnosis,s.evidence,s.fix,s.verification,s.efficiency]): col.metric(label,str(value))
