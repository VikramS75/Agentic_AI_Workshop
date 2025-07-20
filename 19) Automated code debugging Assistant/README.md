# 🤖 Automated Code Debugging Assistant

A visually-attractive, AI-powered **Streamlit** app that analyzes and corrects Python code using **CrewAI** agents and **Gemini LLM**. The assistant identifies syntax and logical errors, suggests fixes, and provides corrected code—all in a modern, user-friendly interface.

---

## 🚀 Features

- **AI Agents:**
  - 🔍 *Python Static Analyzer*: Finds issues in code without executing it
  - 🛠️ *Python Code Fixer*: Suggests and applies corrections
  - 👨‍💼 *Code Review Manager*: Oversees the process
- **Sequential Task Flow:** Ensures analysis and correction are performed in logical order
- **Modern UI:** Sidebar, card layout, custom colors, and icons
- **Lightweight Setup:** No ONNX/ChromaDB required

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) – UI development
- [CrewAI](https://github.com/joaomdmoura/crewAI) – Agent framework
- [Gemini LLM](https://ai.google.dev/gemini-api/docs) – Language model
- Python 3.8+

---

## ⚡ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd "19) Automated code debugging Assistant"
   ```

2. **(Optional) Create and activate a virtual environment**
   ```bash
   python -m venv venv

   # On Windows:
   venv\Scripts\activate

   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your API keys**
   - Open `app.py` and set your `GOOGLE_API_KEY` for Gemini LLM.

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

---

## 📝 Usage Guide

1. Paste your Python code into the text input area.
2. Click the **"Analyze & Fix"** button.
3. Review the issues detected and view the corrected code displayed below.

---

## 💡 Example

**Input:**
```python
def fibonacci_iterative(n):
    if n < 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    fib_sequence = [0, 1]
    for i in range(2, n):
    next_fib = fib_sequence[-1] + fib_sequence[-2]
    fib_sequence.append(next_fib)
    return fib_sequence
```

**Output:**
```python
def fibonacci_iterative(n):
    if n < 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    fib_sequence = [0, 1]
    for i in range(2, n):
        next_fib = fib_sequence[-1] + fib_sequence[-2]
        fib_sequence.append(next_fib)
    return fib_sequence
```

---