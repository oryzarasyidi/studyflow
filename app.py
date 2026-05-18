import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="StudyFlow",
    page_icon="📚",
    layout="centered"
)

DATA_FILE = "tasks.json"

# =========================
# Load Data
# =========================

def load_tasks():

    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        return json.load(file)


# =========================
# Save Data
# =========================

def save_tasks(tasks):

    with open(DATA_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


# =========================
# Initial Data
# =========================

if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

if "timer_seconds" not in st.session_state:
    st.session_state.timer_seconds = 25 * 60


# =========================
# Title
# =========================

st.title("📚 StudyFlow")
st.caption("Smart To-Do List Pelajar")

st.info(
    "Sedikit progress setiap hari tetap lebih baik daripada tidak sama sekali."
)


# =========================
# Progress Bar
# =========================

completed_tasks = [
    task for task in st.session_state.tasks
    if task["completed"]
]

progress = 0

if len(st.session_state.tasks) > 0:
    progress = len(completed_tasks) / len(st.session_state.tasks)

st.subheader("📈 Progress Tugas")
st.progress(progress)

st.write(f"{int(progress * 100)}% selesai")


# =========================
# Form Tambah Tugas
# =========================

st.subheader("➕ Tambah Tugas")

with st.form("task_form"):

    title = st.text_input("Nama Tugas")

    subject = st.selectbox(
        "Pilih Mapel",
        [
            "Matematika",
            "Fisika",
            "Kimia",
            "Biologi",
            "Sejarah",
            "Geografi",
            "Sosiologi",
            "Bahasa Indonesia",
            "Bahasa Inggris",
            "Informatika",
            "Bahasa Jawa",
            "Bahasa Arab",
            "Fikih",
            "Quran Hadis",
            "SKI",
            "Akidah Akhlak"
        ]
    )

    deadline = st.date_input("Deadline")

    submitted = st.form_submit_button("Tambah")

    if submitted:

        new_task = {
            "title": title,
            "subject": subject,
            "deadline": str(deadline),
            "completed": False
        }

        st.session_state.tasks.append(new_task)

        save_tasks(st.session_state.tasks)

        st.success("Tugas berhasil ditambahkan!")


# =========================
# Tampilkan Tugas
# =========================

st.subheader("📝 Daftar Tugas")

sorted_tasks = sorted(
    st.session_state.tasks,
    key=lambda x: x["subject"]
)

current_subject = ""

for index, task in enumerate(sorted_tasks):

    if current_subject != task["subject"]:

        current_subject = task["subject"]

        st.markdown(f"## 📘 {current_subject}")

    col1, col2, col3 = st.columns([5, 1, 1])

    with col1:

        if task["completed"]:
            st.markdown(
                f"~~{task['title']}~~  ")
        else:
            st.markdown(task["title"])

        st.caption(f"Deadline: {task['deadline']}")

    with col2:

        if not task["completed"]:

            if st.button("✔", key=f"done_{index}"):

                task["completed"] = True
                save_tasks(st.session_state.tasks)
                st.rerun()

    with col3:

        if st.button("🗑", key=f"delete_{index}"):

            st.session_state.tasks.remove(task)
            save_tasks(st.session_state.tasks)
            st.rerun()


# =========================
# Pomodoro Timer
# =========================

st.subheader("⏳ Pomodoro Timer")

minutes = st.session_state.timer_seconds // 60
seconds = st.session_state.timer_seconds % 60

st.markdown(
    f"# {minutes:02d}:{seconds:02d}"
)

col1, col2, col3 = st.columns(3)

with col1:

    if st.button("Start"):
        st.session_state.timer_running = True

with col2:

    if st.button("Pause"):
        st.session_state.timer_running = False

with col3:

    if st.button("Reset"):
        st.session_state.timer_seconds = 25 * 60
        st.session_state.timer_running = False


if st.session_state.timer_running:

    import time

    time.sleep(1)

    st.session_state.timer_seconds -= 1

    if st.session_state.timer_seconds <= 0:

        st.success("Pomodoro selesai!")

        st.session_state.timer_running = False

        st.session_state.timer_seconds = 25 * 60

    st.rerun()