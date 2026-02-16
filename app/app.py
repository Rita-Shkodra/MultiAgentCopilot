import sys
import os
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



st.markdown("### Business Task")

with st.form("task_form", clear_on_submit=False):

    task = st.text_area(
        "",
        placeholder="Example: Evaluate fuel price exposure risk in air transportation.",
        height=120
    )

    col1, col2 = st.columns([4, 1])

    with col2:
        run_button = st.form_submit_button("Run Analysis")


st.markdown("---")



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



if st.session_state.result:

    result = st.session_state.result
    draft_text = result.get("draft", "")

    verification = result.get("verification", "")

    if verification.startswith("PASS"):
        st.success("Verification: PASS")
    else:
        st.error("Verification Failed – Unsupported Claims Detected")
        st.warning(verification)
        st.stop() 


    st.markdown("---")

    st.markdown("## Executive Summary")

    if "executive summary" in draft_text.lower():
        start = draft_text.lower().index("executive summary")
        section = draft_text[start:]

        if "client email" in section.lower():
            end = section.lower().index("client email")
            section = section[:end]

        if ":" in section:
            section = section.split(":", 1)[1]

        st.write(section.strip())
    else:
        st.write("Not available.")

    st.markdown("## Client Email")

    if "client email" in draft_text.lower():
        start = draft_text.lower().index("client email")
        section = draft_text[start:]

        if "action list" in section.lower():
            end = section.lower().index("action list")
            section = section[:end]

        if ":" in section:
            section = section.split(":", 1)[1]

        st.write(section.strip())
    else:
        st.write("Not available.")

    st.markdown("## Action List")

    if "action list" in draft_text.lower():
        start = draft_text.lower().index("action list")
        section = draft_text[start:]

        if "sources" in section.lower():
            end = section.lower().index("sources")
            section = section[:end]

        if ":" in section:
            section = section.split(":", 1)[1]

        clean_action = section.strip()

        if not clean_action:
            st.write("No documented action identified in retrieved evidence.")
        else:
            st.write(clean_action)
    else:
        st.write("No documented action identified in retrieved evidence.")

       
    st.markdown("## Sources")

    if "sources" in draft_text.lower():
        start = draft_text.lower().index("sources")
        section = draft_text[start:]

        if ":" in section:
            section = section.split(":", 1)[1]

        sources = [line.strip() for line in section.splitlines() if line.strip()]

        if not sources:
            st.write("No sources found.")
        else:
            for src in sources:
                st.markdown(
                    f"""
<div style="
    padding:10px 14px;
    border-radius:8px;
    background-color:#1f2937;  /* darker */
    border:1px solid #111827;
    margin-bottom:8px;
    font-family:monospace;
    font-size:13px;
    color:#e5e7eb;
">
{src}
</div>
""",
                    unsafe_allow_html=True
                )
    else:
        st.write("No sources found.")

    with st.expander("Agent Execution Trace"):
        for step in result.get("trace", []):
            st.write(
                f"{step.get('agent')} → {step.get('status')} | {step.get('details')} | {step.get('latency_ms', 0)} ms"
            )

    st.markdown("## Observability")

    trace = result.get("trace", [])

    if trace:
        rows = []
        total_latency = 0
        total_tokens = 0

        for t in trace:
            latency = t.get("latency_ms", 0)
            tokens = t.get("total_tokens", 0)

            total_latency += latency
            total_tokens += tokens

            rows.append({
                "Agent": t.get("agent"),
                "Status": t.get("status"),
                "Latency (ms)": latency,
                "Total Tokens": tokens
            })

        st.table(rows)

        st.markdown("---")
        st.caption(f"Total Agent Time: {round(total_latency, 2)} ms")
        st.caption(f"Total Tokens Used: {total_tokens}")
        st.caption(f"Errors: {result.get('metrics', {}).get('errors', 0)}")
    else:
        st.write("No observability data available.")
