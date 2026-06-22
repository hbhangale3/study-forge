from datetime import date, timedelta
import json, os

PROGRESS_FILE = 'data/progress.json'

def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return {}
    with open(PROGRESS_FILE) as f:
        return json.load(f)

def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def get_card_progress(progress, card_id):
    return progress.get(card_id, {
        'card_id': card_id,
        'ease_factor': 2.5,
        'interval': 1,
        'repetitions': 0,
        'next_review': date.today().isoformat(),
        'history': []
    })

def update_card(card_state, quality):
    """SM-2 algorithm. Quality 0-5."""
    ef = card_state['ease_factor']
    reps = card_state['repetitions']
    interval = card_state['interval']

    if quality >= 3:
        if reps == 0:
            interval = 1
        elif reps == 1:
            interval = 6
        else:
            interval = round(interval * ef)
        reps += 1
    else:
        reps = 0
        interval = 1

    ef = ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    ef = max(1.3, round(ef, 2))

    next_review = (date.today() + timedelta(days=interval)).isoformat()
    history = card_state.get('history', [])
    history.append(quality)

    return {
        'card_id': card_state['card_id'],
        'ease_factor': ef,
        'interval': interval,
        'repetitions': reps,
        'next_review': next_review,
        'history': history
    }

def is_due(card_state):
    return card_state['next_review'] <= date.today().isoformat()

def is_mastered(card_state):
    return (card_state['ease_factor'] >= 2.5 and
            card_state['interval'] >= 21 and
            card_state['repetitions'] >= 3)
