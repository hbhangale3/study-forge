from flask import Flask, jsonify, request, render_template
from datetime import date
import json, os, glob
from sm2 import (load_progress, save_progress, get_card_progress,
                 update_card, is_due, is_mastered)
from groq_client import evaluate_answer, generate_followup

app = Flask(__name__)

# Dynamic card file discovery
def discover_card_files():
    """Find all cards_*.json files in data/ directory."""
    card_files = {}
    data_dir = 'data'
    pattern = os.path.join(data_dir, 'cards_*.json')
    
    for filepath in glob.glob(pattern):
        # Extract mode name from filename: cards_xyz.json → xyz
        filename = os.path.basename(filepath)
        mode = filename.replace('cards_', '').replace('.json', '')
        card_files[mode] = filepath
    
    return card_files

CARD_FILES = discover_card_files()

def mode_display_name(mode):
    """Convert mode name to display name."""
    mapping = {
        'java_core': 'Java Core',
        'lld': 'LLD Patterns',
        'hld': 'HLD Concepts'
    }
    if mode in mapping:
        return mapping[mode]
    # For other modes: hld_advanced → HLD Advanced
    return ' '.join(word.capitalize() for word in mode.split('_'))

def fix_card_file(path):
    """Unwrap {"cards": [...]} to flat array if needed."""
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, dict) and 'cards' in data:
        with open(path, 'w') as f:
            json.dump(data['cards'], f, indent=2)
        print(f"Fixed structure: {path}")

def load_cards(mode):
    """Load and fix cards for a given mode."""
    if mode not in CARD_FILES:
        return None
    fix_card_file(CARD_FILES[mode])
    with open(CARD_FILES[mode]) as f:
        return json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/modes')
def get_modes():
    """Return list of available modes with display names."""
    modes = []
    for mode in sorted(CARD_FILES.keys()):
        modes.append({
            'id': mode,
            'name': mode_display_name(mode)
        })
    return jsonify(modes)

@app.route('/api/session/<mode>')
def get_session(mode):
    """Get due cards for a study session (max 20)."""
    if mode not in CARD_FILES:
        return jsonify({'error': 'Unknown mode'}), 400
    
    cards = load_cards(mode)
    if cards is None:
        return jsonify({'error': 'Failed to load cards'}), 500
    
    progress = load_progress()
    today = date.today().isoformat()
    due = []
    
    for card in cards:
        state = get_card_progress(progress, card['id'])
        if state['next_review'] <= today:
            card['progress'] = state
            due.append(card)
    
    # Sort: new cards first (repetitions==0), then overdue oldest first
    due.sort(key=lambda c: (c['progress']['repetitions'] > 0,
                             c['progress']['next_review']))
    return jsonify(due[:20])  # cap at 20 per session

@app.route('/api/answer', methods=['POST'])
def submit_answer():
    """Submit a rated answer and update progress."""
    body = request.json
    card_id = body['card_id']
    quality  = int(body['quality'])
    
    progress = load_progress()
    state    = get_card_progress(progress, card_id)
    updated  = update_card(state, quality)
    progress[card_id] = updated
    save_progress(progress)
    
    return jsonify({
        'next_review':  updated['next_review'],
        'interval':     updated['interval'],
        'ease_factor':  updated['ease_factor'],
        'mastered':     is_mastered(updated)
    })

@app.route('/api/stats')
def get_stats():
    """Get study statistics for all modes."""
    progress = load_progress()
    stats = {}
    today = date.today().isoformat()
    
    for mode in sorted(CARD_FILES.keys()):
        cards = load_cards(mode)
        if cards is None:
            continue
        
        total = len(cards)
        seen = mastered = due_today = 0
        
        for card in cards:
            state = get_card_progress(progress, card['id'])
            if state['repetitions'] > 0:
                seen += 1
            if is_mastered(state):
                mastered += 1
            if state['next_review'] <= today:
                due_today += 1
        
        stats[mode] = {
            'name': mode_display_name(mode),
            'total':     total,
            'seen':      seen,
            'mastered':  mastered,
            'due_today': due_today,
            'unseen':    total - seen
        }
    
    return jsonify(stats)

@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    """Evaluate a free-text answer using Groq AI."""
    body = request.json
    card = body['card']
    user_answer = body['user_answer']
    try:
        result = evaluate_answer(card, user_answer)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e), 'score': None}), 500

@app.route('/api/followup/<card_id>')
def get_followup(card_id):
    """Generate a follow-up question for mastered cards."""
    # Find card across all modes
    for mode in CARD_FILES.keys():
        cards = load_cards(mode)
        if cards is None:
            continue
        for card in cards:
            if card['id'] == card_id:
                try:
                    question = generate_followup(card)
                    return jsonify({'followup': question})
                except Exception as e:
                    return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Card not found'}), 404

@app.route('/api/reset/<mode>', methods=['POST'])
def reset_mode(mode):
    """Reset all progress for a given mode."""
    if mode not in CARD_FILES:
        return jsonify({'error': 'Unknown mode'}), 400
    
    cards = load_cards(mode)
    if cards is None:
        return jsonify({'error': 'Failed to load cards'}), 500
    
    progress = load_progress()
    for card in cards:
        if card['id'] in progress:
            del progress[card['id']]
    save_progress(progress)
    
    return jsonify({'reset': True, 'mode': mode})

if __name__ == '__main__':
    # Print discovered modes on startup
    print(f"Discovered modes: {', '.join(CARD_FILES.keys())}")
    app.run(debug=True, port=3000)
