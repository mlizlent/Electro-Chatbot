# ElectroBot — AI Electronics Engineering Assistant

An AI-powered chatbot specialized in electronics, IoT, sensors, RF/wireless, cellular communication, and hardware engineering. Built with React + FastAPI + GPT-4o.

## Features

- 🤖 **GPT-4o powered** — deep expertise in hardware engineering
- 💬 **Chat history** — persistent conversations with memory
- 🔌 **Circuit sketching** — AI generates and renders circuit diagrams as SVG
- 🖼️ **Image upload** — upload circuit diagrams/schematics for GPT-4o vision analysis
- 📝 **Markdown rendering** — formatted responses with syntax-highlighted code
- 🔐 **User authentication** — JWT-based auth with registration/login
- 🌙 **Dark theme** — electronics-inspired dark UI

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, TailwindCSS |
| Backend | Python FastAPI, SQLAlchemy |
| AI | OpenAI GPT-4o (chat + vision) |
| Circuit rendering | schemdraw (SVG) |
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

# Set your OpenAI API key
cp .env.example .env
# Edit .env and add your key: OPENAI_API_KEY=sk-...

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

## Circuit Sketching

Ask ElectroBot to draw circuits using natural language:

- *"Draw a 555 timer astable multivibrator circuit"*
- *"Sketch a basic LED driver circuit with a transistor"*
- *"Show me a voltage divider circuit"*
- *"Draw an RC low-pass filter"*

The AI will generate a circuit diagram rendered as an interactive SVG with zoom and download controls.

## Image Upload

Upload circuit diagrams, schematics, or PCB layouts and ask:

- *"What's wrong with this circuit?"*
- *"Identify the components in this schematic"*
- *"How can I improve this design?"*

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
│   ├── main.py          # FastAPI app, all routes
│   ├── auth.py          # JWT authentication
│   ├── chat.py          # OpenAI integration
│   ├── circuit.py       # Circuit rendering (schemdraw)
│   ├── models.py        # SQLAlchemy models
│   ├── database.py      # DB connection
│   └── requirements.txt
└── frontend/
    └── src/
        ├── App.jsx
        ├── components/
        │   ├── Auth.jsx         # Login/Register
        │   ├── Chat.jsx         # Main chat interface
        │   ├── Message.jsx      # Message with markdown
        │   ├── CircuitViewer.jsx # SVG circuit display
        │   └── Sidebar.jsx      # Conversation list
        ├── context/
        │   └── AuthContext.jsx
        └── api/
            └── client.js        # Axios instance
```


