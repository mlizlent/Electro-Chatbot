# ElectroBot — AI Electronics Engineering Assistant

An AI-powered chatbot specialized in electronics, IoT, sensors, RF/wireless, cellular communication, and hardware engineering. Built with React + FastAPI + Groq (Llama 3.1).

## Features

- **Groq Llama 3.1 powered** — fast, intelligent electronics expertise
-  **Chat history** — persistent conversations with memory
- **Animated circuits** — AI generates and renders interactive circuit diagrams with animations
- **Multi-model image analysis** — upload circuit diagrams/schematics for detailed vision analysis
- **Markdown rendering** — formatted responses with syntax-highlighted code
- **User authentication** — JWT-based auth with registration/login
- **Dark & light themes** — electronics-inspired UI with theme persistence

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, TailwindCSS |
| Backend | Python FastAPI, SQLAlchemy |
| AI | Groq API (Llama 3.1) + Multi-model vision |
| Circuit rendering | Animated SVG with custom animations |
| Database | SQLite |
| Auth | JWT (python-jose) |

## Quick Start

### 1. Clone and set up environment

```bash
cd electronics-chatbot
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set your Groq API key
cp .env.example .env
# Edit .env and add your key: GROQ_API_KEY=gsk_...

# Start the backend
uvicorn main:app --reload --port 8000
```

### 3. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

### 4. Open the app

Visit **http://localhost:5173**, register an account, and start chatting.

## Docker

You can run the full app with Docker Compose from the repo root.

1. Create a `.env` file with at least your `GROQ_API_KEY`, `HF_API_KEY`, and `SECRET_KEY`.
2. Start the app:

```bash
docker compose up --build
```

Open **http://localhost** after the containers start.

## Circuit Sketching

Ask ElectroBot to draw circuits using natural language:

- *"Draw a 555 timer astable multivibrator circuit"*
- *"Sketch a basic LED driver circuit with a transistor"*
- *"Show me a voltage divider circuit"*
- *"Draw an RC low-pass filter"*

The AI will generate an animated circuit diagram rendered as an interactive SVG with component labels, values, and current flow visualization.

## Image Upload

Upload circuit diagrams, schematics, or PCB layouts and ask:

- *"What's wrong with this circuit?"*
- *"Identify the components in this schematic"*
- *"How can I improve this design?"*

ElectroBot uses multi-model vision analysis to provide detailed descriptions, component detection, and object identification with confidence scores.

## Example Questions

**Components:**
- "Explain the difference between MOSFET and BJT transistors"
- "What capacitor should I use for decoupling a 3.3V MCU?"

**IoT & Sensors:**
- "How do I interface a BME280 sensor with ESP32 over I2C?"
- "Design a battery-powered temperature logger with LoRa"

**RF & Wireless:**
- "Compare LoRa, Zigbee, and BLE for industrial IoT"
- "How do I calculate the link budget for a 915MHz LoRa system?"

**Cellular:**
- "What's the difference between NB-IoT and LTE-M?"
- "How do I use a SIM7600 module with AT commands?"

**PCB Design:**
- "What are the rules for high-speed PCB trace routing?"
- "How do I design a proper ground plane?"

## Project Structure

```
electronics-chatbot/
├── backend/
│   ├── main.py              # FastAPI app, all routes
│   ├── auth.py              # JWT authentication
│   ├── chat.py              # Groq API integration & vision
│   ├── circuit.py           # Circuit SVG rendering
│   ├── circuit_animator.py  # Animated circuit generator
│   ├── components_db.py     # Component database
│   ├── models.py            # SQLAlchemy models
│   ├── database.py          # DB connection
│   └── requirements.txt
└── frontend/
    └── src/
        ├── App.jsx
        ├── components/
        │   ├── Auth.jsx         # Login/Register
        │   ├── Chat.jsx         # Main chat interface
        │   ├── Message.jsx      # Message with markdown
        │   ├── CircuitViewer.jsx # Animated SVG display
        │   └── Sidebar.jsx      # Conversation list
        ├── context/
        │   ├── AuthContext.jsx
        │   └── ThemeContext.jsx
        ├── api/
        │   └── client.js        # Axios instance
        ├── App.jsx              # Main app
        └── index.css            # Global styles
```


