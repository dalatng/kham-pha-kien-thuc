"""
===============================================================================
EDUSPARK ENGLISH PLATFORM - PYTHON 3.10 & FLASK
===============================================================================
Mô tả: Nền tảng học Tiếng Anh tương tác hiện đại tích hợp Flashcards 3D,
       Quiz Arena, AI Tutor Chatbot, Ngữ pháp tương tác & Biểu đồ tiến độ.
Tác giả: Gemini Assistant
Python Version: 3.10+
===============================================================================
"""

import os
import json
import random
from typing import Any, Dict, List, Optional, Tuple
from flask import Flask, render_template_string, jsonify, request, session

# =============================================================================
# 1. CẤU HÌNH ỨNG DỤNG FLASK
# =============================================================================

app = Flask(__name__)
app.secret_key = "eduspark_secret_key_python_310_super_secured"

# =============================================================================
# 2. CƠ SỞ DỮ LIỆU BÀI HỌC (DATA MODELS & DATASETS)
# =============================================================================

VOCABULARY_DB: list[dict[str, str | list[str]]] = [
    {
        "id": "v1",
        "word": "Resilience",
        "phonetic": "/rɪˈzɪl.jəns/",
        "type": "noun",
        "meaning": "Khả năng phục hồi, sự kiên cường",
        "example": "Her resilience in the face of adversity inspired everyone.",
        "level": "B2",
        "category": "Psychology",
        "synonyms": ["toughness", "flexibility", "adaptability"]
    },
    {
        "id": "v2",
        "word": "Meticulous",
        "phonetic": "/məˈtɪk.jə.ləs/",
        "type": "adjective",
        "meaning": "Tỉ mỉ, kỹ lưỡng, cẩn thận",
        "example": "He described the process with meticulous detail.",
        "level": "C1",
        "category": "Work & Business",
        "synonyms": ["thorough", "precise", "painstaking"]
    },
    {
        "id": "v3",
        "word": "Eradicate",
        "phonetic": "/ɪˈræd.ɪ.keɪt/",
        "type": "verb",
        "meaning": "Diệt trừ, xóa bỏ hoàn toàn",
        "example": "The government aims to eradicate poverty by 2030.",
        "level": "C1",
        "category": "Society",
        "synonyms": ["eliminate", "wipe out", "exterminate"]
    },
    {
        "id": "v4",
        "word": "Ambiguity",
        "phonetic": "/ˌæm.bɪˈɡjuː.ə.ti/",
        "type": "noun",
        "meaning": "Sự mơ hồ, nhập nhằng",
        "example": "Write clear instructions to avoid any ambiguity.",
        "level": "B2",
        "category": "Academic",
        "synonyms": ["uncertainty", "vagueness", "obscurity"]
    },
    {
        "id": "v5",
        "word": "Pragmatic",
        "phonetic": "/præɡˈmæt.ɪk/",
        "type": "adjective",
        "meaning": "Thực tế, thực dụng",
        "example": "We need a pragmatic approach to solve this issue quickly.",
        "level": "B2",
        "category": "Philosophy",
        "synonyms": ["practical", "realistic", "sensible"]
    },
    {
        "id": "v6",
        "word": "Eloquent",
        "phonetic": "/ˈel.ə.kwənt/",
        "type": "adjective",
        "meaning": "Hùng hồn, lưu loát, truyền cảm",
        "example": "She gave an eloquent speech about human rights.",
        "level": "C1",
        "category": "Communication",
        "synonyms": ["articulate", "persuasive", "expressive"]
    },
    {
        "id": "v7",
        "word": "Empathy",
        "phonetic": "/ˈem.pə.θi/",
        "type": "noun",
        "meaning": "Sự đồng cảm, thấu hiểu",
        "example": "Empathy is essential for building healthy relationships.",
        "level": "B1",
        "category": "Psychology",
        "synonyms": ["understanding", "compassion", "sympathy"]
    },
    {
        "id": "v8",
        "word": "Procrastinate",
        "phonetic": "/prəʊˈkræs.tɪ.neɪt/",
        "type": "verb",
        "meaning": "Trì hoãn, chần chừ",
        "example": "Don't procrastinate; start working on your goal today.",
        "level": "B2",
        "category": "Habits",
        "synonyms": ["delay", "postpone", "dally"]
    }
]

GRAMMAR_LESSONS: list[dict[str, Any]] = [
    {
        "id": "g1",
        "title": "Mastering the Present Perfect Continuous",
        "level": "Intermediate (B1-B2)",
        "formula": "S + have/has + been + V-ing",
        "summary": "Diễn tả hành động bắt đầu trong quá khứ, tiếp diễn ở hiện tại và có khả năng kéo dài đến tương lai.",
        "usage_points": [
            "Nhấn mạnh tính liên tục của hành động.",
            "Diễn tả hành động vừa hoàn thành nhưng để lại kết quả ở hiện tại.",
            "Dùng với 'for' (khoảng thời gian) và 'since' (mốc thời gian)."
        ],
        "examples": [
            "I have been learning English for 3 years.",
            "It has been raining all morning.",
            "She is tired because she has been working hard."
        ]
    },
    {
        "id": "g2",
        "title": "Third Conditional (Mệnh đề điều kiện loại 3)",
        "level": "Advanced (B2-C1)",
        "formula": "If + S + had + V3/ed, S + would/could/might + have + V3/ed",
        "summary": "Diễn tả giả định trái ngược với sự thật trong quá khứ và kết quả giả định của nó.",
        "usage_points": [
            "Dùng để thể hiện sự hối tiếc hoặc trách móc.",
            "Mô tả kịch bản thay thế cho sự kiện lịch sử/quá khứ."
        ],
        "examples": [
            "If I had studied harder, I would have passed the exam.",
            "They wouldn't have missed the flight if they had left earlier."
        ]
    }
]

