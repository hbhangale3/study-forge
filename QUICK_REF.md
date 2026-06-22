# StudyForge - Quick Reference

## 📍 Essential Commands

### START THE APP

```bash
source venv/bin/activate && python app.py
```

→ Opens at **http://localhost:3000**

### STOP THE APP

```bash
pkill -f "python app.py"
```

### RESTART THE APP

```bash
pkill -f "python app.py" && sleep 2 && source venv/bin/activate && python app.py
```

### CHECK IF PORT 3000 IS IN USE

```bash
lsof -i :3000
```

---

## 📚 What's Covered

### **High-Level Design (HLD)** — 60 Cards

- **Fundamentals**: Scalability, Load Balancing, CAP Theorem, Caching, Message Queues
- **Advanced**: Microservices, Consistent Hashing, API Gateway, System Design Interview Framework
- **Real-World**: Instagram, YouTube, Uber, Google Search, WhatsApp, Cassandra, MongoDB, Kafka, Elasticsearch, CDN

### **Low-Level Design (LLD)** — 25 Cards

- **SOLID Principles**: SRP, OCP, LSP, ISP, DIP (with code examples)
- **Behavioral Patterns**: Strategy, Observer, Decorator
- **Structural Patterns**: Factory, Singleton, Adapter, Flyweight, Proxy, Builder

### **Java Core** — 63 Cards

- **Fundamentals**: Classes, OOP, Access Modifiers, Static, Inheritance, Polymorphism
- **Threading**: Concurrency, Thread Lifecycle, Executors, Locks, Deadlock, Wait/Notify, Volatile
- **Advanced**: Exception Handling, GC, REST APIs, RabbitMQ, Spring DI

---

## 🎯 Study Modes

| Mode             | Cards | Type                        |
| ---------------- | ----- | --------------------------- |
| **Java Core**    | 63    | Fundamentals → Advanced     |
| **LLD Patterns** | 25    | Design Patterns & SOLID     |
| **HLD Concepts** | 60    | System Design & Scalability |

---

## 📁 Files to Know

| File                | Purpose               | Git-Ignored? |
| ------------------- | --------------------- | ------------ |
| `app.py`            | Flask backend, routes | ❌ Track     |
| `sm2.py`            | SM-2 algorithm        | ❌ Track     |
| `groq_client.py`    | AI integration        | ❌ Track     |
| `.env`              | API key (Groq)        | ✅ Yes       |
| `progress.json`     | Your study history    | ✅ Yes       |
| `data/cards_*.json` | Study questions       | ❌ Track     |
| `venv/`             | Python packages       | ✅ Yes       |
| `__pycache__/`      | Python cache          | ✅ Yes       |

---

## ⚙️ Setup Reference

```bash
# 1. Create environment
python3 -m venv venv

# 2. Activate
source venv/bin/activate

# 3. Install
pip install -r requirements.txt

# 4. Configure (optional, for AI)
cp .env.example .env
# Then edit .env and add: GROQ_API_KEY=your_key

# 5. Start
python app.py
```

---

## 🚀 Key Features

✅ **Spaced Repetition (SM-2)** — Smart review scheduling  
✅ **Dark-Themed UI** — Modern sidebar navigation  
✅ **Quick Rate Mode** — Fast 4-button ratings  
✅ **Deep Mode (AI)** — Write answers, get feedback  
✅ **Progress Tracking** — Auto-saves to progress.json  
✅ **Dynamic Card Discovery** — Add new cards anytime  
✅ **Responsive Design** — Works on desktop & mobile  
✅ **Offline-First** — Works without API key

---

## 📞 Troubleshooting

### "Port 3000 already in use"

```bash
lsof -i :3000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9
```

### "ModuleNotFoundError"

```bash
pip install -r requirements.txt
```

### "App won't start"

1. Check Python: `python --version` (need 3.8+)
2. Check venv: `which python` (should show venv path)
3. Try reinstall: `pip install --force-reinstall -r requirements.txt`

### "AI evaluation not working"

- Without `GROQ_API_KEY` in `.env`, use Quick Rate mode (no API needed)
- To enable AI: Get free key at https://console.groq.com

---

## 📖 Documentation

- **README.md** — Complete guide (features, API, file structure)
- **COMMANDS.sh** — All terminal commands
- **.gitignore** — Files to exclude from Git

---

## 🎓 Study Statistics

- **Total Cards**: 148
- **Difficulty Levels**: Fundamentals → Advanced
- **Topics**: OOP, Design Patterns, System Architecture, Java Threading
- **Time to Complete One Mode**: 30-90 minutes per session
- **Recommended Frequency**: Daily (15-30 min) for spaced repetition benefits

---

## 🔗 Links

- **App**: http://localhost:3000
- **Groq API**: https://console.groq.com
- **Flask Docs**: https://flask.palletsprojects.com
- **SM-2 Algorithm**: https://en.wikipedia.org/wiki/Leitner_system

---

## 💡 Pro Tips

1. **Start with Fundamentals** → Build foundation before advanced topics
2. **Use Deep Mode** → Better learning than just ratings (when API available)
3. **Follow-up Questions** → Great for truly mastering concepts
4. **Consistent Study** → 15 min daily > 2 hours once a week
5. **Review Regularly** → SM-2 will schedule cards at optimal times
6. **Track Progress** → Dashboard shows mastery progression

---

**Created**: June 2026  
**Version**: 1.0  
**Status**: Production Ready ✅
