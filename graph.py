from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph
from llm import explain_topic


class StudyState(TypedDict, total=False):
    syllabus: List[str]
    total_days: int
    hours_per_day: int
    topics: List[str]
    distribution: Dict[str, int]
    plan: List[str]


# -------- Nodes --------

def analyze_syllabus(state: StudyState):
    state["topics"] = state["syllabus"]
    return state


def distribute_days(state: StudyState):
    topics = state["topics"]
    total_days = state["total_days"]

    per_topic_days = max(1, total_days // len(topics))
    state["distribution"] = {
        topic: per_topic_days for topic in topics
    }
    return state


def generate_plan(state: StudyState):
    plan = []
    day = 1

    for topic, days in state["distribution"].items():
        explanation = explain_topic(topic)

        for _ in range(days):
            if day > state["total_days"]:
                break

            plan.append(
                f"### 📅 Day {day}\n"
                f"**Topic:** {topic}\n"
                f"**Study Time:** {state['hours_per_day']} hours\n\n"
                f"📘 **Explanation:**\n{explanation}"
            )
            day += 1

    state["plan"] = plan
    return state


# -------- Build Graph --------

graph = StateGraph(StudyState)

graph.add_node("analyze", analyze_syllabus)
graph.add_node("distribute", distribute_days)
graph.add_node("plan", generate_plan)

graph.set_entry_point("analyze")
graph.add_edge("analyze", "distribute")
graph.add_edge("distribute", "plan")
graph.set_finish_point("plan")

app = graph.compile()
