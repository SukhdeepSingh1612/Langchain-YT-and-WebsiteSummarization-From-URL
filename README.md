# Langchain YT and WebsiteSummarization From URL

This is a Python-based text summarization project that extracts and summarizes transcripts from YouTube videos using LangChain and LLMs (Large Language Models). It uses the Groq API to interface with powerful LLMs like LLaMA or Mixtral.

## Features

- Extracts transcripts from YouTube videos
- Summarizes long-form content using an LLM chain
- Built with LangChain and Groq
- Modular and easy to expand for more features

## Requirements

- Python 3.10+
- API access to Groq (https://console.groq.com/)
- YouTube video must have captions available

## Installation

```bash
git clone https://github.com/your-username/youtube-summary.git
cd youtube-summary
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Usage

Update the `groq_api_key` in the script and provide a valid YouTube URL. Then run:

```bash
python betterApp.py
```

## Configuration

Replace the model name with a valid Groq model if needed:

```python
llm = ChatGroq(model="llama3-8b-8192", groq_api_key=groq_api_key)
```

## Supported Groq Models

- `llama3-8b-8192`
- `llama3-70b-8192`
- `mixtral-8x7b-32768`

## License

This project is licensed under the MIT License.
