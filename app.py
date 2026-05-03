import json
import os
from datetime import datetime, timedelta

import streamlit as st
from anthropic import Anthropic

st.set_page_config(page_title="Digital Worker Agent", page_icon="🤖", layout="wide")

st.title("🤖 AI Task Automation Agent (Digital Worker)")
st.caption("Automate repetitive digital work: email drafting, scheduling, data formatting, and webhook/tool handoffs.")


@st.cache_resource
def get_client():
    key = st.secrets.get("ANTHROPIC_API_KEY") if hasattr(st, "secrets") else None
    key = key or os.getenv("ANTHROPIC_API_KEY")
    if not key:
        return None
    return Anthropic(api_key=key)


client = get_client()

SYSTEM_PROMPT = """You are an enterprise digital worker that converts user requests into deterministic task plans.
Return STRICT JSON with this schema:
{
  "summary": "short human summary",
  "tasks": [
    {
      "type": "email|schedule|data_entry|integration",
      "title": "task title",
      "details": "clear details",
      "priority": "low|medium|high",
      "payload": {"any": "machine-friendly fields"}
    }
  ]
}
Do not include markdown fences.
"""


DEFAULT_SCENARIO = """Tomorrow send a follow-up email to all interview candidates,
book 30-minute interviews next week between 10am-2pm,
and convert the attached lead sheet into CRM-ready JSON.
Then POST a completion summary to our webhook."""

with st.sidebar:
    st.header("⚙️ Agent Controls")
    model = st.selectbox("Model", ["claude-sonnet-4-20250514"], index=0)
    dry_run = st.toggle("Dry run mode", value=True, help="No external call execution, only simulated outputs")
    webhook_url = st.text_input("Webhook URL (optional)", placeholder="https://example.com/hook")

st.subheader("1) Describe the work")
request = st.text_area("Natural language task request", value=DEFAULT_SCENARIO, height=130)

st.subheader("2) Optional structured data")
raw_data = st.text_area(
    "Paste CSV-ish rows or JSON to process",
    placeholder="name,email,company\nAva,ava@x.com,Orbit\n...",
    height=140,
)


def parse_response(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(text[start : end + 1])
        raise


def mock_execute(task, webhook):
    now = datetime.utcnow()
    t = task.get("type")
    if t == "email":
        return f"Prepared email draft '{task.get('title')}' for review."
    if t == "schedule":
        slot = (now + timedelta(days=2)).strftime("%Y-%m-%d 10:30 UTC")
        return f"Reserved tentative calendar slot: {slot}."
    if t == "data_entry":
        return "Validated rows and generated normalized JSON payload for CRM import."
    if t == "integration":
        if webhook:
            return f"Would POST payload to {webhook} (dry-run={dry_run})."
        return "Integration task ready; no webhook URL provided."
    return "Task simulated."


def fallback_plan(user_request: str):
    return {
        "summary": "Fallback plan generated locally because no model key/valid response was available.",
        "tasks": [
            {
                "type": "email",
                "title": "Draft follow-up email",
                "details": user_request,
                "priority": "high",
                "payload": {"channel": "email"},
            },
            {
                "type": "schedule",
                "title": "Create scheduling proposal",
                "details": "Prepare available interview slots and invite links.",
                "priority": "medium",
                "payload": {"duration_minutes": 30},
            },
        ],
    }


if st.button("🚀 Run Digital Worker", use_container_width=True):
    if not request.strip():
        st.warning("Please provide a task request.")
        st.stop()

    with st.spinner("Planning tasks..."):
        plan = None
        if client:
            user_payload = {
                "request": request,
                "data": raw_data,
                "constraints": {"dry_run": dry_run, "utc_now": datetime.utcnow().isoformat()},
            }
            try:
                msg = client.messages.create(
                    model=model,
                    max_tokens=1400,
                    system=SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": json.dumps(user_payload)}],
                )
                plan = parse_response(msg.content[0].text)
            except Exception as e:
                st.warning(f"Model response failed, using fallback plan. Details: {e}")

        if not plan:
            plan = fallback_plan(request)

    st.success("Task plan created.")
    st.markdown("### 🧠 Agent Summary")
    st.write(plan.get("summary", "No summary"))

    st.markdown("### 📋 Planned Tasks")
    tasks = plan.get("tasks", [])
    for idx, task in enumerate(tasks, start=1):
        with st.expander(f"{idx}. [{task.get('type','task')}] {task.get('title','Untitled')}"):
            st.write(f"**Priority:** {task.get('priority', 'medium')}")
            st.write(task.get("details", ""))
            st.code(json.dumps(task.get("payload", {}), indent=2), language="json")

    st.markdown("### ⚡ Execution Log")
    logs = []
    for task in tasks:
        logs.append({"task": task.get("title", "Untitled"), "result": mock_execute(task, webhook_url)})

    st.dataframe(logs, use_container_width=True)

    artifact = {"plan": plan, "logs": logs, "generated_at": datetime.utcnow().isoformat()}
    st.download_button(
        "⬇️ Download run artifact (JSON)",
        data=json.dumps(artifact, indent=2),
        file_name="digital_worker_run.json",
        mime="application/json",
        use_container_width=True,
    )

st.divider()
st.caption("Tip: connect real APIs (Gmail, Calendar, Airtable, Slack, CRM) by replacing `mock_execute` with authenticated clients.")
