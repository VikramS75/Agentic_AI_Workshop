# 🧾 Bill Management Agent

A modern, AI-powered Streamlit app to help users efficiently track and analyze their expenses by processing bill images. The app uses a **multi-agent collaboration** approach to extract, categorize, and summarize spending—providing actionable insights into your financial habits.

---

## 🚀 Features

- 📷 **Bill Image Upload** – Upload a photo or scan of your bill (JPG/PNG).
- 🧠 **AI-Powered Extraction** – Uses Google Gemini Vision to extract items and costs from the image.
- 📊 **Automatic Categorization** – Groups expenses into categories: Groceries, Dining, Utilities, Shopping, Entertainment, Others.
- 📈 **Spending Summary** – Provides total per category, overall total, and highlights unusual/high spending.
- 🤖 **Agent Collaboration** – Simulated multi-agent chat for explainability and transparency.
- 💻 **Modern UI** – Card-based, responsive, and delightful interface using Streamlit.

---

## 🛠️ Setup Instructions

1. **Clone the Repository**

```bash
git clone <repo-url>
cd "16) Bill Managing Agent"
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure API Key**

- Replace the placeholder `GEMINI_API_KEY` in `app.py` with your actual [Google Gemini API key](https://aistudio.google.com/app/apikey).

4. **Run the App**

```bash
streamlit run app.py
```

---

## 🖼️ How to Use

1. Launch the app in your browser.
2. Click **"Upload your bill"** and select a JPG/PNG image.
3. Let the AI process and categorize your expenses.
4. View:
   - Categorized items
   - Spending breakdown by category
   - Agent conversation log for transparency

---

## 🤖 Agent Workflow

- **User Proxy Agent** – Submits the bill image.
- **Bill Processing Agent** – Extracts and categorizes the bill.
- **Expense Summarization Agent** – Analyzes the results and provides a summary.
- **Group Chat Manager** – Coordinates the agent communication (simulated).

---

## 📦 Requirements

- Python 3.8+
- Streamlit
- google-generativeai
- python-dotenv
- pyautogen
- Pillow

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## 🧾 Example Bill

The app works best with clean, itemized bills like:

| Item           | Cost |
|----------------|------|
| Milk           | 50   |
| Bread          | 30   |
| Pizza          | 300  |
| Electricity    | 1200 |
| T-shirt        | 500  |
| Movie Ticket   | 250  |
| Parking        | 40   |

---

## 🙏 Credits

Built using:

- [Streamlit](https://streamlit.io/)
- [Google Gemini](https://aistudio.google.com/app/apikey)
- [Microsoft AutoGen](https://github.com/microsoft/autogen)

UI inspired by modern dashboard best practices.

---