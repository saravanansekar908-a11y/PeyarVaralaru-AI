# PeyarVaralaru AI — Historical Tamil Place Name Explorer
### பெயர்வரலாறு AI — வரலாற்றுத் தமிழ் இடப்பெயர் ஆராய்ச்சி தளம்

An AI-powered full-stack historical research platform studying the historical evolution of Tamil Nadu place names, names of cities, villages, streets, and settlements across old maps, government orders, district gazetteers, inscriptions, and archival records.

---

## 🏛️ Project Overview

Historical Tamil place names carry centuries of linguistic, cultural, and administrative evolution. Many place names have transitioned across periods (Sangam, Chola, Vijayanagara, Colonial, and Post-Independence). **PeyarVaralaru AI** connects modern geographic locations with their historical variants, official renaming government orders, and epigraphical evidence while strictly distinguishing verified records, spelling variations, and unverified claims.

---

## 🚀 Key Features

1. **Bilingual by Default (Tamil & English)**:
   - First-time visitors experience the interface in **Tamil (தமிழ்) by default**.
   - One-click instant switching to English with persistent language state (`localStorage`).
   - Unicode Tamil typography and natural translation across all cards, modals, tables, and AI chat.

2. **Smart Place Search**:
   - Exact and fuzzy name matching powered by `RapidFuzz` and Unicode normalization.
   - Accepts search queries in both Tamil script and English transliteration (e.g., *Madras*, *சென்னை*, *Black Town*, *Trichinopoly*, *Tanjore*).
   - Returns matched place profiles, historical variants, and the exact matching rationale.

3. **Place Details & Historical Evolution Timeline**:
   - Detailed geographic profiles with verified coordinates and district metadata.
   - Chronological timelines distinguishing:
     - `Official Renaming` (அதிகாரப்பூர்வ பெயர் மாற்றம்)
     - `Historical Name Variant` (வரலாற்றுப் பெயர் பதிவு)
     - `Transliteration Variant` (எழுத்துப்பெயர்ப்பு மாற்றம்)
     - `Settlement Founded` (குடியேற்றத் தொடக்கம்)
   - Clickable primary source citations linking directly to official archive portals.

4. **Evidence & Sources Explorer**:
   - Central repository of official Government Orders (e.g., G.O. No. 158 of 1906 for George Town), District Gazetteers, and Tamil Nadu Archives records.
   - Evidence verification tiers: **Verified**, **Partially Verified**, and **Unverified**.
   - Clear ethical policy: AI answers are grounded in primary sources and never fabricated.

5. **Ask History AI (Evidence-Grounded Q&A)**:
   - AI assistant powered by Google Gemini with strict database evidence grounding.
   - When Gemini API key is not configured, automatically operates in **Database Fallback Mode** with zero crashes.
   - Replies in the selected language (Tamil or English) with attached source citations.

6. **Historical Relationship Explorer (Interactive Graph)**:
   - Built with `React Flow` (`@xyflow/react`).
   - Visualizes nodes for Places, Historical Names, Events, and Source Documents connected by typed edges (`HAS_HISTORICAL_NAME`, `CHANGED_ON`, `SUPPORTED_BY`).
   - Interactive zoom, pan, fit-to-view, node inspector side panel, and legend.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 19, Vite 8, Tailwind CSS, React Router v7, `@xyflow/react` (React Flow), Lucide React, Axios |
| **Backend** | Python 3.12, FastAPI, Uvicorn, SQLAlchemy ORM, SQLite, Pydantic v2, RapidFuzz |
| **AI / ML** | Google GenAI SDK (`google-genai`), evidence grounding engine with database fallback |
| **Database** | SQLite with normalized relational schema (places, historical names, events, sources, associations) |

---

## 📁 Project Directory Structure

```
PeyarVaralaru-AI/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application, lifespan & CORS
│   │   ├── database.py          # SQLAlchemy models & SQLite setup
│   │   ├── schemas.py           # Pydantic validation schemas
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── places.py        # Place listing, search, timeline & sources
│   │   │   ├── graph.py         # Relationship graph generator
│   │   │   └── ask.py           # AI question answering endpoint
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── seed_service.py  # Automated database seeding
│   │       ├── search_service.py# RapidFuzz search with unicode normalization
│   │       └── ai_service.py    # Gemini integration with fallback
│   ├── data/
│   │   └── seed_data.json       # Historical dataset (Chennai, George Town, Trichy, Thanjavur)
│   ├── .env.example
│   ├── .env
│   ├── requirements.txt
│   └── venv/
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── Navbar.jsx       # Header with Tamil/English switcher
│   │   │   ├── Sidebar.jsx      # Navigation sidebar with module links
│   │   │   └── StatusBadge.jsx  # Evidence verification badges
│   │   ├── pages/
│   │   │   ├── Home.jsx         # Landing dashboard with hero search & quick links
│   │   │   ├── SearchPage.jsx   # Smart search with match criteria chips
│   │   │   ├── PlaceDetails.jsx # Historical timeline with source excerpts
│   │   │   ├── SourcesPage.jsx  # Evidence & G.O. explorer
│   │   │   ├── AskAI.jsx        # Grounded Q&A chat interface
│   │   │   └── RelationshipGraph.jsx # Interactive React Flow graph
│   │   ├── locales/
│   │   │   ├── en.json          # English localization dictionary
│   │   │   └── ta.json          # Tamil localization dictionary
│   │   ├── services/
│   │   │   ├── api.js           # Axios client for backend endpoints
│   │   │   └── LanguageContext.jsx # Bilingual context provider
│   │   ├── App.jsx              # Routing & application shell
│   │   ├── index.css            # Tailwind CSS & theme tokens
│   │   └── main.jsx             # React DOM root
│   ├── index.html               # Tamil Unicode & Latin typography
│   ├── package.json
│   ├── vite.config.js
└── README.md
```

