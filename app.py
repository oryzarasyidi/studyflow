import streamlit as st
import time

# =====================================
# CONFIG
# =====================================

st.set_page_config(
    page_title="StudyFlow",
    page_icon="📚",
    layout="centered"
)

# =====================================
# SESSION STATE
# =====================================

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "timer_seconds" not in st.session_state:
    st.session_state.timer_seconds = 25 * 60

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

# =====================================
# TITLE
# =====================================

st.title("📚 StudyFlow")
st.subheader("Smart To-Do List Pelajar")

st.info(
    "Sedikit progress setiap hari tetap lebih baik daripada tidak sama sekali."
)

# =====================================
# PROGRESS BAR
# =====================================

total_tasks = len(st.session_state.tasks)

completed_tasks = len([
    task for task in st.session_state.tasks
    if task["completed"]
])

progress = 0

if total_tasks > 0:
    progress = completed_tasks / total_tasks

st.write(f"### Progress Tugas: {int(progress * 100)}%")

st.progress(progress)

# =====================================
# FORM TAMBAH TUGAS
# =====================================

st.write("## ➕ Tambah Tugas")

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

    submit = st.form_submit_button("Tambah")

    if submit:

        new_task = {
            "title": title,
            "subject": subject,
            "deadline": str(deadline),
            "completed": False
        }

        st.session_state.tasks.append(new_task)

        st.success("Tugas berhasil ditambahkan!")

# =====================================
# TAMPILKAN TUGAS
# =====================================

st.write("## 📝 Daftar Tugas")

sorted_tasks = sorted(
    st.session_state.tasks,
    key=lambda x: x["subject"]
)

current_subject = ""

for i, task in enumerate(sorted_tasks):

    if current_subject != task["subject"]:

        current_subject = task["subject"]

        st.markdown(f"## 📘 {current_subject}")

    col1, col2, col3 = st.columns([5, 1, 1])

    with col1:

        if task["completed"]:
            st.markdown(f"~~{task['title']}~~")

        else:
            st.markdown(task["title"])

        st.caption(f"Deadline: {task['deadline']}")

    with col2:

        if not task["completed"]:

            if st.button("✔", key=f"done_{i}"):

                task["completed"] = True
                st.rerun()

    with col3:

        if st.button("🗑", key=f"delete_{i}"):

            st.session_state.tasks.remove(task)
            st.rerun()

# =====================================
# POMODORO TIMER
# =====================================

st.write("## ⏳ Pomodoro Timer")

minutes = st.session_state.timer_seconds // 60
seconds = st.session_state.timer_seconds % 60

st.markdown(f"# {minutes:02d}:{seconds:02d}")

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
        st.rerun()

# =====================================
# TIMER LOOP
# =====================================

if st.session_state.timer_running:

    time.sleep(1)

    st.session_state.timer_seconds -= 1

    if st.session_state.timer_seconds <= 0:

        st.success("Pomodoro selesai!")

        st.session_state.timer_seconds = 25 * 60
        st.session_state.timer_running = False

    st.rerun()