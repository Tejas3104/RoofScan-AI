from groq import Groq
import os


def generate_ddr(inspection_text: str, thermal_text: str) -> str:
    """
    Send inspection + thermal text to Groq API (free) and return structured DDR content.
    """
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set.")

    client = Groq(api_key=api_key)

    prompt = f"""
You are an expert property inspection analyst working for Urbanroof, a professional roofing and property inspection company.

You have been given two documents:

=== INSPECTION REPORT ===
{inspection_text}

=== THERMAL REPORT ===
{thermal_text}

Your task is to generate a comprehensive DDR (Detailed Diagnostic Report) that merges both documents into a single, professional, client-ready report.

Generate the report with EXACTLY these 7 sections using these exact headings:

1. PROPERTY ISSUE SUMMARY
Write a concise high-level overview of all major issues found across the property.

2. AREA-WISE OBSERVATIONS
List observations grouped by area/location (e.g., Roof, Walls, Basement, etc.).
For each area, combine relevant findings from both the inspection and thermal reports.
Mention "[Image Available]" next to any observation that has a corresponding image in the documents.

3. PROBABLE ROOT CAUSE
For each major issue, explain the most likely root cause based on the evidence in the documents.

4. SEVERITY ASSESSMENT
Assess each issue as High / Medium / Low severity.
Provide reasoning for each severity rating based on the data.

5. RECOMMENDED ACTIONS
List specific, actionable steps the client should take to address each issue.
Prioritize by severity (High first).

6. ADDITIONAL NOTES
Include any extra observations, seasonal considerations, maintenance tips, or context from the documents.

7. MISSING OR UNCLEAR INFORMATION
Explicitly list any information that was expected but not found in the documents.
Write "Not Available" for each missing item.
If inspection and thermal data conflict on any point, mention the conflict clearly here.

=== STRICT RULES ===
- Do NOT invent or assume any facts not present in the documents
- If information is missing → write "Not Available"
- If data conflicts between the two reports → state the conflict explicitly
- Avoid duplicate observations — merge related points
- Use simple, client-friendly language
- Avoid unnecessary technical jargon
- Keep the tone professional and helpful
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Best free model on Groq
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000,
        temperature=0.3
    )

    return response.choices[0].message.content


def validate_ddr_sections(ddr_text: str) -> dict:
    """
    Check that all 7 required sections are present in the generated DDR.
    Returns a dict with section names and whether they were found.
    """
    required_sections = [
        "PROPERTY ISSUE SUMMARY",
        "AREA-WISE OBSERVATIONS",
        "PROBABLE ROOT CAUSE",
        "SEVERITY ASSESSMENT",
        "RECOMMENDED ACTIONS",
        "ADDITIONAL NOTES",
        "MISSING OR UNCLEAR INFORMATION"
    ]
    results = {}
    for section in required_sections:
        results[section] = section in ddr_text.upper()
    return results
