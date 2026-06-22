# StudyForge 🧠 - Spaced Repetition Study App

A professional Flask-based spaced repetition system for mastering **system design (HLD)**, **low-level design patterns (LLD)**, and **Java core concepts**. Built with the SM-2 algorithm, AI-powered evaluation via Groq, and a modern dark-themed interface.

## Quick Start

### Prerequisites

- Python 3.8+
- pip or conda

### Installation

```bash
# Clone or navigate to the project directory
cd study-forge

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

> Note: `requirements.txt` pins a compatible Groq dependency stack, including `httpx==0.27.0` for `groq==0.9.0`.

### Configuration (Optional)

For AI-powered answer evaluation in Deep Mode, set your Groq API key:

```bash
# Create .env file
cp .env.example .env

# Edit .env and add your Groq API key
# GROQ_API_KEY=your_api_key_here
```

Without an API key, the app works perfectly in **Quick Rate mode** (offline).

---

## Running the App

### Start the Server

```bash
source venv/bin/activate && python app.py
```

**Output:**

```
Discovered modes: hld, lld, java_core
 * Running on http://127.0.0.1:3000
 * Debugger PIN: xxxxx
```

Visit **http://localhost:3000** in your browser.

### Stop the Server

**Option 1: Interactive (if running in foreground)**

```bash
# Press Ctrl+C in the terminal
```

**Option 2: Kill by port**

```bash
# macOS/Linux:
lsof -i :3000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9

# Or simpler:
pkill -f "python app.py"
```

**Option 3: Kill specific process ID**

```bash
kill -9 <PID>
```

### Restart the Server

```bash
# Kill any existing process
pkill -f "python app.py"

# Wait a moment
sleep 2

