# 🧠 Smart Medical Agentic Assistant

An AI-powered multi-agent medical assistant capable of performing **symptom diagnosis**, **treatment planning**, and **hospital recommendations** using **AutoGen**, **ChromaDB**, **MemGPT**, and **Streamlit**.

> Built as part of a practical internship project to explore agentic AI in healthcare.

---

## 🚀 Features

- 🔬 Symptom checker using agentic reasoning
- 💊 Treatment recommendation based on context-aware multi-agent planning
- 🏥 Nearest hospital suggestion using Google Maps API
- 🧠 Long-term memory with ChromaDB
- 🧠 Context summarization and recall using MemGPT
- 📄 Generates a downloadable PDF medical report via WeasyPrint
- 🖥️ Clean UI using Streamlit

---

## 📦 Tech Stack

- **Python 3.10+**
- [AutoGen](https://github.com/microsoft/autogen)
- [ChromaDB](https://www.trychroma.com/)
- [MemGPT](https://github.com/cpacker/MemGPT)
- [Streamlit](https://streamlit.io/)
- [WeasyPrint](https://weasyprint.org/) (for PDF generation)
- Google Maps API (for hospital location)

---

## 🛠️ Setup Instructions

```bash
# 1. Clone the repo
git clone https://github.com/Prabhu1702/smart-medical-agentic-assistant.git
cd smart-medical-agentic-assistant

# 2. Create virtual environment
python -m venv .venv
# Activate it:
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
