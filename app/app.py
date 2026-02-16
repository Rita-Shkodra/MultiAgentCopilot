import sys
import os
import json
import time
import streamlit as st

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from pipeline import run_copilot

st.set_page_config(
    page_title="SupplyChain Copilot",
    layout="centered"
)

st.title("SupplyChain Copilot")
st.caption("Multi-Agent Evidence-Grounded Enterprise Assistant")

st.markdown("---")

# -------- INPUT AREA --------

task = st.text_area(
    "Business Task",
    placeholder="Analyze transportation cost increases and identify possible causes.",
    height=140
)

col1, col2 = st.columns([1, 4])

with col1:
    run_button = st.button("Run")

st.markdown("---")

# -------- STATE --------

if "result" not in st.session_state:
    st.session_state.result = None
    st.session_state.latency = None

if run_button:

    if not task.strip():
        st.warning("Please enter a task.")
    else:
        start = time.time()

        with st.spinner("Running multi-agent workflow..."):
            result = run_copilot(task)

        latency = round((time.time() - start) * 1000, 2)

        st.session_state.result = result
        st.session_state.latency = latency

# -------- OUTPUT --------

if st.session_state.result:

    result = st.session_state.result

    # Verification
    if result["verification"].startswith("PASS"):

        cleaned = result["draft"].replace("```json", "").replace("```", "").strip()
    parsed = json.loads(cleaned)

    # -------- Copilot Insight --------
    st.markdown("## 🧠 Copilot Insight")

    insight_text = " ".join(
        [item["statement"] for item in parsed.get("executive_summary", [])[:2]]
    )

    st.info(insight_text)

    # -------- Key Drivers --------
    st.markdown("## 🔎 Key Risk Drivers")

    for item in parsed.get("executive_summary", []):
        st.markdown(f"- {item['statement']}")

    # -------- Communication Draft --------
    st.markdown("## ✉ Suggested Client Communication")

    email_preview = "\n\n".join(
        [item["statement"] for item in parsed.get("client_email", [])]
    )

    st.text_area(
        "Draft Email",
        value=email_preview,
        height=200
    )

    # -------- Evidence --------
    with st.expander("📚 View Supporting Evidence"):
        for s in parsed.get("sources", []):
            st.write(s)

    # -------- Trace --------
    with st.expander("⚙ Agent Execution Trace"):
        for step in result["trace"]:
            st.write(f"{step['agent']} → {step['status']} | {step['details']}")
