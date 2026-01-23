# Cardio Agent Setup - Jan 23 2026

## Task List

### 1. Build Conda Environment
```bash
conda create -n cardio-agent python=3.10 -y
conda activate cardio-agent
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your-key-here
```
*(Ask for the OpenAI API key via Slack)*

### 4. Test Setup
Run the test script to verify everything works:
```bash
python test_cardio_agent.py
```

### 5. Update Cardio Tools
Modify `/tools/cardio_tools.py` to query SQLite databases directly instead of making API calls.

**Database locations:**
- `/data/client_1_cardio.db`
- `/data/client_2_cardio.db`
- `/data/client_3_cardio.db`

### 6. Set Up GCP Agent
Create `/agents/gcp_cardio_chat_agent.py` that uses Google Vertex AI (Gemini) instead of OpenAI.

*(Ask for the GCP service account JSON file from David when ready)*

---

## Project Structure
```
CardioChatBot/
├── agents/
│   ├── cardio_chat_agent.py          # OpenAI version (existing, run)
│   └── gcp_cardio_chat_agent.py      # GCP version (to build)
├── tools/
│   └── cardio_tools.py                # Update to use SQLite
├── data/
│   ├── client_1_cardio.db
│   ├── client_2_cardio.db
│   └── client_3_cardio.db
├── .env                                # Your API keys (create this)
├── requirements.txt
└── test_cardio_agent.py
```

## Questions?
Reach out to David on Slack!