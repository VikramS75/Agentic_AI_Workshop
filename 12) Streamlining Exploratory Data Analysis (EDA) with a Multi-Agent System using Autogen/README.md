# 📊 Streamlining Exploratory Data Analysis (EDA) with a Multi-Agent System using Autogen

## 🧠 Overview  
Exploratory Data Analysis (EDA) is a vital step in data science that helps uncover the structure, patterns, and insights within a dataset before modeling. This project automates and enhances EDA using a **multi-agent system** built with [Microsoft Autogen](https://github.com/microsoft/autogen) and integrated with **Google Gemini** for intelligent processing.

Each agent is responsible for a distinct task, ensuring a modular, scalable, and high-quality EDA process — all accessible through a modern **Streamlit interface**.

---

## 🚀 Key Features

- **🧹 Data Preparation Agent**  
  Cleans and preprocesses data by handling missing values, correcting data types, and removing duplicates.

- **📈 EDA Agent**  
  Performs statistical analysis, extracts insights, and suggests visualizations.

- **📝 Report Generator Agent**  
  Compiles a structured and insightful EDA report.

- **🔍 Critic Agent**  
  Reviews outputs and improves clarity, accuracy, and usefulness.

- **⚙️ Executor Agent**  
  Validates preprocessing and EDA code to ensure correctness.

- **🧑‍💼 Admin Agent**  
  Coordinates communication and workflow among agents.

- **💻 Streamlit UI**  
  User-friendly web interface for uploading datasets and viewing results interactively.

---

## ⚙️ How It Works

1. Upload a **CSV file** via the web interface.
2. Preview the dataset.
3. Click **"Run Agentic EDA"** to trigger the multi-agent workflow:
   - Data is cleaned and preprocessed.
   - EDA is performed, and insights are extracted.
   - A comprehensive report is generated.
   - The critic agent reviews and enhances the report.
   - The executor agent validates the code logic.
4. View results and feedback in organized, expandable sections.

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
\`\`\`bash
git clone <repo-url>
cd "12) Streamlining Exploratory Data Analysis (EDA) with a Multi-Agent System using Autogen"
\`\`\`

### 2. Install Dependencies
Make sure you have **Python 3.8+** installed:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Add Your Google Gemini API Key  
Open \`app.py\` and replace the placeholder:
\`\`\`python
api_key = "YOUR_GEMINI_API_KEY_HERE"
\`\`\`

### 4. Run the Application
\`\`\`bash
streamlit run app.py
\`\`\`
Open your browser at \`http://localhost:8501\`.

---

## 🧪 Sample Dataset

Use the following sample CSV to test the system:

\`\`\`csv
OrderID,Customer,Product,Category,Quantity,Price,OrderDate,Country
1001,Alice,Smartphone,Electronics,1,699,2024-01-15,USA
1002,Bob,Laptop,Electronics,2,1200,2024-01-17,Canada
1003,Charlie,Desk Chair,Furniture,1,150,2024-01-18,USA
1004,David,Notebook,Stationery,5,3,2024-01-19,UK
1005,Eva,Pen,Stationery,10,1.5,2024-01-20,India
1006,Frank,Tablet,Electronics,1,350,2024-01-21,USA
1007,Grace,Bookshelf,Furniture,1,80,2024-01-22,Canada
1008,Hannah,Monitor,Electronics,1,200,2024-01-23,UK
1009,Ian,Desk,Furniture,1,250,2024-01-24,India
1010,Jane,Backpack,Accessories,2,40,2024-01-25,USA
\`\`\`

---

## 📁 Project Structure

\`\`\`
├── app.py                # Main Streamlit application
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── sample_data.csv       # Sample dataset (optional)
\`\`\`

---

## 📄 License  
This project is intended for **educational and research purposes only**.

---

## 🙌 Acknowledgements

- [Microsoft Autogen](https://github.com/microsoft/autogen) – Multi-agent orchestration framework  
- [Google Gemini API](https://ai.google.dev/gemini-api/docs/get-started) – Generative AI for enhanced data understanding  
- [Streamlit](https://streamlit.io/) – UI framework for rapid data apps
