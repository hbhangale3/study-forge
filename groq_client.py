import os, json, re
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

_client = None

def get_client():
    global _client
    if _client is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not set. Deep Mode (AI evaluation) requires a valid API key. "
                "Get one at https://console.groq.com and set it in .env file."
            )
        try:
            _client = Groq(api_key=api_key)
        except TypeError as error:
            raise RuntimeError(
                "Failed to initialize Groq client. This often happens when the installed "
                "httpx version is incompatible with groq==0.9.0. Install `httpx==0.27.0` "
                "and retry."
            ) from error
    return _client

def _strip_json_fences(text):
    """Strip markdown code fences and extract JSON."""
    text = text.strip()
    # Remove ```json ... ``` or ``` ... ``` wrappers
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    return text.strip()

def evaluate_answer(card, user_answer):
    """Evaluate user's free-text answer. Returns dict with score 0-5, feedback, missed_points."""
    client = get_client()

    prompt = f"""You are a strict but fair technical interviewer evaluating a Java/System Design answer.

Question: {card['question']}
Expected Answer: {card['answer']}
Code Example: {card.get('code', 'N/A')}
Student's Answer: {user_answer}

Evaluate and return ONLY valid JSON with no extra text:
{{
  "score": <integer 0-5>,
  "feedback": "<one concise sentence>",
  "missed_points": ["<point1>", "<point2>"]
}}

Scoring: 5=perfect, 4=correct minor gaps, 3=correct missing detail, 2=partial, 1=shows some understanding, 0=wrong/blank"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    text = _strip_json_fences(response.choices[0].message.content)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "score": 2,
            "feedback": "Could not parse AI evaluation response. Please try again.",
            "missed_points": []
        }

def generate_followup(card):
    """Generate a harder follow-up question based on a card the user got right."""
    client = get_client()

    prompt = f"""You are a senior software engineer interviewer.

The student just correctly answered this question:
Topic: {card['subcategory']}
Question: {card['question']}

Generate ONE harder follow-up question that probes deeper understanding or asks about edge cases, tradeoffs, or real-world application. Return ONLY the question text, nothing else."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def chat_about_card(card, user_message, history=None, user_answer=None, evaluation=None):
    """Interactive chat about a flashcard topic. Returns assistant reply string."""
    client = get_client()
    if history is None:
        history = []

    context_parts = [
        f"Topic: {card.get('subcategory', 'Unknown')}",
        f"Question: {card['question']}",
        f"Expected Answer: {card['answer']}",
    ]
    if card.get('code'):
        context_parts.append(f"Code Example:\n{card['code']}")
    if card.get('hint'):
        context_parts.append(f"Hint: {card['hint']}")
    if user_answer:
        context_parts.append(f"Student's Submitted Answer: {user_answer}")
    if evaluation:
        context_parts.append(
            f"Prior Evaluation: Score {evaluation.get('score')}/5 — {evaluation.get('feedback', '')}"
        )
        if evaluation.get('missed_points'):
            context_parts.append(f"Missed Points: {', '.join(evaluation['missed_points'])}")

    context = '\n'.join(context_parts)

    system_prompt = (
        "You are a technical interview coach and study tutor. "
        "Answer based primarily on the flashcard context provided. "
        "Be concise, practical, and accurate. "
        "If the question asks for general concept clarification, explain using standard technical knowledge. "
        "Do not invent project-specific facts not present in the card. "
        "Keep responses to 3-5 sentences unless a longer explanation is clearly necessary."
    )

    messages = [
        {"role": "system", "content": f"{system_prompt}\n\nFlashcard Context:\n{context}"}
    ]
    # Include last 6 history turns to keep context manageable
    for msg in history[-6:]:
        role = msg.get('role', 'user')
        content = msg.get('content', '')
        if role in ('user', 'assistant') and content:
            messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()
