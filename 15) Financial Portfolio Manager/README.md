# 💼 Financial Portfolio Manager

An AI-powered Streamlit app that helps users analyze and optimize their investment portfolios using a multi-agent, agentic workflow. The system leverages **Google Gemini LLM** and the **Autogen framework** to provide personalized financial analysis and recommendations.

---

## 🚀 Features

- **Modern, Attractive UI**  
  Clean, user-friendly interface with sidebar, icons, and sectioned forms.

- **Agentic Collaboration**  
  Multiple AI agents collaborate to analyze your portfolio and generate tailored investment advice.

- **Dynamic Workflow**  
  The system dynamically routes your case to growth or value investment agents based on your profile.

- **Personalized Report**  
  Receive a comprehensive, markdown-formatted financial report with actionable recommendations.

- **Privacy First**  
  No user data is stored.

---

## 🧩 How It Works

1. **User Input**  
   Enter your personal and portfolio details in the app.

2. **Portfolio Analysis Agent**  
   Summarizes your portfolio and determines your investment category (Growth or Value).

3. **Dynamic Routing**  
   Based on the analysis, the workflow is routed to either the Growth or Value Investment Agent.

4. **Investment Agents**  
   Suggest high-growth or stable investment options tailored to your profile.

5. **Investment Advisor Agent**  
   Compiles all insights into a detailed, easy-to-read report.

---

## 🖥️ Setup Instructions

### 1. Clone the Repository
```bash
git clone <repo-url>
cd "15) Financial Portfolio Manager"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Gemini API Key
Edit the `app.py` file and replace the placeholder in `default_gemini_api_key` with your actual Gemini API key.

### 4. Run the App
```bash
streamlit run app.py
```

---

## 📝 Sample Input

**Personal Information:**
- Annual Salary (₹): `1800000`
- Your Age: `32`
- Annual Expenses (₹): `700000`
- Risk Tolerance: `Moderate`
- Financial Goals:
  ```
  - Buy a house in 7 years
  - Save for children's education in 10 years
  - Retire at age 60 with ₹2 crore corpus
  ```

**Portfolio Details:**
- Mutual Funds:
  ```
  Axis Bluechip - Equity - ₹3L
  HDFC Hybrid - Balanced - ₹1.5L
  SBI Small Cap - Equity - ₹1L
  ```
- Stocks:
  ```
  Infosys - 20 shares - ₹1450
  HDFC Bank - 15 shares - ₹1600
  Reliance - 10 shares - ₹2500
  ```
- Real Estate:
  ```
  Residential Apartment - Pune - ₹25L
  ```
- Fixed Deposit (Total ₹): `400000`

---

## 🧠 Agentic Workflow (Under the Hood)

- **User Proxy Agent**  
  Initiates the process.

- **Portfolio Analysis Agent**  
  Analyzes your portfolio and determines investment strategy.

- **Growth/Value Investment Agents**  
  Provide recommendations based on your profile.

- **Investment Advisor Agent**  
  Compiles the final report.

> *Note: The current implementation uses sequential agent calls. For advanced agent collaboration (GroupChat, StateFlow), see the Autogen documentation.*

---