# Start fresh
source venv/bin/activate && python app.py
```

---

## Features

### ✨ Core Functionality

- **Spaced Repetition (SM-2 Algorithm)** - Scientifically-optimized review intervals
- **Dark-Themed Professional UI** - Modern sidebar navigation with real-time stats
- **Multi-page Application** - Dashboard, Study Session, and Completion pages
- **Quick Rate Mode** - 4-button ratings (Again/Hard/Good/Easy) with instant feedback
- **Deep Mode (AI)** - Write answers → AI evaluates with score & feedback (requires API key)
- **Progress Persistence** - All study history saved to `progress.json`
- **Dynamic Card Discovery** - Auto-detect new card files in `data/` folder
- **Session Analytics** - Track review counts, average quality, and study duration
- **Responsive Design** - Works on desktop and mobile devices
- **Sidebar Navigation** - Easy navigation between dashboard and study sessions

### 🎯 Study Modes

#### 1. **High-Level Design (HLD)** — 60 Cards

System design fundamentals and advanced patterns

**Chunk 1 — Fundamentals (15 cards)**

- Performance vs Scalability, Vertical vs Horizontal Scaling
- Load Balancing (algorithms, L4 vs L7), DNS & CDN
- CAP Theorem, Consistency Models (Strong/Eventual/Weak), Availability nines
- SQL vs NoSQL decision guide, Database Replication & Sharding
- Database Indexes (B-Tree, clustered vs non-clustered)
- Caching patterns (Cache-aside, Read-through, Write-through, Write-behind)
- Cache eviction, Redis deep dive (5 data structures, 6 use cases)
- Message Queues (Kafka vs RabbitMQ)

**Chunk 2 — Advanced (10 cards)**

- Microservices vs Monolith, SAGA pattern
- Consistent Hashing (virtual nodes, why modulo fails)
- API Gateway vs Load Balancer
- Design Scenarios: URL Shortener, Rate Limiter (4 algorithms), Notification System
- Twitter Feed (fan-out write vs read hybrid), Chat System (WebSocket)
- System Design Interview Framework (4 steps)
- Back-of-envelope estimation (latency, storage, QPS)

**Chunk 3 — Real-World Systems (35 cards)**

- Instagram (upload, likes, media storage)
- YouTube (transcoding, streaming, recommendations)
- Uber (geospatial matching, trip tracking, payments, surge pricing)
- Google Search (web crawler, inverted index, PageRank)
- Key-Value Store (LSM tree, quorum, vector clocks)
- WhatsApp (end-to-end encryption, ACID properties)
- Transaction isolation levels, Cassandra & MongoDB
- Kafka (architecture, delivery guarantees, consumer rebalancing)
- Elasticsearch (full-text search, sync patterns)
- Typeahead/autocomplete with Trie
- Forward vs Reverse Proxy + Nginx
- Service Discovery, Circuit Breaker deep dive
- CDN estimation (full worked examples)

#### 2. **Low-Level Design (LLD)** — 25 Cards

Object-oriented design patterns and SOLID principles

**Chunk 1 — SOLID + Object Relationships (10 cards)**

- Is-a vs Has-a relationships
- Aggregation vs Composition with lifecycle examples
- All 5 SOLID principles:
  - SRP (Single Responsibility Principle)
  - OCP (Open/Closed Principle)
  - LSP (Liskov Substitution Principle — Square/Rectangle violation)
  - ISP (Interface Segregation Principle)
  - DIP (Dependency Inversion Principle)
- Interface vs Abstract Class decision guide

**Chunk 2 — Behavioral Patterns (6 cards)**

- Strategy Pattern (5 real-world scenarios, identification)
- Observer Pattern (4 components, YouTube flow, Push vs Pull)
- Decorator Pattern (Pizza example, class explosion problem)

**Chunk 3 — Creational + Structural Patterns (9 cards)**

- Factory Pattern, Abstract Factory Pattern
- Singleton Pattern (early vs lazy loading, double-checked locking)
- Adapter Pattern (RazorPay integration example)
- Flyweight Pattern (intrinsic vs extrinsic state)
- Proxy Pattern (Adapter vs Decorator vs Proxy comparison)
- Builder Pattern (fluent API, telescoping constructor)
- Pattern identification guide with interview approach

#### 3. **Java Core** — 63 Cards

Fundamental Java concepts, threading, and backend patterns

**Fundamentals (27 cards)**

- Classes, Objects, Memory Model (Stack vs Heap)
- Constructors (default, parameterized, copy), `this` keyword, `new` keyword
- Access modifiers (public, private, protected, package-private)
- Static keyword vs instance members
- Abstract classes, Interfaces, visibility contracts
- Association vs Aggregation vs Composition with lifecycle reasoning
- All 5 SOLID principles with bad design → good design patterns
- Runtime polymorphism, overloading vs overriding
- Inheritance types, `super` keyword, constructor chain, `final` keyword
- Object class, `equals` vs `==`, wrapper classes + autoboxing trap
- String immutability + string pool

**Threading (23 cards)**

- Program vs Process vs Thread, Context Switching
- Concurrency vs Parallelism, Process vs Thread comparison
- ULT vs KLT vs LWP (JVM threading model)
- Creating threads (Runnable vs Thread, `start()` vs `run()`)
- Thread lifecycle (6 states: New, Runnable, Blocked, Waiting, Timed-Waiting, Terminated)
- Callable vs Runnable, Future, FutureTask bridge
- ExecutorService (3 thread pool types, CachedThreadPool crash under load)
- Thread starvation, fair vs non-fair lock tradeoffs
- Race condition with `counter++` internals, thread safety (4 approaches)
- Synchronized keyword and monitor
- ReentrantLock (tryLock, reentrancy), ReadWriteLock, Semaphore
- Deadlock (4 conditions, bank transfer example), wait/notify/notifyAll
- Producer-Consumer pattern
- Volatile keyword (visibility vs atomicity)
- Mutex vs Lock vs Monitor distinctions

**Advanced (13 cards)**

- Exception Handling (checked vs unchecked)
- Try-catch-finally rules, stack unwinding
- throw vs throws, custom exceptions
- Fail Fast / Fail Safe / Timeout strategies
- JVM Memory (Heap vs Stack vs Method Area)
- Garbage Collection (reachability, generational GC)
- Eden/Survivor/Old generation
- REST API design (HTTP methods, status codes, DTOs)
- REST vs GraphQL vs gRPC comparison
- HTTP Polling vs WebSocket
- RabbitMQ architecture (Direct/Fanout/Topic exchanges)
- API idempotency with idempotency keys
- Spring Dependency Injection + DIP connection

---

## File Structure

```
study-forge/
├── app.py                      # Flask backend (routes, card loading, progress management)
├── sm2.py                      # SM-2 spaced repetition algorithm
├── groq_client.py              # AI evaluation (optional, Groq integration)
├── requirements.txt            # Python dependencies
├── .env.example               # Template for environment variables
├── .gitignore                 # Git ignore patterns
├── README.md                  # This file
├── data/
│   ├── cards_hld.json        # 60 high-level design cards
│   ├── cards_lld.json        # 25 low-level design pattern cards
│   └── cards_java_core.json  # 63 Java core concept cards
├── templates/
│   └── index.html            # Single-page app with sidebar navigation
└── progress.json             # User study progress (auto-created, Git-ignored)
```

---

## API Endpoints

| Method | Endpoint                  | Purpose                                                |
| ------ | ------------------------- | ------------------------------------------------------ |
| `GET`  | `/`                       | Serve main UI                                          |
| `GET`  | `/api/modes`              | List all available study modes                         |
| `GET`  | `/api/stats`              | Get statistics (total, due, mastered, unseen) per mode |
| `GET`  | `/api/session/<mode>`     | Start study session (load due cards)                   |
| `POST` | `/api/answer`             | Submit rating (0-5) for a card                         |
| `POST` | `/api/evaluate`           | AI evaluation of user answer (requires API key)        |
| `GET`  | `/api/followup/<card_id>` | Generate follow-up question (AI, requires API key)     |
| `POST` | `/api/reset/<mode>`       | Reset progress for a study mode                        |

---

## Card Format

Cards are stored as JSON with the following structure:

```json
{
  "cards": [
    {
      "id": "hld_001",
      "question": "What is the difference between...",
      "answer": "...",
      "code": "// optional code example",
      "hint": "Think about...",
      "subcategory": "Fundamentals",
      "category": "HLD",
      "difficulty": "Medium",
      "tags": ["scalability", "architecture"],
      "mode": "hld"
    }
  ]
}
```

### Adding New Cards

**Method 1: Extend existing files**

```bash
# Edit data/cards_hld.json, data/cards_lld.json, or data/cards_java_core.json
# Add more objects to the "cards" array
# Restart the app — cards auto-discovered!
```

**Method 2: Create new mode file**

```bash
# Create data/cards_your_topic.json with same structure
# Restart the app — auto-discovered as "your_topic" mode
```

---

## How It Works

### SM-2 Spaced Repetition Algorithm

Each card tracks:

- **Ease Factor** (1.3–∞, starts at 2.5) — affects interval growth
- **Interval** (1→6→exponential) — days until next review
- **Repetitions** — number of times reviewed
- **Next Review** — calculated date for this card

**Quality Scale (0-5):**

- **0**: Completely wrong / Blank
- **1**: Incorrect, some understanding
- **2**: Partially correct
- **3**: Correct with missing details
- **4**: Correct with minor gaps
- **5**: Perfect answer

**Mastery Criteria:**

- Ease Factor ≥ 2.5 AND Interval ≥ 21 days AND Repetitions ≥ 3

### Card Discovery

On startup, the app scans `data/` for `cards_*.json` files:

```bash
Discovered modes: hld, lld, java_core
```

Each file is automatically unwrapped from `{"cards": [...]}` format (if needed) and loaded into memory.

### Progress Tracking

Study progress is saved to `progress.json`:

```json
{
  "hld_001": {
    "ease_factor": 2.5,
    "interval": 1,
    "repetitions": 0,
    "next_review": "2026-06-22",
    "history": []
  }
}
```

This file is **Git-ignored** to prevent tracking personal study data.

---

## Dependencies

```
flask==3.0.3
groq==0.9.0
python-dotenv==1.0.1
```

See `requirements.txt` for exact versions.

---

## Troubleshooting

### Port 3000 Already in Use

```bash
# Find and kill process using port 3000
lsof -i :3000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9

