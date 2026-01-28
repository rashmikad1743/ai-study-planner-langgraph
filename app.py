import streamlit as st
from graph import app

st.set_page_config(page_title="AI Study Planner", page_icon="📘")
st.title("📘 AI Study Planner (LangGraph + Groq)")

st.markdown(
    "Generate a **personalized study plan** using **Agentic AI (LangGraph)** "
    "and **Groq LLaMA-3**."
)

syllabus_input = st.text_area(
    "✍️ Enter syllabus topics (one per line)",
    height=150
)

total_days = st.number_input(
    "📅 Total available study days",
    min_value=1,
    value=7
)

hours_per_day = st.number_input(
    "⏱ Hours per day",
    min_value=1,
    value=3
)

if st.button("🚀 Generate Study Plan"):
    syllabus = [s.strip() for s in syllabus_input.split("\n") if s.strip()]

    if not syllabus:
        st.warning("Please enter at least one syllabus topic.")
    else:
        with st.spinner("Generating your AI-powered study plan..."):
            result = app.invoke({
                "syllabus": syllabus,
                "total_days": total_days,
                "hours_per_day": hours_per_day
            })

        st.success("Study plan generated successfully!")

        for day_plan in result["plan"]:
            st.markdown(day_plan)
            st.divider()
