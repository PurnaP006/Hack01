import streamlit as st

st.title("🤖 AI Task Automation Agent")

task = st.text_input("Enter your task:")

if st.button("Run"):
    if "email" in task.lower():
        st.success("📧 Email sent (demo)")
    elif "remind" in task.lower():
        st.success("⏰ Reminder set (demo)")
    else:
        st.write("🤖 Task processed:", task)
