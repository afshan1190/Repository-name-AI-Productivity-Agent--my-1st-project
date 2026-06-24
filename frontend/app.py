import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Productivity Agent",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI Productivity Agent")

menu = st.sidebar.selectbox(
    "Navigation",
    ["Register", "Login", "Tasks"]
)

# ==========================
# REGISTER
# ==========================

if menu == "Register":

    st.header("Create Account")

    username = st.text_input(
        "Username",
        key="register_username"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="register_password"
    )

    if st.button("Register"):

        response = requests.post(
            f"{API_URL}/register",
            json={
                "username": username,
                "password": password
            }
        )

        data = response.json()

        if response.status_code == 200:

            st.success(
                "Registration Successful! Please Login."
            )

        else:

            st.error(
                data.get(
                    "detail",
                    "Registration Failed"
                )
            )

# ==========================
# LOGIN
# ==========================

elif menu == "Login":

    st.header("Login")

    username = st.text_input(
        "Username",
        key="login_username"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button("Login"):

        response = requests.post(
            f"{API_URL}/login",
            json={
                "username": username,
                "password": password
            }
        )

        data = response.json()

        if "access_token" in data:

            st.session_state["token"] = (
                data["access_token"]
            )

            st.success(
                "Login Successful"
            )

        else:

            st.error(
                "Invalid Username or Password"
            )

# ==========================
# TASKS
# ==========================

elif menu == "Tasks":

    st.header("📋 Task Manager")

    task_title = st.text_input(
        "Enter Task"
    )

    if st.button("Add Task"):

        if task_title.strip():

            response = requests.post(
                f"{API_URL}/tasks",
                json={
                    "title": task_title
                }
            )

            st.success(
                response.json()["message"]
            )

            st.rerun()

    # LOAD TASKS

    response = requests.get(
        f"{API_URL}/tasks"
    )

    tasks = response.json()

    total_tasks = len(tasks)

    completed_tasks = sum(
        1 for task in tasks
        if task["completed"]
    )

    productivity = (
        (completed_tasks / total_tasks) * 100
        if total_tasks > 0
        else 0
    )

    st.divider()

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            "Total Tasks",
            total_tasks
        )

    with metric2:
        st.metric(
            "Completed",
            completed_tasks
        )

    with metric3:
        st.metric(
            "Productivity %",
            f"{productivity:.1f}%"
        )

    st.divider()

    st.subheader("My Tasks")

    if total_tasks == 0:

        st.info(
            "No tasks available."
        )

    else:

        for task in tasks:

            col1, col2, col3 = st.columns(
                [6, 1, 1]
            )

            with col1:

                status = (
                    "✅"
                    if task["completed"]
                    else "⏳"
                )

                st.write(
                    f"{status} {task['title']}"
                )

            with col2:

                if not task["completed"]:

                    if st.button(
                        "✓",
                        key=f"complete_{task['id']}"
                    ):

                        requests.put(
                            f"{API_URL}/tasks/{task['id']}"
                        )

                        st.rerun()

            with col3:

                if st.button(
                    "🗑️",
                    key=f"delete_{task['id']}"
                ):

                    requests.delete(
                        f"{API_URL}/tasks/{task['id']}"
                    )

                    st.rerun()

    st.divider()

    # AI SUMMARY

    if st.button(
        "🤖 Generate AI Summary"
    ):

        with st.spinner(
            "Generating Summary..."
        ):

            response = requests.get(
                f"{API_URL}/summary"
            )

            st.subheader(
                "AI Productivity Report"
            )

            st.success(
                response.json()["summary"]
            )

    st.divider()

    # TOMORROW PLAN

    if st.button(
        "📅 Generate Tomorrow Plan"
    ):

        with st.spinner(
            "Planning Tomorrow..."
        ):

            response = requests.get(
                f"{API_URL}/tomorrow-plan"
            )

            st.subheader(
                "Tomorrow's Plan"
            )

            st.info(
                response.json()["plan"]
            )