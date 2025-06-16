import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


def extract_keywords(text: str, max_keywords: int = 8) -> list[str]:
    model = genai.GenerativeModel(
        "models/gemini-1.5-flash"
    )

    prompt = (
        f"You are a video content assistant. Your job is to extract up to "
        f"{max_keywords} visually relevant keywords or phrases from the "
        "following video narration.\n"
        "The keywords should describe visual scenes, objects, locations, "
        "emotions, or atmosphere that would be useful for video generation "
        "or stock footage curation.\n"
        "Return the keywords in English, as a comma-separated list, with no "
        "explanations.\n"
        f"Narration: {text}"
    )

    try:
        response = model.generate_content(prompt)
        keywords_text = response.text.strip()
        keywords = [kw.strip()
                    for kw in keywords_text.split(",") if kw.strip()]
        return keywords
    except Exception:
        return []