# Or:
pkill -f "python app.py"

# Or for specific PID:
kill -9 <PID>
```

### App Won't Start

1. Check Python version: `python --version` (need 3.8+)
2. Verify venv activated: `which python` (should show venv path)
3. Reinstall dependencies: `pip install -r requirements.txt`
4. Check port: `lsof -i :3000`

### AI Evaluation Returns Error

The app works offline without an API key. To enable AI:

1. Get free Groq API key from https://console.groq.com
2. Set `GROQ_API_KEY=...` in `.env`
3. Restart the app

### Progress Not Saving

Ensure `progress.json` has write permissions:

```bash
chmod 644 progress.json
```

---

## Performance Notes

- **148 total cards** loaded in memory
- **Session load time** < 100ms
- **Card render time** < 50ms
- Suitable for local/personal use (single user)

---

## License

Open-source study material. Use freely for educational purposes.

---

## Contributing

To add new cards or topics:

1. Create `data/cards_my_topic.json`
2. Follow the card format above
3. Restart the app
4. Cards appear automatically

---

## Summary

**StudyForge** is a comprehensive spaced repetition system covering:

- **System Design** (HLD): 60 cards on architecture, scalability, real-world systems
- **Design Patterns** (LLD): 25 cards on SOLID, OOP patterns, refactoring
- **Java Core**: 63 cards on fundamentals, threading, backend concepts

Perfect for interview prep, backend learning, and mastering core CS concepts.
