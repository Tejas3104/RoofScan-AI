# 🏠 DDR Report Generator — Urbanroof AI System

An AI-powered system that converts raw site inspection documents into structured, client-ready Detailed Diagnostic Reports (DDR).

## 🎯 What It Does

Upload two PDF documents:
- **Inspection Report** — site observations and issue descriptions
- **Thermal Report** — temperature readings and thermal findings

The system will:
1. Extract all text and images from both PDFs
2. Send the data to Claude AI for intelligent analysis
3. Generate a structured 7-section DDR report
4. Output a professional Word document (.docx)

## 📄 DDR Output Structure

1. Property Issue Summary
2. Area-wise Observations (with images)
3. Probable Root Cause
4. Severity Assessment (High / Medium / Low)
5. Recommended Actions
6. Additional Notes
7. Missing or Unclear Information

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ddr-generator.git
cd ddr-generator
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your API key
```bash
# Option A: Set environment variable
export GROQ_API_KEY=gsk_your_key_here

# Option B: Enter it in the app UI (Configuration section)
```

### 4. Run the app
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## 📁 Project Structure

```
ddr-generator/
├── app.py                  # Streamlit web UI
├── pdf_parser.py           # PDF text + image extraction
├── ai_engine.py            # Claude AI integration
├── report_generator.py     # Word document generation
├── requirements.txt        # Python dependencies
├── .env.example            # API key template
├── .streamlit/
│   └── secrets.toml        # Streamlit Cloud secrets template
├── extracted_images/       # Auto-created during processing
│   ├── inspection/
│   └── thermal/
└── outputs/                # Generated reports saved here
```

## ☁️ Deploy to Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. In **App Settings > Secrets**, add:
   ```
   ANTHROPIC_API_KEY = "sk-ant-your-key-here"
   ```
5. Deploy → get your live link ✅

## 🔑 Getting an API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up / Log in
3. Go to **API Keys** → **Create Key**
4. Copy and use it in the app

## ⚠️ Limitations

- Works best with text-based PDFs (not scanned/image-only PDFs)
- Very large PDFs (50+ pages) may be slower
- Image extraction depends on how images are embedded in the PDF
- Report quality depends on the detail in the source documents

## 🔧 How to Improve

- Add OCR support for scanned PDFs (using `pytesseract`)
- Add table extraction from PDFs
- Support multiple inspection reports at once
- Add PDF output in addition to Word
- Add email sending functionality

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| UI | Streamlit |
| PDF Parsing | PyMuPDF (fitz) |
| AI Engine | Groq API (Free) |
| Report Output | python-docx |
| Language | Python 3.10+ |

---

Built for Urbanroof Pvt Ltd — AI Intern Assignment 2026