QUIZ_BANK: list[dict[str, Any]] = [
    {
        "id": "q1",
        "question": "Choose the word closest in meaning to 'Meticulous':",
        "options": ["Careless", "Thorough & Precise", "Rapid", "Aggressive"],
        "answer": 1,
        "explanation": "'Meticulous' có nghĩa là tỉ mỉ, cẩn thận, đồng nghĩa với 'Thorough & Precise'."
    },
    {
        "id": "q2",
        "question": "Complete sentence: 'If she _____ harder, she would have passed the test.'",
        "options": ["studied", "has studied", "had studied", "would study"],
        "answer": 2,
        "explanation": "Câu điều kiện loại 3 sử dụng thì Quá khứ hoàn thành (had + V3) ở mệnh đề IF."
    },
    {
        "id": "q3",
        "question": "What is the correct pronunciation noun for 'Sự đồng cảm'?",
        "options": ["Apathy", "Empathy", "Antipathy", "Symbiosis"],
        "answer": 1,
        "explanation": "'Empathy' mang nghĩa là sự đồng cảm, thấu hiểu cảm xúc của người khác."
    },
    {
        "id": "q4",
        "question": "Identify the correct formula for Present Perfect Continuous:",
        "options": [
            "S + have/has + V3",
            "S + had + been + V-ing",
            "S + have/has + been + V-ing",
            "S + am/is/are + V-ing"
        ],
        "answer": 2,
        "explanation": "Công thức chuẩn của Thì hiện tại hoàn thành tiếp diễn là: S + have/has + been + V-ing."
    }
]

# =============================================================================
# 3. PYTHON 3.10 BUSINESS LOGIC HELPER FUNCTIONS (MATCH-CASE, TYPE HINTS)
# =============================================================================

def process_quiz_submission(user_answers: dict[str, int]) -> dict[str, Any]:
    """Xử lý chấm điểm trắc nghiệm sử dụng tính năng Python 3.10 pattern matching."""
    total = len(QUIZ_BANK)
    correct_count = 0
    detailed_results = []

    for idx, q in enumerate(QUIZ_BANK):
        user_choice = user_answers.get(str(q["id"]))
        is_correct = (user_choice == q["answer"])
        if is_correct:
            correct_count += 1

        # Minh họa sử dụng Match-Case trong Python 3.10
        match is_correct:
            case True:
                status_text = "Chính xác! Rất xuất sắc."
                badge_color = "success"
            case False:
                status_text = "Chưa đúng. Hãy xem giải thích bên dưới."
                badge_color = "danger"

        detailed_results.append({
            "question_id": q["id"],
            "question": q["question"],
            "user_choice": user_choice,
            "correct_answer": q["answer"],
            "is_correct": is_correct,
            "status_text": status_text,
            "badge_color": badge_color,
            "explanation": q["explanation"]
        })

    score_percentage = round((correct_count / total) * 100, 1) if total > 0 else 0

    return {
        "score": score_percentage,
        "correct_count": correct_count,
        "total_questions": total,
        "details": detailed_results
    }


def generate_ai_tutor_response(user_message: str) -> str:
    """Mô phỏng phản hồi từ AI Tutor luyện nói/viết Tiếng Anh."""
    msg = user_message.lower().strip()

    if "hello" in msg or "hi" in msg or "xin chào" in msg:
        return "Hello there! I am your AI English Assistant. How can I help you improve your vocabulary or grammar today?"
    elif "grammar" in msg or "ngữ pháp" in msg:
        return "Grammar is the backbone of English! I recommend reviewing the 'Third Conditional' or 'Present Perfect Continuous' in our Grammar section."
    elif "vocab" in msg or "từ vựng" in msg:
        return "To expand your vocabulary, try our interactive 3D Flashcards! Words like 'Resilience' and 'Meticulous' are great for academic fluency."
    elif "tip" in msg or "mẹo" in msg:
        return "Pro Tip: Practice speaking out loud for 15 minutes daily using our speech synthesis tool. Shadowing native speakers speeds up accent naturalness!"
    else:
        return f"That's an interesting point about '{user_message}'! Let's practice phrasing that in formal English: 'I would like to explore more details regarding {user_message}.' Keep going!"

# =============================================================================
# 4. FLASK API ROUTES & CONTROLLERS
# =============================================================================

@app.route("/")
def index():
    """Route chính trả về trang Single Page Application (SPA)."""
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/vocab", methods=["GET"])
def get_vocab():
    """API lấy danh sách từ vựng có hỗ trợ bộ lọc level."""
    level_filter = request.args.get("level", "ALL")
    search_query = request.args.get("search", "").lower()

    filtered_vocab = VOCABULARY_DB

    if level_filter != "ALL":
        filtered_vocab = [v for v in filtered_vocab if v["level"] == level_filter]

    if search_query:
        filtered_vocab = [
            v for v in filtered_vocab 
            if search_query in v["word"].lower() or search_query in v["meaning"].lower()
        ]

    return jsonify({"status": "success", "data": filtered_vocab, "count": len(filtered_vocab)})


