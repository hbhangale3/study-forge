import os, json
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

# Lazy initialization of Groq client
_client = None

def get_client():
    """Get or initialize Groq client. Raises error if API key not set."""
    global _client
    if _client is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not set. Deep Mode (AI evaluation) requires a valid API key. "
                "Get one at https://console.groq.com and set it in .env file."
            )
        _client = Groq(api_key=api_key)
    return _client

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
        model="llama-3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    text = response.choices[0].message.content.strip()
    # Strip markdown code fences if present
    text = text.replace('```json','').replace('```','').strip()
    return json.loads(text)

def generate_followup(card):
    """Generate a harder follow-up question based on a card the user got right."""
    client = get_client()
    
    prompt = f"""You are a senior software engineer interviewer.

The student just correctly answered this question:
Topic: {card['subcategory']}
Question: {card['question']}

Generate ONE harder follow-up question that probes deeper understanding or asks about edge cases, tradeoffs, or real-world application. Return ONLY the question text, nothing else."""

    response = client.chat.completions.create(
        model="llama-3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()
