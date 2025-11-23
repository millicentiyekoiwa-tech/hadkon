import streamlit as st
import json
import os
from datetime import datetime
import random

# Page configuration
st.set_page_config(
    page_title="Hadkon Learning Platform",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .teacher-header {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .course-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 10px 0;
    }
    .lesson-complete {
        background: #d4edda;
        border-left: 5px solid #28a745;
    }
    .achievement-badge {
        display: inline-block;
        background: gold;
        padding: 5px 15px;
        border-radius: 20px;
        margin: 5px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_type' not in st.session_state:
    st.session_state.user_type = None  # 'student' or 'teacher'

if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'name': '',
        'points': 0,
        'completed_lessons': [],
        'current_streak': 0,
        'achievements': [],
        'game_unlocked': False
    }

if 'teacher_data' not in st.session_state:
    st.session_state.teacher_data = {
        'name': '',
        'password': 'teacher123'  # Default password (can be changed)
    }

if 'courses' not in st.session_state:
    st.session_state.courses = {
        'Mathematics': {
            'lessons': [
                {'id': 'math_1', 'title': 'Addition Basics', 'content': 'Learn to add numbers from 1-10', 'quiz': [
                    {'q': 'What is 3 + 4?', 'options': ['6', '7', '8', '9'], 'correct': 1},
                    {'q': 'What is 5 + 2?', 'options': ['6', '7', '8', '9'], 'correct': 1}
                ]},
                {'id': 'math_2', 'title': 'Subtraction Basics', 'content': 'Learn to subtract numbers from 1-10', 'quiz': [
                    {'q': 'What is 8 - 3?', 'options': ['4', '5', '6', '7'], 'correct': 1},
                    {'q': 'What is 9 - 4?', 'options': ['4', '5', '6', '7'], 'correct': 1}
                ]},
                {'id': 'math_3', 'title': 'Multiplication Tables', 'content': 'Learn multiplication tables 1-5', 'quiz': [
                    {'q': 'What is 3 × 4?', 'options': ['10', '11', '12', '13'], 'correct': 2},
                    {'q': 'What is 5 × 3?', 'options': ['13', '14', '15', '16'], 'correct': 2}
                ]}
            ]
        },
        'Science': {
            'lessons': [
                {'id': 'sci_1', 'title': 'Water Cycle', 'content': 'Understanding evaporation, condensation, and precipitation', 'quiz': [
                    {'q': 'What happens when water heats up?', 'options': ['It freezes', 'It evaporates', 'It melts', 'Nothing'], 'correct': 1},
                    {'q': 'What are clouds made of?', 'options': ['Cotton', 'Water vapor', 'Smoke', 'Air'], 'correct': 1}
                ]},
                {'id': 'sci_2', 'title': 'Plants and Photosynthesis', 'content': 'How plants make their own food', 'quiz': [
                    {'q': 'What do plants need for photosynthesis?', 'options': ['Water and soil', 'Sunlight and water', 'Air only', 'Nothing'], 'correct': 1}
                ]},
                {'id': 'sci_3', 'title': 'The Solar System', 'content': 'Learn about planets and the sun', 'quiz': [
                    {'q': 'How many planets are in our solar system?', 'options': ['7', '8', '9', '10'], 'correct': 1}
                ]}
            ]
        },
        'English': {
            'lessons': [
                {'id': 'eng_1', 'title': 'Parts of Speech', 'content': 'Nouns, verbs, and adjectives', 'quiz': [
                    {'q': 'What is a noun?', 'options': ['Action word', 'Describing word', 'Person/place/thing', 'Connecting word'], 'correct': 2}
                ]},
                {'id': 'eng_2', 'title': 'Sentence Structure', 'content': 'Building complete sentences', 'quiz': [
                    {'q': 'Every sentence needs a subject and a...', 'options': ['Noun', 'Verb', 'Adjective', 'Article'], 'correct': 1}
                ]},
                {'id': 'eng_3', 'title': 'Reading Comprehension', 'content': 'Understanding what you read', 'quiz': [
                    {'q': 'What helps you understand a story better?', 'options': ['Reading fast', 'Skipping words', 'Thinking about it', 'Reading once'], 'correct': 2}
                ]}
            ]
        }
    }

# Save/Load data functions
def save_courses():
    try:
        with open('hadkon_courses.json', 'w') as f:
            json.dump(st.session_state.courses, f)
    except:
        pass

def load_courses():
    try:
        if os.path.exists('hadkon_courses.json'):
            with open('hadkon_courses.json', 'r') as f:
                st.session_state.courses = json.load(f)
    except:
        pass

def save_user_data():
    try:
        with open('hadkon_user_data.json', 'w') as f:
            json.dump(st.session_state.user_data, f)
    except:
        pass

def load_user_data():
    try:
        if os.path.exists('hadkon_user_data.json'):
            with open('hadkon_user_data.json', 'r') as f:
                st.session_state.user_data = json.load(f)
    except:
        pass

# Load data on startup
load_courses()

# LOGIN SCREEN
if st.session_state.user_type is None:
    st.markdown('<div class="main-header"><h1>📚 Hadkon Learning Platform</h1><p>Learn Anywhere, Anytime - Even Offline!</p></div>', unsafe_allow_html=True)
    
    st.markdown("### Welcome! Please select your role:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👨‍🎓 Student Portal")
        st.info("Access courses, complete lessons, and earn achievements!")
        if st.button("Enter as Student", use_container_width=True, type="primary"):
            st.session_state.user_type = 'student'
            load_user_data()
            st.rerun()
    
    with col2:
        st.markdown("#### 👨‍🏫 Teacher Portal")
        st.info("Create and manage lessons, add courses, and track progress!")
        teacher_password = st.text_input("Teacher Password:", type="password", key="teacher_pwd")
        if st.button("Enter as Teacher", use_container_width=True):
            if teacher_password == st.session_state.teacher_data['password']:
                st.session_state.user_type = 'teacher'
                st.rerun()
            else:
                st.error("Incorrect password! Default password is: teacher123")

# STUDENT PORTAL
elif st.session_state.user_type == 'student':
    # Header
    st.markdown('<div class="main-header"><h1>📚 Hadkon Learning Platform</h1><p>Student Portal</p></div>', unsafe_allow_html=True)
    
    # Sidebar - User Profile
    with st.sidebar:
        st.header("👤 Student Profile")
        
        if st.button("🚪 Logout"):
            st.session_state.user_type = None
            st.rerun()
        
        st.markdown("---")
        
        if not st.session_state.user_data['name']:
            name = st.text_input("Enter your name:", key="name_input")
            if st.button("Start Learning"):
                if name:
                    st.session_state.user_data['name'] = name
                    save_user_data()
                    st.rerun()
        else:
            st.success(f"Welcome, {st.session_state.user_data['name']}! 👋")
            
            # Progress stats
            st.metric("🏆 Total Points", st.session_state.user_data['points'])
            st.metric("✅ Lessons Completed", len(st.session_state.user_data['completed_lessons']))
            st.metric("🔥 Current Streak", st.session_state.user_data['current_streak'])
            
            # Progress bar
            total_lessons = sum(len(course['lessons']) for course in st.session_state.courses.values())
            progress = len(st.session_state.user_data['completed_lessons']) / total_lessons if total_lessons > 0 else 0
            st.progress(progress)
            st.caption(f"{int(progress*100)}% Complete")
            
            # Achievements
            if st.session_state.user_data['achievements']:
                st.subheader("🏅 Achievements")
                for achievement in st.session_state.user_data['achievements']:
                    st.markdown(f'<div class="achievement-badge">{achievement}</div>', unsafe_allow_html=True)
            
            if st.button("🎮 Play Game" if st.session_state.user_data['game_unlocked'] else "🔒 Game Locked"):
                if st.session_state.user_data['game_unlocked']:
                    st.session_state.current_view = 'game'
                    st.rerun()
            
            if not st.session_state.user_data['game_unlocked']:
                st.caption("Complete lessons to unlock the game!")
            
            if st.button("Reset Progress"):
                st.session_state.user_data = {
                    'name': st.session_state.user_data['name'],
                    'points': 0,
                    'completed_lessons': [],
                    'current_streak': 0,
                    'achievements': [],
                    'game_unlocked': False
                }
                save_user_data()
                st.rerun()
    
    # Main content area
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'courses'
    
    if not st.session_state.user_data['name']:
        st.info("👈 Please enter your name in the sidebar to begin your learning journey!")
    else:
        # Navigation
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📚 Courses", use_container_width=True):
                st.session_state.current_view = 'courses'
                st.rerun()
        with col2:
            if st.button("📊 Dashboard", use_container_width=True):
                st.session_state.current_view = 'dashboard'
                st.rerun()
        with col3:
            if st.button("🎮 Game", use_container_width=True, disabled=not st.session_state.user_data['game_unlocked']):
                st.session_state.current_view = 'game'
                st.rerun()
        
        st.markdown("---")
        
        # Courses View
        if st.session_state.current_view == 'courses':
            st.header("📖 Available Courses")
            
            for course_name, course_data in st.session_state.courses.items():
                with st.expander(f"📘 {course_name}", expanded=True):
                    for lesson in course_data['lessons']:
                        is_completed = lesson['id'] in st.session_state.user_data['completed_lessons']
                        card_class = 'course-card lesson-complete' if is_completed else 'course-card'
                        
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(f'<div class="{card_class}"><h4>{"✅ " if is_completed else "📝 "}{lesson["title"]}</h4><p>{lesson["content"]}</p></div>', unsafe_allow_html=True)
                        with col2:
                            if not is_completed:
                                if st.button(f"Start", key=f"btn_{lesson['id']}"):
                                    st.session_state.current_lesson = lesson
                                    st.session_state.quiz_answers = {}
                                    st.session_state.quiz_submitted = False
                                    st.session_state.current_view = 'lesson'
                                    st.rerun()
                            else:
                                st.success("Done!")
        
        # Lesson View
        elif st.session_state.current_view == 'lesson':
            if 'current_lesson' in st.session_state:
                lesson = st.session_state.current_lesson
                
                st.header(f"📖 {lesson['title']}")
                st.info(lesson['content'])
                
                st.subheader("📝 Quiz")
                
                if not st.session_state.get('quiz_submitted', False):
                    for i, question in enumerate(lesson['quiz']):
                        st.write(f"**Question {i+1}:** {question['q']}")
                        answer = st.radio(
                            "Select your answer:",
                            question['options'],
                            key=f"q_{i}",
                            label_visibility="collapsed"
                        )
                        st.session_state.quiz_answers[i] = question['options'].index(answer)
                    
                    if st.button("Submit Quiz", type="primary"):
                        st.session_state.quiz_submitted = True
                        st.rerun()
                else:
                    # Check answers
                    correct_count = 0
                    for i, question in enumerate(lesson['quiz']):
                        if st.session_state.quiz_answers.get(i) == question['correct']:
                            correct_count += 1
                            st.success(f"✅ Question {i+1}: Correct!")
                        else:
                            st.error(f"❌ Question {i+1}: Incorrect. Correct answer: {question['options'][question['correct']]}")
                    
                    score_percent = (correct_count / len(lesson['quiz'])) * 100
                    
                    if score_percent >= 70:
                        st.balloons()
                        st.success(f"🎉 Congratulations! You scored {score_percent:.0f}%")
                        
                        # Award points and mark complete
                        if lesson['id'] not in st.session_state.user_data['completed_lessons']:
                            st.session_state.user_data['completed_lessons'].append(lesson['id'])
                            st.session_state.user_data['points'] += 10
                            st.session_state.user_data['current_streak'] += 1
                            
                            # Check for game unlock
                            if len(st.session_state.user_data['completed_lessons']) >= 3:
                                st.session_state.user_data['game_unlocked'] = True
                                st.success("🎮 Game unlocked! Check the sidebar!")
                            
                            # Check for achievements
                            if len(st.session_state.user_data['completed_lessons']) == 1:
                                st.session_state.user_data['achievements'].append("🌟 First Lesson")
                            if len(st.session_state.user_data['completed_lessons']) == 5:
                                st.session_state.user_data['achievements'].append("🔥 5 Lessons")
                            if st.session_state.user_data['points'] >= 50:
                                st.session_state.user_data['achievements'].append("💯 50 Points")
                            
                            save_user_data()
                    else:
                        st.warning(f"You scored {score_percent:.0f}%. You need 70% to pass. Try again!")
                    
                    if st.button("Back to Courses"):
                        st.session_state.current_view = 'courses'
                        st.rerun()
        
        # Dashboard View
        elif st.session_state.current_view == 'dashboard':
            st.header("📊 Your Learning Dashboard")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Points", st.session_state.user_data['points'], "+10" if st.session_state.user_data['points'] > 0 else "0")
            with col2:
                st.metric("Completed", len(st.session_state.user_data['completed_lessons']))
            with col3:
                st.metric("Streak", f"{st.session_state.user_data['current_streak']} days")
            with col4:
                st.metric("Achievements", len(st.session_state.user_data['achievements']))
            
            st.subheader("📈 Progress by Subject")
            for course_name, course_data in st.session_state.courses.items():
                completed = sum(1 for lesson in course_data['lessons'] if lesson['id'] in st.session_state.user_data['completed_lessons'])
                total = len(course_data['lessons'])
                progress = completed / total if total > 0 else 0
                
                st.write(f"**{course_name}**")
                st.progress(progress)
                st.caption(f"{completed}/{total} lessons completed")
        
        # Game View
        elif st.session_state.current_view == 'game':
            if st.session_state.user_data['game_unlocked']:
                st.header("🎮 Math Challenge Game")
                st.info("Reward yourself with a quick game break!")
                
                if 'game_state' not in st.session_state:
                    st.session_state.game_state = {
                        'score': 0,
                        'questions_answered': 0,
                        'current_question': None
                    }
                
                if st.session_state.game_state['current_question'] is None:
                    num1 = random.randint(1, 10)
                    num2 = random.randint(1, 10)
                    operation = random.choice(['+', '-', '×'])
                    
                    if operation == '+':
                        answer = num1 + num2
                    elif operation == '-':
                        answer = num1 - num2
                    else:
                        answer = num1 * num2
                    
                    st.session_state.game_state['current_question'] = {
                        'num1': num1,
                        'num2': num2,
                        'operation': operation,
                        'answer': answer
                    }
                
                q = st.session_state.game_state['current_question']
                st.subheader(f"What is {q['num1']} {q['operation']} {q['num2']}?")
                
                user_answer = st.number_input("Your answer:", min_value=-100, max_value=100, value=0, key=f"game_answer_{st.session_state.game_state['questions_answered']}")
                
                if st.button("Submit Answer"):
                    if user_answer == q['answer']:
                        st.success("✅ Correct!")
                        st.session_state.game_state['score'] += 1
                    else:
                        st.error(f"❌ Incorrect. The answer was {q['answer']}")
                    
                    st.session_state.game_state['questions_answered'] += 1
                    st.session_state.game_state['current_question'] = None
                    st.rerun()
                
                st.metric("Game Score", st.session_state.game_state['score'])
                st.metric("Questions Answered", st.session_state.game_state['questions_answered'])
                
                if st.button("Exit Game"):
                    st.session_state.current_view = 'courses'
                    del st.session_state.game_state
                    st.rerun()
            else:
                st.warning("🔒 Complete at least 3 lessons to unlock the game!")
                if st.button("Back to Courses"):
                    st.session_state.current_view = 'courses'
                    st.rerun()

# TEACHER PORTAL
elif st.session_state.user_type == 'teacher':
    st.markdown('<div class="teacher-header"><h1>👨‍🏫 Hadkon Teacher Portal</h1><p>Manage Courses & Lessons</p></div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("👨‍🏫 Teacher Menu")
        
        if st.button("🚪 Logout"):
            st.session_state.user_type = None
            st.rerun()
        
        st.markdown("---")
        
        teacher_view = st.radio(
            "Navigation:",
            ["📚 Manage Courses", "➕ Add New Lesson", "📊 Statistics"],
            label_visibility="collapsed"
        )
    
    # Manage Courses View
    if teacher_view == "📚 Manage Courses":
        st.header("📚 Manage Courses")
        
        # Add New Course
        with st.expander("➕ Add New Course", expanded=False):
            new_course_name = st.text_input("Course Name:", key="new_course")
            if st.button("Create Course"):
                if new_course_name and new_course_name not in st.session_state.courses:
                    st.session_state.courses[new_course_name] = {'lessons': []}
                    save_courses()
                    st.success(f"✅ Course '{new_course_name}' created!")
                    st.rerun()
                elif new_course_name in st.session_state.courses:
                    st.error("Course already exists!")
                else:
                    st.error("Please enter a course name")
        
        # Display existing courses
        st.subheader("Existing Courses")
        for course_name, course_data in st.session_state.courses.items():
            with st.expander(f"📘 {course_name} ({len(course_data['lessons'])} lessons)"):
                for idx, lesson in enumerate(course_data['lessons']):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"**{lesson['title']}**")
                        st.caption(lesson['content'])
                    with col2:
                        if st.button("🗑️ Delete", key=f"del_{lesson['id']}"):
                            course_data['lessons'].pop(idx)
                            save_courses()
                            st.rerun()
    
    # Add New Lesson View
    elif teacher_view == "➕ Add New Lesson":
        st.header("➕ Add New Lesson")
        
        # Select course
        course_name = st.selectbox("Select Course:", list(st.session_state.courses.keys()))
        
        # Lesson details
        lesson_title = st.text_input("Lesson Title:")
        lesson_content = st.text_area("Lesson Content/Notes:", height=150)
        
        st.subheader("Add Quiz Questions")
        num_questions = st.number_input("Number of Questions:", min_value=1, max_value=10, value=2)
        
        quiz_questions = []
        for i in range(num_questions):
            st.markdown(f"**Question {i+1}:**")
            col1, col2 = st.columns([3, 1])
            with col1:
                question = st.text_input(f"Question:", key=f"q_{i}")
            
            options = []
            for j in range(4):
                option = st.text_input(f"Option {j+1}:", key=f"q_{i}_opt_{j}")
                options.append(option)
            
            correct = st.selectbox(f"Correct Answer:", [1, 2, 3, 4], key=f"q_{i}_correct") - 1
            
            if question and all(options):
                quiz_questions.append({
                    'q': question,
                    'options': options,
                    'correct': correct
                })
            
            st.markdown("---")
        
        # Save lesson
        if st.button("💾 Save Lesson", type="primary"):
            if lesson_title and lesson_content and len(quiz_questions) == num_questions:
                lesson_id = f"{course_name.lower()[:3]}_{len(st.session_state.courses[course_name]['lessons']) + 1}"
                new_lesson = {
                    'id': lesson_id,
                    'title': lesson_title,
                    'content': lesson_content,
                    'quiz': quiz_questions
                }
                st.session_state.courses[course_name]['lessons'].append(new_lesson)
                save_courses()
                st.success(f"✅ Lesson '{lesson_title}' added to {course_name}!")
                st.balloons()
            else:
                st.error("Please fill in all fields and complete all quiz questions")
    
    # Statistics View
    elif teacher_view == "📊 Statistics":
        st.header("📊 Platform Statistics")
        
        total_courses = len(st.session_state.courses)
        total_lessons = sum(len(course['lessons']) for course in st.session_state.courses.values())
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Courses", total_courses)
        with col2:
            st.metric("Total Lessons", total_lessons)
        with col3:
            st.metric("Active Students", "N/A")
        
        st.subheader("Lessons per Course")
        for course_name, course_data in st.session_state.courses.items():
            st.write(f"**{course_name}:** {len(course_data['lessons'])} lessons")

# Footer
st.markdown("---")
st.caption("🌍 Hadkon - Education for Everyone, Everywhere | Works Offline | Made with ❤️")