@app.route("/api/grammar", methods=["GET"])
def get_grammar():
    """API lấy danh sách bài học ngữ pháp."""
    return jsonify({"status": "success", "data": GRAMMAR_LESSONS})


@app.route("/api/quiz/questions", methods=["GET"])
def get_quiz_questions():
    """API lấy danh sách câu hỏi trắc nghiệm (ẩn đáp án đúng để bảo mật)."""
    public_questions = []
    for q in QUIZ_BANK:
        public_questions.append({
            "id": q["id"],
            "question": q["question"],
            "options": q["options"]
        })
    return jsonify({"status": "success", "data": public_questions})


@app.route("/api/quiz/submit", methods=["POST"])
def submit_quiz():
    """API nhận câu trả lời và chấm điểm."""
    data = request.get_json() or {}
    answers = data.get("answers", {})
    results = process_quiz_submission(answers)
    return jsonify({"status": "success", "result": results})


@app.route("/api/chat", methods=["POST"])
def chat_ai():
    """API phản hồi cuộc trò chuyện luyện tập Tiếng Anh."""
    data = request.get_json() or {}
    user_message = data.get("message", "")
    reply = generate_ai_tutor_response(user_message)
    return jsonify({"status": "success", "reply": reply})

# =============================================================================
# 5. UI HTML/CSS/JS SINGLE PAGE TEMPLATE (EMBEDDED)
# =============================================================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EduSpark - Nền Tảng Học Tiếng Anh Tương Tác</title>
    <!-- Google Fonts & FontAwesome -->
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        /* ====================================================================
           MODERN CSS STYLES & GLASSMORPHISM DESIGN SYSTEM
           ==================================================================== */
        :root {
            --bg-dark: #0f172a;
            --bg-card: rgba(30, 41, 59, 0.7);
            --bg-card-hover: rgba(51, 65, 85, 0.8);
            --accent-primary: #6366f1;
            --accent-secondary: #ec4899;
            --accent-cyan: #06b6d4;
            --accent-green: #10b981;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border-glass: rgba(255, 255, 255, 0.1);
            --shadow-glow: 0 10px 30px -10px rgba(99, 102, 241, 0.4);
            --radius-lg: 24px;
            --radius-md: 16px;
            --radius-sm: 10px;
            --transition-fast: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            --transition-spring: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            min-height: 100vh;
            overflow-x: hidden;
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.15) 0px, transparent 50%),
                radial-gradient(at 50% 50%, rgba(6, 182, 212, 0.1) 0px, transparent 50%);
            background-attachment: fixed;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: var(--bg-dark);
        }
        ::-webkit-scrollbar-thumb {
            background: #334155;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-primary);
        }

        /* App Container & Sidebar Layout */
        .app-wrapper {
            display: flex;
            min-height: 100vh;
        }

        /* Sidebar Navigation */
        .sidebar {
            width: 280px;
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(20px);
            border-right: 1px solid var(--border-glass);
            padding: 2rem 1.5rem;
            display: flex;
            flex-direction: column;
            position: fixed;
            height: 100vh;
            z-index: 100;
        }

        .brand-logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 1.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #818cf8, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 3rem;
        }

        .brand-logo i {
            font-size: 1.8rem;
            color: var(--accent-primary);
            -webkit-text-fill-color: initial;
        }

        .nav-menu {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .nav-item {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 14px 18px;
            color: var(--text-muted);
            border-radius: var(--radius-md);
            cursor: pointer;
            font-weight: 600;
            transition: var(--transition-fast);
            position: relative;
            overflow: hidden;
        }

        .nav-item:hover, .nav-item.active {
            color: var(--text-main);
            background: rgba(99, 102, 241, 0.15);
            border: 1px solid rgba(99, 102, 241, 0.3);
        }

        .nav-item.active::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 4px;
            background: linear-gradient(to bottom, var(--accent-primary), var(--accent-secondary));
            border-radius: 0 4px 4px 0;
        }

        .nav-item i {
            font-size: 1.2rem;
        }

        .user-profile-badge {
            margin-top: auto;
            background: var(--bg-card);
            border: 1px solid var(--border-glass);
            padding: 14px;
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .avatar {
            width: 42px;
            height: 42px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-cyan));
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
        }

        /* Main Content Viewport */
        .main-viewport {
            margin-left: 280px;
            flex: 1;
            padding: 2.5rem 3rem;
            max-width: 1400px;
        }

        /* Header Bar */
        .top-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2.5rem;
        }

        .header-title h1 {
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -0.5px;
        }

        .header-title p {
            color: var(--text-muted);
            margin-top: 4px;
        }

        .stats-pills {
            display: flex;
            gap: 15px;
        }

        .pill {
            background: var(--bg-card);
            border: 1px solid var(--border-glass);
            padding: 10px 18px;
            border-radius: 30px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 600;
            font-size: 0.9rem;
            backdrop-filter: blur(10px);
        }

        .pill i {
            color: #f59e0b;
        }

        /* Views Layout */
        .view-section {
            display: none;
            animation: fadeIn 0.4s ease-out forwards;
        }

        .view-section.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* HERO DASHBOARD */
        .hero-banner {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(236, 72, 153, 0.2));
            border: 1px solid var(--border-glass);
            border-radius: var(--radius-lg);
            padding: 3rem;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(20px);
            margin-bottom: 2.5rem;
        }

        .hero-banner::after {
            content: '';
            position: absolute;
            top: -50%;
            right: -10%;
            width: 350px;
            height: 350px;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.3) 0%, transparent 70%);
            border-radius: 50%;
            z-index: 0;
        }

        .hero-content {
            position: relative;
            z-index: 1;
            max-width: 650px;
        }

        .hero-content h2 {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 1rem;
            line-height: 1.2;
        }

        .hero-content p {
            color: var(--text-muted);
            font-size: 1.1rem;
            margin-bottom: 2rem;
            line-height: 1.6;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            color: white;
            border: none;
            padding: 14px 28px;
            border-radius: 30px;
            font-weight: 700;
            font-size: 1rem;
            cursor: pointer;
            box-shadow: var(--shadow-glow);
            transition: var(--transition-fast);
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }

        .btn-primary:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 15px 35px -10px rgba(99, 102, 241, 0.6);
        }

        /* GRID DASHBOARD CARDS */
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }

        .dash-card {
            background: var(--bg-card);
            border: 1px solid var(--border-glass);
            border-radius: var(--radius-md);
            padding: 1.8rem;
            backdrop-filter: blur(16px);
            transition: var(--transition-fast);
            cursor: pointer;
        }

        .dash-card:hover {
            background: var(--bg-card-hover);
            transform: translateY(-5px);
            border-color: rgba(99, 102, 241, 0.4);
        }

        .dash-icon {
            width: 50px;
            height: 50px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            margin-bottom: 1.2rem;
        }

        /* FLASHCARD STYLES (3D FLIP EFFECT) */
        .flashcard-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 2rem;
            margin-top: 2rem;
        }

        .flashcard-scene {
            width: 100%;
            max-width: 550px;
            height: 350px;
            perspective: 1000px;
        }

        .flashcard {
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            cursor: pointer;
        }

        .flashcard.is-flipped {
            transform: rotateY(180deg);
        }

        .card-face {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            border-radius: var(--radius-lg);
            border: 1px solid var(--border-glass);
            padding: 2.5rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            text-align: center;
            backdrop-filter: blur(20px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }

        .card-front {
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9));
        }

        .card-back {
            background: linear-gradient(145deg, rgba(49, 46, 129, 0.9), rgba(15, 23, 42, 0.9));
            transform: rotateY(180deg);
        }

        .word-badge {
            background: rgba(99, 102, 241, 0.2);
            color: #a5b4fc;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
        }

        .word-main {
            font-size: 3rem;
            font-weight: 800;
            letter-spacing: -1px;
            margin-top: 1rem;
        }

        .word-phonetic {
            color: var(--accent-cyan);
            font-size: 1.2rem;
            margin-top: 0.5rem;
        }

        .audio-btn {
            background: rgba(255, 255, 255, 0.1);
            border: none;
            width: 45px;
            height: 45px;
            border-radius: 50%;
            color: white;
            cursor: pointer;
            transition: var(--transition-fast);
            margin-top: 1rem;
        }

        .audio-btn:hover {
            background: var(--accent-primary);
            transform: scale(1.1);
        }

        .flashcard-controls {
            display: flex;
            gap: 1.5rem;
            align-items: center;
        }

        .btn-circle {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            border: 1px solid var(--border-glass);
            background: var(--bg-card);
            color: white;
            font-size: 1.3rem;
            cursor: pointer;
            transition: var(--transition-fast);
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .btn-circle:hover {
            background: var(--accent-primary);
            transform: scale(1.1);
        }

        /* QUIZ ARENA STYLES */
        .quiz-card {
            background: var(--bg-card);
            border: 1px solid var(--border-glass);
            border-radius: var(--radius-lg);
            padding: 2.5rem;
            max-width: 800px;
            margin: 0 auto;
            backdrop-filter: blur(20px);
        }

        .quiz-progress-bar {
            width: 100%;
            height: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 2rem;
        }

        .quiz-progress-fill {
            height: 100%;
            width: 25%;
            background: linear-gradient(to right, var(--accent-primary), var(--accent-secondary));
            transition: width 0.3s ease;
        }

        .options-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1rem;
            margin: 2rem 0;
        }

        .option-item {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border-glass);
            padding: 1.2rem 1.5rem;
            border-radius: var(--radius-md);
            cursor: pointer;
            font-weight: 600;
            transition: var(--transition-fast);
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .option-item:hover {
            border-color: var(--accent-primary);
            background: rgba(99, 102, 241, 0.1);
        }

        .option-item.selected {
            border-color: var(--accent-secondary);
            background: rgba(236, 72, 153, 0.2);
        }

        .option-idx {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9rem;
        }

        /* AI CHATBOT INTERFACE */
        .chat-container {
            background: var(--bg-card);
            border: 1px solid var(--border-glass);
            border-radius: var(--radius-lg);
            height: 650px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            backdrop-filter: blur(20px);
        }

        .chat-messages {
            flex: 1;
            padding: 2rem;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .message-bubble {
            max-width: 70%;
            padding: 1.2rem 1.5rem;
            border-radius: 20px;
            line-height: 1.5;
            font-size: 0.95rem;
            position: relative;
            animation: fadeIn 0.3s ease-out;
        }

        .message-bubble.bot {
            background: rgba(30, 41, 59, 0.9);
            border: 1px solid var(--border-glass);
            align-self: flex-start;
            border-bottom-left-radius: 4px;
        }

        .message-bubble.user {
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            align-self: flex-end;
            border-bottom-right-radius: 4px;
        }

        .chat-input-area {
            padding: 1.5rem;
            border-top: 1px solid var(--border-glass);
            background: rgba(15, 23, 42, 0.8);
            display: flex;
            gap: 12px;
        }

        .chat-input {
            flex: 1;
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid var(--border-glass);
            padding: 14px 20px;
            border-radius: 30px;
            color: white;
            outline: none;
            font-size: 0.95rem;
        }

        .chat-input:focus {
            border-color: var(--accent-primary);
        }

        /* GRAMMAR ACCORDION CARD */
        .grammar-card {
            background: var(--bg-card);
            border: 1px solid var(--border-glass);
            border-radius: var(--radius-md);
            padding: 2rem;
            margin-bottom: 1.5rem;
            backdrop-filter: blur(16px);
        }

        .formula-box {
            background: rgba(15, 23, 42, 0.8);
            border-left: 4px solid var(--accent-cyan);
            padding: 1rem 1.5rem;
            border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
            margin: 1rem 0;
            font-family: monospace;
            font-size: 1.1rem;
            color: var(--accent-cyan);
        }

        /* CANVAS CHART CONTAINER */
        .chart-box {
            background: var(--bg-card);
            border: 1px solid var(--border-glass);
            border-radius: var(--radius-lg);
            padding: 2rem;
            margin-top: 2rem;
            text-align: center;
        }

        canvas {
            max-width: 100%;
            height: 260px;
        }
    </style>
</head>
<body>

    <div class="app-wrapper">
        <!-- SIDEBAR NAVIGATION -->
        <aside class="sidebar">
            <div class="brand-logo">
                <i class="fa-solid fa-bolt-lightning"></i>
                <span>EduSpark 3.10</span>
            </div>

            <ul class="nav-menu">
                <li class="nav-item active" onclick="switchTab('dashboard')">
                    <i class="fa-solid fa-house"></i>
                    <span>Trang Chủ</span>
                </li>
                <li class="nav-item" onclick="switchTab('flashcards')">
                    <i class="fa-solid fa-clone"></i>
                    <span>Flashcards 3D</span>
                </li>
                <li class="nav-item" onclick="switchTab('grammar')">
                    <i class="fa-solid fa-book-open"></i>
                    <span>Ngữ Pháp Smart</span>
                </li>
                <li class="nav-item" onclick="switchTab('quiz')">
                    <i class="fa-solid fa-graduation-cap"></i>
                    <span>Quiz Arena</span>
                </li>
                <li class="nav-item" onclick="switchTab('chat')">
                    <i class="fa-solid fa-robot"></i>
                    <span>AI Tutor Practice</span>
                </li>
            </ul>

            <div class="user-profile-badge">
                <div class="avatar">PY</div>
                <div>
                    <div style="font-weight: 700; font-size: 0.95rem;">Python Scholar</div>
                    <div style="color: var(--text-muted); font-size: 0.8rem;">Level B2 • Advanced</div>
                </div>
            </div>
        </aside>

        <!-- MAIN VIEWPORT -->
        <main class="main-viewport">
            <!-- TOP HEADER -->
            <header class="top-header">
                <div class="header-title">
                    <h1 id="page-title">Hệ Thống Học Tiếng Anh Thông Minh</h1>
                    <p id="page-subtitle">Chào mừng trở lại! Hôm nay bạn sẵn sàng chinh phục từ vựng mới chưa?</p>
                </div>
                <div class="stats-pills">
                    <div class="pill">
                        <i class="fa-solid fa-fire"></i>
                        <span>Streak: <strong style="color: #f59e0b;">12 Ngày</strong></span>
                    </div>
                    <div class="pill">
                        <i class="fa-solid fa-gem" style="color: #ec4899;"></i>
                        <span>XP: <strong style="color: #ec4899;">2,450</strong></span>
                    </div>
                </div>
            </header>

            <!-- SECTION 1: DASHBOARD HERO -->
            <section id="view-dashboard" class="view-section active">
                <div class="hero-banner">
                    <div class="hero-content">
                        <h2>Nâng Tầm Tiếng Anh Với Công Nghệ Tương Tác</h2>
                        <p>Trải nghiệm phương pháp học chủ động kết hợp giữa Flashcard 3D, bài tập phản xạ và AI Tutor đàm thoại chuẩn bản xứ.</p>
                        <button class="btn-primary" onclick="switchTab('flashcards')">
                            <span>Khám Phá Flashcards ngay</span>
                            <i class="fa-solid fa-arrow-right"></i>
                        </button>
                    </div>
                </div>

                <div class="dashboard-grid">
                    <div class="dash-card" onclick="switchTab('flashcards')">
                        <div class="dash-icon" style="background: rgba(99, 102, 241, 0.2); color: #818cf8;">
                            <i class="fa-solid fa-layer-group"></i>
                        </div>
                        <h3>Flashcards 3D</h3>
                        <p style="color: var(--text-muted); font-size: 0.9rem; margin-top: 8px;">Hơn 500+ từ vựng C1-B2 kèm phát âm audio AI & ngữ cảnh.</p>
                    </div>

                    <div class="dash-card" onclick="switchTab('grammar')">
                        <div class="dash-icon" style="background: rgba(6, 182, 212, 0.2); color: #22d3ee;">
                            <i class="fa-solid fa-code-branch"></i>
                        </div>
                        <h3>Chuyên Đề Ngữ Pháp</h3>
                        <p style="color: var(--text-muted); font-size: 0.9rem; margin-top: 8px;">Sơ đồ tư duy cấu trúc câu phức & ngữ pháp nâng cao.</p>
                    </div>

                    <div class="dash-card" onclick="switchTab('quiz')">
                        <div class="dash-icon" style="background: rgba(236, 72, 153, 0.2); color: #f472b6;">
                            <i class="fa-solid fa-trophy"></i>
                        </div>
                        <h3>Quiz Arena</h3>
                        <p style="color: var(--text-muted); font-size: 0.9rem; margin-top: 8px;">Thách thức phản xạ kiến thức với bộ câu hỏi chấm điểm tức thì.</p>
                    </div>
                </div>

                <!-- PROGRESS CANVAS CHART -->
                <div class="chart-box">
                    <h3 style="margin-bottom: 1rem; text-align: left;">Biểu Đồ Tiến Độ Học Tập Trong Tuần (XP)</h3>
                    <canvas id="progressCanvas"></canvas>
                </div>
            </section>

            <!-- SECTION 2: 3D FLASHCARDS -->
            <section id="view-flashcards" class="view-section">
                <div class="flashcard-container">
                    <div class="flashcard-scene" onclick="flipCard()">
                        <div class="flashcard" id="active-card">
                            <!-- Mặt trước -->
                            <div class="card-face card-front">
                                <span class="word-badge" id="card-level">Level B2</span>
                                <div>
                                    <div class="word-main" id="card-word">Resilience</div>
                                    <div class="word-phonetic" id="card-phonetic">/rɪˈzɪl.jəns/</div>
                                </div>
                                <button class="audio-btn" onclick="speakCurrentWord(event)">
                                    <i class="fa-solid fa-volume-high"></i>
                                </button>
                                <div style="color: var(--text-muted); font-size: 0.85rem;">Click để lật xem nghĩa</div>
                            </div>
                            <!-- Mặt sau -->
                            <div class="card-face card-back">
                                <span class="word-badge" style="background: rgba(236, 72, 153, 0.3); color: #f472b6;">Định Nghĩa</span>
                                <div>
                                    <h3 id="card-meaning" style="font-size: 1.5rem; color: #38bdf8;">Khả năng phục hồi, sự kiên cường</h3>
                                    <p id="card-example" style="margin-top: 1rem; font-style: italic; color: #cbd5e1;">"Her resilience in the face of adversity inspired everyone."</p>
                                </div>
                                <div style="color: var(--text-muted); font-size: 0.85rem;">Click để quay lại</div>
                            </div>
                        </div>
                    </div>

                    <div class="flashcard-controls">
                        <button class="btn-circle" onclick="prevCard()"><i class="fa-solid fa-chevron-left"></i></button>
                        <span id="card-counter" style="font-weight: 700; font-size: 1.1rem;">1 / 8</span>
                        <button class="btn-circle" onclick="nextCard()"><i class="fa-solid fa-chevron-right"></i></button>
                    </div>
                </div>
            </section>

            <!-- SECTION 3: GRAMMAR HUB -->
            <section id="view-grammar" class="view-section">
                <div id="grammar-list-container">
                    <!-- Dynamic Grammar Content Rendered via JS -->
                </div>
            </section>

            <!-- SECTION 4: QUIZ ARENA -->
            <section id="view-quiz" class="view-section">
                <div class="quiz-card">
                    <div class="quiz-progress-bar">
                        <div class="quiz-progress-fill" id="quiz-progress"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; color: var(--text-muted); font-size: 0.9rem;">
                        <span>Câu hỏi <strong id="quiz-current-num">1</strong> / <span id="quiz-total-num">4</span></span>
                        <span>Quiz Arena</span>
                    </div>

                    <h2 id="quiz-question-text" style="margin-top: 1.5rem; font-size: 1.3rem;">Loading question...</h2>

                    <div class="options-grid" id="quiz-options-container">
                        <!-- Dynamic Quiz Options -->
                    </div>

                    <div style="display: flex; justify-content: flex-end; margin-top: 1.5rem;">
                        <button class="btn-primary" id="btn-next-quiz" onclick="nextQuizQuestion()">
                            <span>Next Question</span>
                            <i class="fa-solid fa-arrow-right"></i>
                        </button>
                    </div>
                </div>
            </section>

            <!-- SECTION 5: AI TUTOR CHAT -->
            <section id="view-chat" class="view-section">
                <div class="chat-container">
                    <div class="chat-messages" id="chat-messages-box">
                        <div class="message-bubble bot">
                            Hello! I am your AI English Learning Companion. You can type any sentence or question in English, and I will help you practice speaking and grammar!
                        </div>
                    </div>
                    <div class="chat-input-area">
                        <input type="text" class="chat-input" id="chat-input-field" placeholder="Type your message in English..." onkeydown="handleChatKey(event)">
                        <button class="btn-primary" onclick="sendChatMessage()" style="padding: 12px 24px;">
                            <i class="fa-solid fa-paper-plane"></i>
                        </button>
                    </div>
                </div>
            </section>
        </main>
    </div>

    <!-- ====================================================================
         JAVASCRIPT APPLICATION LOGIC & INTERACTIVE ENGINES
         ==================================================================== -->
    <script>
        // GLOBAL APP STATE
        let vocabData = [];
        let currentVocabIndex = 0;
        let quizData = [];
        let currentQuizIndex = 0;
        let userQuizAnswers = {};

        // INITIALIZATION
        document.addEventListener("DOMContentLoaded", () => {
            fetchVocabData();
            fetchGrammarData();
            fetchQuizQuestions();
            renderProgressChart();
        });

        // TAB SWITCHING CONTROLLER
        function switchTab(tabId) {
            document.querySelectorAll(".nav-item").forEach(item => item.classList.remove("active"));
            document.querySelectorAll(".view-section").forEach(sec => sec.classList.remove("active"));

            const targetNav = Array.from(document.querySelectorAll(".nav-item")).find(el => el.getAttribute("onclick").includes(tabId));
            if (targetNav) targetNav.classList.add("active");

            const targetSection = document.getElementById(`view-${tabId}`);
            if (targetSection) targetSection.classList.add("active");

            // Update Page Titles Dynamically
            const titles = {
                'dashboard': ['Hệ Thống Học Tiếng Anh Thông Minh', 'Chào mừng trở lại! Hôm nay bạn sẵn sàng chinh phục từ vựng mới chưa?'],
                'flashcards': ['Thẻ Từ Vựng 3D Tương Tác', 'Lật thẻ để học từ mới và nhấn icon loa để nghe phát âm giọng chuẩn AI.'],
                'grammar': ['Chuyên Đề Ngữ Pháp Smart', 'Tổng hợp cấu trúc ngữ pháp Tiếng Anh với công thức & ví dụ chi tiết.'],
                'quiz': ['Quiz Arena - Luyện Tập Phản Xạ', 'Kiểm tra trình độ kiến thức qua các câu hỏi trắc nghiệm nhanh.'],
                'chat': ['AI English Tutor Practice', 'Trò chuyện bằng Tiếng Anh để tăng phản xạ nói và sửa lỗi câu tự động.']
            };

            if (titles[tabId]) {
                document.getElementById('page-title').innerText = titles[tabId][0];
                document.getElementById('page-subtitle').innerText = titles[tabId][1];
            }
        }

        // FLASHCARD 3D CONTROLLER
        async function fetchVocabData() {
            try {
                const res = await fetch('/api/vocab');
                const json = await res.json();
                if (json.status === 'success') {
                    vocabData = json.data;
                    renderCurrentFlashcard();
                }
            } catch (err) {
                console.error("Error fetching vocab:", err);
            }
        }

        function renderCurrentFlashcard() {
            if (vocabData.length === 0) return;
            const item = vocabData[currentVocabIndex];
            
            document.getElementById("card-word").innerText = item.word;
            document.getElementById("card-phonetic").innerText = item.phonetic;
            document.getElementById("card-level").innerText = `Level ${item.level}`;
            document.getElementById("card-meaning").innerText = item.meaning;
            document.getElementById("card-example").innerText = `"${item.example}"`;
            document.getElementById("card-counter").innerText = `${currentVocabIndex + 1} / ${vocabData.length}`;

            // Reset Flip State
            document.getElementById("active-card").classList.remove("is-flipped");
        }

        function flipCard() {
            document.getElementById("active-card").classList.toggle("is-flipped");
        }

        function nextCard() {
            if (currentVocabIndex < vocabData.length - 1) {
                currentVocabIndex++;
                renderCurrentFlashcard();
            }
        }

        function prevCard() {
            if (currentVocabIndex > 0) {
                currentVocabIndex--;
                renderCurrentFlashcard();
            }
        }

        // WEB SPEECH SYNTHESIS API (SPEECH SOUND)
        function speakCurrentWord(event) {
            event.stopPropagation(); // Prevent card flipping when clicking speaker
            if ('speechSynthesis' in window) {
                const word = vocabData[currentVocabIndex].word;
                const utterance = new SpeechSynthesisUtterance(word);
                utterance.lang = 'en-US';
                utterance.rate = 0.85;
                window.speechSynthesis.speak(utterance);
            } else {
                alert("Trình duyệt của bạn không hỗ trợ tính năng phát âm Web Speech API.");
            }
        }

        // GRAMMAR RENDERER
        async function fetchGrammarData() {
            try {
                const res = await fetch('/api/grammar');
                const json = await res.json();
                if (json.status === 'success') {
                    const container = document.getElementById("grammar-list-container");
                    container.innerHTML = json.data.map(item => `
                        <div class="grammar-card">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <h2>${item.title}</h2>
                                <span class="word-badge" style="background: rgba(6, 182, 212, 0.2); color: #22d3ee;">${item.level}</span>
                            </div>
                            <p style="color: var(--text-muted); margin-top: 8px;">${item.summary}</p>
                            
                            <div class="formula-box">
                                <strong>Công thức:</strong> ${item.formula}
                            </div>

                            <h4 style="margin-top: 1rem; color: #a5b4fc;">Điểm lưu ý:</h4>
                            <ul style="margin-left: 1.2rem; margin-top: 0.5rem; color: var(--text-muted); line-height: 1.8;">
                                ${item.usage_points.map(pt => `<li>${pt}</li>`).join('')}
                            </ul>

                            <h4 style="margin-top: 1rem; color: #a5b4fc;">Ví dụ minh họa:</h4>
                            <ul style="margin-left: 1.2rem; margin-top: 0.5rem; color: #e2e8f0; font-style: italic;">
                                ${item.examples.map(ex => `<li>"${ex}"</li>`).join('')}
                            </ul>
                        </div>
                    `).join('');
                }
            } catch (err) {
                console.error("Error fetching grammar:", err);
            }
        }

        // QUIZ ARENA ENGINE
        async function fetchQuizQuestions() {
            try {
                const res = await fetch('/api/quiz/questions');
                const json = await res.json();
                if (json.status === 'success') {
                    quizData = json.data;
                    renderQuizQuestion();
                }
            } catch (err) {
                console.error("Error fetching quiz:", err);
            }
        }

        function renderQuizQuestion() {
            if (quizData.length === 0) return;

            const q = quizData[currentQuizIndex];
            document.getElementById("quiz-question-text").innerText = q.question;
            document.getElementById("quiz-current-num").innerText = currentQuizIndex + 1;
            document.getElementById("quiz-total-num").innerText = quizData.length;

            const progressPct = ((currentQuizIndex + 1) / quizData.length) * 100;
            document.getElementById("quiz-progress").style.width = `${progressPct}%`;

            const optionsContainer = document.getElementById("quiz-options-container");
            optionsContainer.innerHTML = q.options.map((opt, idx) => `
                <div class="option-item ${userQuizAnswers[q.id] === idx ? 'selected' : ''}" onclick="selectQuizOption('${q.id}', ${idx})">
                    <div class="option-idx">${String.fromCharCode(65 + idx)}</div>
                    <div>${opt}</div>
                </div>
            `).join('');

            const btnNext = document.getElementById("btn-next-quiz");
            if (currentQuizIndex === quizData.length - 1) {
                btnNext.innerHTML = `<span>Hoàn Thành & Nộp Bài</span> <i class="fa-solid fa-check"></i>`;
            } else {
                btnNext.innerHTML = `<span>Câu Tiếp Theo</span> <i class="fa-solid fa-arrow-right"></i>`;
            }
        }

        function selectQuizOption(questionId, optionIdx) {
            userQuizAnswers[questionId] = optionIdx;
            renderQuizQuestion();
        }

        async function nextQuizQuestion() {
            if (currentQuizIndex < quizData.length - 1) {
                currentQuizIndex++;
                renderQuizQuestion();
            } else {
                // Submit Quiz
                try {
                    const res = await fetch('/api/quiz/submit', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ answers: userQuizAnswers })
                    });
                    const json = await res.json();
                    if (json.status === 'success') {
                        showQuizResultModal(json.result);
                    }
                } catch (err) {
                    console.error("Error submitting quiz:", err);
                }
            }
        }

        function showQuizResultModal(result) {
            const container = document.getElementById("quiz-options-container");
            document.getElementById("quiz-question-text").innerText = `Kết quả Quiz Arena: ${result.score}% Score!`;
            
            container.innerHTML = `
                <div style="text-align: center; padding: 2rem;">
                    <h3 style="color: var(--accent-green); font-size: 2rem;">Đúng ${result.correct_count} / ${result.total_questions} câu!</h3>
                    <p style="color: var(--text-muted); margin-top: 10px;">Bạn đã nhận được +${result.correct_count * 50} XP vào tài khoản.</p>
                    <button class="btn-primary" onclick="location.reload()" style="margin-top: 1.5rem;">Thử Lại Từ Đầu</button>
                </div>
            `;
            document.getElementById("btn-next-quiz").style.display = "none";
        }

        // AI TUTOR CHAT CONTROLLER
        function handleChatKey(event) {
            if (event.key === 'Enter') sendChatMessage();
        }

        async function sendChatMessage() {
            const inputEl = document.getElementById("chat-input-field");
            const text = inputEl.value.trim();
            if (!text) return;

            const chatBox = document.getElementById("chat-messages-box");

            // Render User Bubble
            chatBox.innerHTML += `<div class="message-bubble user">${text}</div>`;
            inputEl.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const json = await res.json();
                if (json.status === 'success') {
                    // Render Bot Bubble
                    chatBox.innerHTML += `<div class="message-bubble bot">${json.reply}</div>`;
                    chatBox.scrollTop = chatBox.scrollHeight;
                }
            } catch (err) {
                console.error("Error sending message:", err);
            }
        }

        // CANVAS CHART DRAWER
        function renderProgressChart() {
            const canvas = document.getElementById("progressCanvas");
            if (!canvas) return;
            const ctx = canvas.getContext("2d");

            canvas.width = canvas.parentElement.clientWidth - 60;
            canvas.height = 200;

            const days = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"];
            const xpValues = [120, 250, 180, 320, 290, 410, 380];
            const maxVal = 500;

            const stepX = canvas.width / (days.length - 1);

            // Draw Gradient Line
            ctx.beginPath();
            ctx.strokeStyle = '#6366f1';
            ctx.lineWidth = 4;

            for (let i = 0; i < days.length; i++) {
                const x = i * stepX;
                const y = canvas.height - (xpValues[i] / maxVal) * (canvas.height - 40) - 20;

                if (i === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.stroke();

            // Draw Points & Labels
            for (let i = 0; i < days.length; i++) {
                const x = i * stepX;
                const y = canvas.height - (xpValues[i] / maxVal) * (canvas.height - 40) - 20;

                ctx.beginPath();
                ctx.fillStyle = '#ec4899';
                ctx.arc(x, y, 6, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = '#94a3b8';
                ctx.font = '12px Plus Jakarta Sans';
                ctx.fillText(days[i], x - 15, canvas.height - 2);
            }
        }
    </script>
</body>
</html>
"""

# =============================================================================
# 6. APPLICATION ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    print("=====================================================================")
    print("  EDUSPARK ENGLISH PLATFORM - STARTING FLASK SERVER (PYTHON 3.10)   ")
    print("=====================================================================")
    print("  Localhost Server: http://127.0.0.1:5000")
    print("=====================================================================")
    app.run(debug=True, host="0.0.0.0", port=5000)