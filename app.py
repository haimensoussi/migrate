import streamlit as st
from orchestrator import HorizonOrchestrator

st.set_page_config(page_title="HORIZON — Databricks", page_icon="🤖")
st.title("HORIZON — Assistant migré")
st.caption("CallLLM • Databricks Apps • Model Serving")

@st.cache_resource
def get_orchestrator():
    return HorizonOrchestrator()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Posez votre question")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    try:
        with st.spinner("Génération en cours…"):
            answer = get_orchestrator().run(st.session_state.messages)
    except Exception:
        st.error("Échec de l'appel au modèle. Vérifiez les logs, l'endpoint et les permissions.")
    else:
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.write(answer)
