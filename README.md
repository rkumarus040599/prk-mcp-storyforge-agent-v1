Here is an updated, **specific** README you can use for this project (replace anything you don’t like and adjust the env var names if needed).

---

# 🤖 Story Forge Agent

A **Streamlit-powered Gen-AI app** that combines Google Gemini and Tavily search to turn any trending topic into a concise research summary and a short-form video script for YouTube Shorts or Instagram Reels.[1][2]

***

## Overview

Story Forge Agent lets you type any topic (from world news to niche research trends) and automatically:  
- Fetches recent information with the Tavily search API.[1]
- Summarizes it into a ~200‑word, human-like explanation using Gemini.  
- Optionally converts the summary into a 100–120 word, hook-driven short video script.

This makes it useful for content creators, marketers, students, and researchers who want quick, **ready-to-use** insights and scripts.

---

## Features

- **Real-time research:** Uses Tavily to search the web and aggregate 3 recent results for your query.[1]
- **AI-generated summary:** Gemini turns raw search snippets into a clean, factual, ~200-word summary.  
- **Video script generator:** Creates a “hook → main content → call to action” script suitable for Shorts/Reels in 100–120 words.  
- **Downloadable output:** One-click download of the generated script as a `.txt` file.  
- **Polished UI:** Custom CSS on top of Streamlit for a card-style, centered layout.

***

## Tech Stack

- **Frontend / App:** Streamlit (`app.py`)  
- **LLM:** Google Gemini (`google.generativeai`)  
- **Search:** Tavily API (`tavily` Python client)[1]
- **Config:** `python-dotenv` for environment variable management  

***

## Project Structure

```text
prk-mcp-storyforge-agent-v1/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies (if present)
├── .env.example        # Example environment configuration (recommended)
└── README.md           # This file
```

(Add or adjust files above to match your repo.)

***

## Getting Started

### Prerequisites

- Python 3.10+  
- A Google AI Studio / Gemini API key (`GOOGLE_API_KEY`)[1]
- A Tavily API key (`TAVILY_API_KEY`)  

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/rkumarus040599/prk-mcp-storyforge-agent-v1.git
cd prk-mcp-storyforge-agent-v1

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

***

## Configuration

The app uses `python-dotenv` and `load_dotenv()` to read environment variables.[3]

Create a `.env` file in the project root:

```bash
cp .env.example .env   # if you add an example file
```

Then set these variables:

```dotenv
GOOGLE_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

The code uses two model identifiers:

```python
MODEL_INFO   = "gemini-2.0-flash"
MODEL_SCRIPT = "gemini-2.0-flash"
```

You can change those to any supported Gemini model name if needed.[1]

***

## How It Works

### 1. Real-time information (`get_realtime_info`)

- Calls Tavily with the user query (`topic="general"`, `max_results=3`).  
- Builds a combined text block from result title, URL, and snippet.[1]
- Sends that block to Gemini with a prompt that asks for:
  - ~200 word length  
  - Factual, smooth, human-like tone  
  - Key takeaways / trends  
- Returns the refined summary back to the UI.

### 2. Video script generation (`generate_video_script`)

- Takes the AI summary as input.  
- Prompts Gemini to create a short script (100–120 words) with:
  - Introduction (hook)  
  - Main content  
  - Conclusion (call to action)  
- Returns the script for display and download.

***

## Running the App

From the project root:

```bash
streamlit run app.py
```

Then open the local URL shown in your terminal (typically `http://localhost:8501`).[2]

### Usage in the UI

1. Enter any topic in the **“Enter your search query”** input.  
2. Wait while the app “Searches and generating / Gathering latest information ...”.  
3. Read the **AI generated summary** under “Real-time Information”.  
4. Select **“Yes”** in the “Generate Video Script” radio button.  
5. View the **AI generated video script** and click **Download Script** to save it as `video_script.txt`.

***

## Customization Ideas

- Swap Gemini models (e.g., different `gemini-*` variants) for cost/quality tradeoffs.[1]
- Change Tavily parameters (e.g., `topic`, `max_results`) to target different domains.  
- Add language selection and ask Gemini to respond in that language.  
- Extend the UI to show source links nicely (cards, expandable sections).  

***

## Contributing

Contributions, ideas, and bug reports are welcome.[4][5]

- Open an **Issue** for problems or feature requests.  
- Fork the repo, create a branch, and open a **Pull Request** for changes.

***

## License

This project is licensed under the terms specified in the `LICENSE` file in this repository (e.g., MIT).[3][4]

[1](https://benhouston3d.com/blog/crafting-readmes-for-ai)
[2](https://www.netguru.com/blog/how-to-write-a-perfect-readme)
[3](https://www.makeareadme.com)
[4](https://github.com/othneildrew/Best-README-Template)
[5](https://dev.to/busycaesar/make-your-github-repos-readmemd-uniform-and-informative-by-creating-a-repo-template-2e3b)