---

## ⚙️ Prerequisites

- **Python**: 3.10+
- **Node.js**: 18+ (includes `npm`)

---

## 🚀 Running the Application

### 1. Backend Setup & Startup

```powershell
cd C:\Users\Admin\.gemini\antigravity-ide\scratch\PeyarVaralaru-AI\backend

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Start FastAPI server on port 8000
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The backend starts at `http://127.0.0.1:8000`. Database automatically seeds on first launch.

### 2. Frontend Setup & Startup

```powershell
cd C:\Users\Admin\.gemini\antigravity-ide\scratch\PeyarVaralaru-AI\frontend

# Install dependencies (if not already installed)
npm install

# Start Vite dev server on port 5173
npm run dev -- --host 127.0.0.1 --port 5173
```

Open your browser at `http://localhost:5173`.

---

## 🔑 Environment Variables

### Backend (`backend/.env`)
```ini
# Optional: Google Gemini API Key for generative answers (App functions without it using database fallback)
GEMINI_API_KEY=

# SQLite database file path
DATABASE_URL=sqlite:///./peyarvaralaru.db

# Frontend origin allowed for CORS
FRONTEND_ORIGIN=http://localhost:5173
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check for server & database |
| `GET` | `/api/places` | List all historical places |
| `GET` | `/api/places?q={query}` | Search current & historical place names (exact + fuzzy) |
| `GET` | `/api/places/{id}` | Detailed place profile with historical names & events |
| `GET` | `/api/places/{id}/timeline` | Chronological event timeline |
| `GET` | `/api/places/{id}/sources` | Sources supporting events for a place |
| `GET` | `/api/sources` | All historical primary source records |
| `GET` | `/api/graph/{id}` | Node & edge data for React Flow visualization |
| `POST` | `/api/ask` | Evidence-grounded historical question answering |

---

## 🧪 Sample Demonstration Workflow

1. **First-Time Load**: Open `http://localhost:5173`. Notice all navigation, headers, and descriptions are rendered in **Tamil (தமிழ்)**.
2. **Language Switching**: Click **English** in the top navigation bar. The entire interface immediately switches to English. Click **தமிழ்** to restore Tamil.
3. **Smart Place Search**:
   - Type `Madras` in the search bar.
   - Result displays **Chennai (சென்னை)** with match reason `exact_historical_name:Madras`.
   - Historical variants shown: *Madras*, *மெட்ராஸ்*, *Madraspatnam*, *Chennapatnam*, *சென்னப்பட்டணம்*.
4. **Timeline & Sources**:
   - Click "Explore Historical Timeline" for Chennai.
   - Inspect the official 1996 renaming event and colonial 1639 settlement event with primary source links to Tamil Nadu Archives.
5. **Ask History AI**:
   - Navigate to `/ask`.
   - Click the prompt chip: *"When was Black Town renamed to George Town?"*
   - View answer citing G.O. No. 158, Public Department, dated 3 March 1906.
6. **Relationship Graph**:
   - Navigate to `/graph`.
   - Select **Chennai** or **George Town** to explore the interactive node network linking places to historical names, events, and source documents.

---

## 📜 Historical Seed Records

1. **Chennai (`id: 1`)**:
   - Current Name: Chennai (சென்னை)
   - Historical Variants: Madras, மெட்ராஸ், Madraspatnam, Chennapatnam, சென்னப்பட்டணம்
   - Verified Event: 1996 official renaming.
   - Sources: Chennai District Administration & Tamil Nadu Archives Gazetteers.

2. **George Town (`id: 2`)**:
   - Current Name: George Town (ஜார்ஜ் டவுன்)
   - Historical Variant: Black Town (பிளாக் டவுன்)
   - Documented Event: G.O. No. 158, Public Department, 3 March 1906.
   - Sources: Tamil Nadu Archives Important Government Orders.

3. **Tiruchirappalli (`id: 3`)**:
   - Current Name: Tiruchirappalli (திருச்சிராப்பள்ளி)
   - Historical English Form: Trichinopoly
   - Type: Historical transliteration variant.

4. **Thanjavur (`id: 4`)**:
   - Current Name: Thanjavur (தஞ்சாவூர்)
   - Historical English Form: Tanjore
   - Type: Historical colonial spelling variant.
