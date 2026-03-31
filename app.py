import streamlit as st
import tempfile
import os
from pdf_parser import extract_from_pdf, get_pdf_metadata
from ai_engine import generate_ddr, validate_ddr_sections
from report_generator import create_ddr_report

# ── Page Config ──
st.set_page_config(
    page_title="RoofScan AI — Smart Diagnostic Reports",
    page_icon="🏗️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── CSS ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
    }

    /* Main container */
    .block-container {
        padding-top: 2rem !important;
        max-width: 780px !important;
    }

    /* Hero */
    .hero-wrap {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem 1rem;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        color: #a0c4ff;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 0.3rem 0.9rem;
        border-radius: 20px;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.2;
        margin-bottom: 0.5rem;
    }
    .hero-title span {
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-sub {
        color: #94a3b8;
        font-size: 1rem;
        font-weight: 400;
        margin-bottom: 0.3rem;
    }

    /* Step indicator */
    .step-row {
        display: flex;
        gap: 0.5rem;
        margin: 1.2rem 0;
        justify-content: center;
        flex-wrap: wrap;
    }
    .step-item {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 0.78rem;
        color: #475569;
        font-weight: 500;
    }
    .step-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #334155;
    }
    .step-dot.active {
        background: #60a5fa;
        box-shadow: 0 0 6px #60a5fa88;
    }
    .step-arrow { color: #334155; font-size: 0.7rem; }

    .card-title {
        font-size: 0.8rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.8rem;
    }

    /* Upload labels */
    .upload-label {
        font-size: 0.95rem;
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 0.4rem;
    }
    .upload-hint {
        font-size: 0.78rem;
        color: #64748b;
        margin-top: 0.3rem;
    }
    .file-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(96,165,250,0.12);
        border: 1px solid rgba(96,165,250,0.3);
        color: #93c5fd;
        font-size: 0.82rem;
        font-weight: 500;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin-top: 0.5rem;
    }

    /* Stats */
    .stat-box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 0.9rem 1rem;
        text-align: center;
    }
    .stat-num {
        font-size: 1.5rem;
        font-weight: 700;
        color: #60a5fa;
    }
    .stat-label {
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 0.1rem;
    }

    /* Section check pills */
    .check-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 0.8rem 0;
    }
    .check-pill {
        font-size: 0.75rem;
        font-weight: 500;
        padding: 0.25rem 0.7rem;
        border-radius: 20px;
        background: rgba(16,185,129,0.12);
        border: 1px solid rgba(16,185,129,0.3);
        color: #6ee7b7;
    }
    .check-pill.missing {
        background: rgba(239,68,68,0.12);
        border: 1px solid rgba(239,68,68,0.3);
        color: #fca5a5;
    }

    .custom-divider {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.07);
        margin: 1.5rem 0;
    }

    .footer {
        text-align: center;
        padding: 1.5rem 0 2rem 0;
        color: #334155;
        font-size: 0.8rem;
    }
    .footer a { color: #475569; text-decoration: none; }

    /* Streamlit component overrides */
    .stTextInput input {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }
    .stTextInput label { color: #94a3b8 !important; }
    .stExpander {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
    }
    .stProgress > div > div {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6) !important;
        border-radius: 4px !important;
    }
    div[data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.03) !important;
        border: 1.5px dashed rgba(255,255,255,0.15) !important;
        border-radius: 12px !important;
        padding: 0.5rem !important;
    }
    div[data-testid="stFileUploader"]:hover {
        border-color: rgba(96,165,250,0.4) !important;
    }
    .stTextArea textarea {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
        color: #cbd5e1 !important;
        font-size: 0.88rem !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        letter-spacing: 0.02em !important;
    }
    .stButton > button:hover { opacity: 0.88 !important; }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        padding: 0.75rem !important;
    }
    p, li, span, label { color: #94a3b8 !important; }
    h1, h2, h3 { color: #e2e8f0 !important; }
    .stAlert { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">🏗️ Urbanroof · Powered by AI</div>
    <div class="hero-title">RoofScan <span>AI</span></div>
    <div class="hero-sub">Upload your inspection &amp; thermal reports — get a complete diagnostic in seconds.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="step-row">
    <div class="step-item"><div class="step-dot active"></div> Upload PDFs</div>
    <div class="step-arrow">›</div>
    <div class="step-item"><div class="step-dot"></div> AI Analyses</div>
    <div class="step-arrow">›</div>
    <div class="step-item"><div class="step-dot"></div> DDR Generated</div>
    <div class="step-arrow">›</div>
    <div class="step-item"><div class="step-dot"></div> Download Report</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# ── API Key ──
with st.expander("🔑  API Key Setup  (click to configure)", expanded=False):
    st.markdown("<br>", unsafe_allow_html=True)
    api_key_input = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_xxxxxxxxxxxxxxxxxxxxxxxx",
        help="Get your free key at console.groq.com"
    )
    if api_key_input:
        os.environ["GROQ_API_KEY"] = api_key_input
        st.success("✅ API Key saved for this session")
    else:
        st.caption("👉 Don't have a key? Get one free at [console.groq.com](https://console.groq.com)")

st.markdown("<br>", unsafe_allow_html=True)

# ── Upload ──
st.markdown('<div class="card-title">📂 Upload Documents</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="medium")
with col1:
    st.markdown('<div class="upload-label">📋 Inspection Report</div>', unsafe_allow_html=True)
    inspection_pdf = st.file_uploader("inspection", type="pdf", key="inspection", label_visibility="collapsed")
    if inspection_pdf:
        st.markdown(f'<div class="file-pill">✓ &nbsp;{inspection_pdf.name}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="upload-hint">Site observations &amp; issue descriptions</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="upload-label">🌡️ Thermal Report</div>', unsafe_allow_html=True)
    thermal_pdf = st.file_uploader("thermal", type="pdf", key="thermal", label_visibility="collapsed")
    if thermal_pdf:
        st.markdown(f'<div class="file-pill">✓ &nbsp;{thermal_pdf.name}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="upload-hint">Temperature readings &amp; thermal findings</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Generate ──
generate_clicked = st.button("⚡  Generate Diagnostic Report", use_container_width=True)

if generate_clicked:
    if not os.environ.get("GROQ_API_KEY"):
        st.error("Please enter your Groq API key in the setup section above.")
        st.stop()
    if not inspection_pdf:
        st.error("Please upload the Inspection Report PDF.")
        st.stop()
    if not thermal_pdf:
        st.error("Please upload the Thermal Report PDF.")
        st.stop()

    progress = st.progress(0)
    status = st.empty()
    insp_path = therm_path = None

    try:
        status.info("📥  Reading your documents...")
        progress.progress(10)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f1:
            f1.write(inspection_pdf.read())
            insp_path = f1.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f2:
            f2.write(thermal_pdf.read())
            therm_path = f2.name

        status.info("🔍  Extracting text and images from both PDFs...")
        progress.progress(28)

        insp_text,  insp_images  = extract_from_pdf(insp_path,  "extracted_images/inspection")
        therm_text, therm_images = extract_from_pdf(therm_path, "extracted_images/thermal")
        insp_meta  = get_pdf_metadata(insp_path)
        therm_meta = get_pdf_metadata(therm_path)
        all_images = insp_images + therm_images

        progress.progress(45)

        # Stats
        c1, c2, c3, c4 = st.columns(4)
        total_chars = len(insp_text) + len(therm_text)
        for col, num, label in [
            (c1, insp_meta["pages"],  "Inspection Pages"),
            (c2, therm_meta["pages"], "Thermal Pages"),
            (c3, len(all_images),     "Images Found"),
            (c4, f"{total_chars//1000}k", "Chars Read"),
        ]:
            with col:
                st.markdown(f'<div class="stat-box"><div class="stat-num">{num}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        status.info("🧠  AI is reading and analysing — this takes about 20–30 seconds...")
        progress.progress(62)

        ddr_content = generate_ddr(insp_text, therm_text)
        progress.progress(82)

        status.info("📝  Building your Word document...")
        report_path = create_ddr_report(ddr_content, all_images, "outputs/RoofScan_DDR_Report.docx")
        progress.progress(100)

        status.empty()
        progress.empty()

        st.success("🎉  Your Detailed Diagnostic Report is ready!")

        # Section pills
        section_check    = validate_ddr_sections(ddr_content)
        missing_sections = [s for s, f in section_check.items() if not f]
        pills = '<div class="check-grid">'
        for section, found in section_check.items():
            label = section.replace("PROPERTY ", "").replace(" INFORMATION", "").title()
            css   = "check-pill" if found else "check-pill missing"
            icon  = "✓" if found else "✗"
            pills += f'<span class="{css}">{icon} {label}</span>'
        pills += '</div>'
        st.markdown(pills, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Download
        with open(report_path, "rb") as f:
            st.download_button(
                label="⬇️  Download Full DDR Report (.docx)",
                data=f,
                file_name="RoofScan_DDR_Report.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander("📄  Preview Report Text", expanded=False):
            st.text_area("", ddr_content, height=480, label_visibility="collapsed")

        if all_images:
            st.markdown(f"<br><div class='card-title'>🖼️ Extracted Images ({len(all_images)} total — all included in report)</div>", unsafe_allow_html=True)
            img_cols = st.columns(min(3, len(all_images)))
            for idx, img_path in enumerate(all_images[:6]):
                with img_cols[idx % 3]:
                    try:
                        st.image(img_path, use_container_width=True)
                    except Exception:
                        st.caption(f"[{os.path.basename(img_path)}]")
            if len(all_images) > 6:
                st.caption(f"+ {len(all_images) - 6} more images included in the downloaded report.")

    except ValueError as ve:
        status.empty(); progress.empty()
        st.error(f"API Key Error: {ve}")
        st.info("Make sure your Groq API key is correct. Get one free at console.groq.com")
    except Exception as e:
        status.empty(); progress.empty()
        st.error(f"Something went wrong: {str(e)}")
        st.info("💡 Tip: Make sure both PDFs contain readable text, not scanned images.")
    finally:
        for p in [insp_path, therm_path]:
            try:
                if p: os.unlink(p)
            except Exception:
                pass

# ── Footer ──
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    RoofScan AI &nbsp;·&nbsp; Built for Urbanroof Pvt Ltd &nbsp;·&nbsp;
    Powered by <a href="https://console.groq.com" target="_blank">Groq</a> &amp; Llama 3.3
</div>
""", unsafe_allow_html=True)
