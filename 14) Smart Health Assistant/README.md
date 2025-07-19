
# 🩺 Smart Health Assistant

A visually engaging, multi-agent Streamlit application that provides personalized health plans, including BMI analysis, health recommendations, meal planning, and workout scheduling. Built using a sequential agent conversation pattern and powered by Gemini 1.5 Flash API.

---

## 🚀 Features

- **User Proxy Agent**: Collects user data (weight, height, age, gender, dietary preference)
- **BMI Tool & Agent**: Calculates BMI and provides health recommendations
- **Diet Planner Agent**: Suggests meal plans based on BMI and dietary preferences
- **Workout Scheduler Agent**: Creates a weekly workout plan tailored to age, gender, and meal plan
- **Attractive UI**: Modern, card-based layout with icons and styled download button
- **Downloadable Health Plan**: Export your personalized plan as a text file

---

## 🧠 Agent Workflow (Sequential Conversation Pattern)

1. **User Proxy Agent**: Collects user inputs (weight, height, age, gender, dietary preference)
2. **BMI Tool**: Calculates BMI using:
   ```
   BMI = Weight (kg) / (Height (m))^2
   ```
3. **BMI Agent**: Analyzes BMI, categorizes it, and provides health recommendations
4. **Diet Planner Agent**: Suggests meal plans based on BMI insights and dietary preferences
5. **Workout Scheduler Agent**: Creates a weekly workout plan based on meal plan, age, and gender

---

## 🖥️ Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd "14) Smart Health Assistant"
```

### 2. Install Dependencies
It is recommended to use a virtual environment.
```bash
pip install -r requirements.txt
```

### 3. Get a Gemini API Key
- Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to generate your Gemini 1.5 Flash API key.

### 4. Run the App
```bash
streamlit run app.py
```

---

## 📝 Usage

1. Enter your Gemini API key in the sidebar.
2. Fill in your health details (weight, height, age, gender, dietary preference).
3. Click **"Generate Health Plan"**.
4. View your personalized recommendations:
   - BMI analysis and health advice
   - Tailored meal plan
   - Weekly workout schedule
5. Download your complete health plan as a text file.

---

## 📦 Requirements

- Python 3.8+
- [pyautogen](https://pypi.org/project/pyautogen/)
- [streamlit](https://streamlit.io/)
- [google-generativeai](https://pypi.org/project/google-generativeai/)
- [streamlit-extras](https://github.com/arnaudmiribel/streamlit-extras)

Install all dependencies with:
```bash
pip install -r requirements.txt
```

---

## 🛠️ Customization

- Customize the UI via CSS and Streamlit Extras in `app.py`
- Modify agent prompts and logic for advanced health planning

---

## 📄 License

This project is for educational and demonstration purposes.
