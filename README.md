# MediChat 🏥 — AI Medical Assistant

> A conversational AI health assistant powered by **GPT-4o** — supports 10 medical specialties, 3 response tones, and 3 languages, with strict medical-only guardrails.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/GPT--4o-412991?style=for-the-badge&logo=openai&logoColor=white)

---

## 🔍 What It Does

MediChat is a focused AI health assistant that answers medical and health questions in plain language. Users can select their preferred medical specialty, response tone, and language — and get evidence-based, compassionate health information.

> ⚠️ **Disclaimer:** MediChat provides general health information only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for personal medical concerns.

---

## ✨ Features

- 🩺 **10 Medical Specialties** — General Medicine, Cardiology, Neurology, Dermatology, Pediatrics, Orthopedics, Psychiatry, Nutrition, Gynecology, Oncology
- 🗣️ **3 Response Tones** — Simple (plain language), Clinical (medical terminology), Detailed (in-depth)
- 🌐 **3 Languages** — English, Hindi, Marathi
- 💡 **Quick Question Buttons** — One-click prompts for common health topics
- 🔒 **Strict Medical Guardrails** — Refuses all non-medical questions by design
- 🚨 **Emergency Detection** — Immediately directs to emergency services for urgent symptoms
- 🗑️ **Clear Chat** — Reset conversation anytime

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| LLM | OpenAI GPT-4o |
| Frontend | Streamlit |
| Config | python-dotenv |

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/medichat.git
cd medichat
```

### 2. Set up environment
```bash
cp .env.example .env
# Add your OpenAI API key to .env
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run medichat.py
```

---

## 📁 Project Structure

```
medichat/
├── medichat.py        # Main Streamlit app
├── requirements.txt
├── .env.example       # API key template
└── .gitignore
```

---

## 💬 Example Interactions

**User:** What are the early signs of diabetes?
**MediChat (Simple tone):** Early signs include increased thirst, frequent urination, unexplained fatigue, blurry vision, and slow-healing wounds. If you notice these, visit a doctor for a blood sugar test...

**User (non-medical):** Who won the IPL?
**MediChat:** I'm a medical assistant. I can only help with health and medical questions. Please ask me something related to health, symptoms, medications, or wellness.

---

## 🔒 Design: Medical-Only Guardrails

The system prompt strictly instructs GPT-4o to:
- Answer **only** health and medical questions
- Refuse all off-topic requests (sports, coding, geography, etc.) with a fixed response
- Never diagnose or prescribe — only educate and inform
- Immediately flag emergencies (chest pain, suicidal ideation) with crisis resources
