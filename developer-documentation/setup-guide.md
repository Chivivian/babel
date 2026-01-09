# Setup Guide

This guide walks you through setting up the Babel development environment from scratch. By the end, you will have a fully functional local translation server.

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

| Tool | Version | Purpose |
| :--- | :--- | :--- |
| **Python** | 3.10 or higher | Core runtime for the translation engine. |
| **Node.js** | 20+ (optional) | For frontend development and Next.js dashboard. |
| **uv** | Latest | Ultra-fast Python package installer and virtual environment manager. |
| **Git** | Any | Version control for cloning the repository. |

---

## Step 1: Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/LunarTechAI/babel.git
cd babel
```

---

## Step 2: Install `uv` (Python Package Manager)

We use `uv` for its speed and reliability. Install it with the following command:

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

After installation, restart your terminal or run `source ~/.bashrc` (or equivalent) to refresh your PATH.

Verify the installation:
```bash
uv --version
```

---

## Step 3: Set Up the Backend Environment

Navigate to the backend directory and install dependencies:

```bash
cd babel-backend/BabelDOC-main
uv sync
```

This command:
1. Creates a virtual environment (`.venv`) if one doesn't exist.
2. Installs all dependencies from `pyproject.toml`.

---

## Step 4: Configure Environment Variables

The translation engine requires an OpenAI API key. Create a `.env` file in the `babel-backend` directory:

```bash
cd ..
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

> **Important:** Never commit your `.env` file to version control. It is already included in `.gitignore`.

---

## Step 5: Start the Translation Server

From the `babel-backend` directory, start the FastAPI server:

```bash
python server.py
```

Or, use the provided startup script:

```bash
./start_server.sh
```

The server will start on `http://localhost:8000`. You can access the web dashboard at:
```
http://localhost:8000/
```

---

## Step 6: Verify the Installation

Open a new terminal and test the API:

```bash
curl http://localhost:8000/api/translations
```

You should receive an empty list:
```json
{"count": 0, "translations": []}
```

---

## Directory Structure

Here is an overview of the key directories:

```
babel/
├── babel-backend/          # Python backend and translation engine
│   ├── BabelDOC-main/      # Core translation logic (BabelDOC)
│   ├── server.py           # FastAPI application
│   ├── .env                # API keys (not committed)
│   ├── Inputs/             # Uploaded PDFs
│   └── Outputs/            # Translated PDFs
├── documentation/          # User-facing guides
├── developer-documentation/# Technical docs (you are here)
├── front/                  # Static HTML frontend
├── scripts/                # CLI translation scripts
├── logs/                   # Server and translation logs
└── test/                   # Test files and scripts
```

---

## Common Issues

### `uv: command not found`
Ensure `uv` is in your PATH. On Windows, you may need to restart your terminal or add `%USERPROFILE%\.local\bin` to your PATH manually.

### `OPENAI_API_KEY not set`
Double-check that your `.env` file exists in `babel-backend/` and contains the correct key. The format is:
```
OPENAI_API_KEY=sk-...
```

### Port 8000 already in use
Another application is using the port. Either stop that application or change the port in `server.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)
```

---

## Next Steps

- Read the [API Reference](./api-reference.md) to understand the available endpoints.
- Explore [Worker Orchestration](./worker-orchestration.md) for production scaling.
- Contribute to the project by following [Contributing Guidelines](./contributing.md).
