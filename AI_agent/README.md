# SKARAB_BINGO AI Assistant

An intelligent agent to help users understand the SKARAB_BINGO project functionality through natural language queries.

## Overview

This AI assistant helps users understand the SKARAB_BINGO radio astronomy project by analyzing project files and providing intelligent responses to user questions. The system consists of three main components:

1. **Analyzer**: Scans project files (.py, .tex, .txt, README) and creates a structured JSON description
2. **AI Backend**: Interfaces with the DeepSeek API to answer user questions with context
3. **Web Frontend**: Provides a user-friendly web interface for asking questions

## Architecture

```
AI_agent/
├── analyzer.py          # Project file analyzer
├── ai_backend.py        # DeepSeek API interface
├── server.py            # Flask web server
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html      # Web interface
└── project_analysis.json # Generated project analysis (after running analyzer)
```

## Setup

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Set up your DeepSeek API key as an environment variable:
```bash
export DEEPSEEK_API_KEY="your_api_key_here"
```

## Usage

1. First, run the analyzer to scan the project files:
```bash
python analyzer.py
```
This will generate a `project_analysis.json` file with information about the project structure.

2. Start the web server:
```bash
python server.py
```

3. Open your browser and go to `http://localhost:5000` to access the AI assistant interface.

## Features

- Natural language queries about the project in any language
- Context-aware responses based on project file analysis
- Responsive web interface that works on desktop and mobile devices
- Intelligent file matching to provide specific information about relevant scripts
- Streaming responses for better user experience
- Markdown rendering for formatted responses

## How It Works

1. The analyzer scans all project files and creates a structured representation of the codebase
2. When a user asks a question, the AI backend identifies relevant files from the analysis
3. The question, along with context from relevant files, is sent to the DeepSeek API
4. The response is streamed back to the user through the web interface with real-time rendering

## Example Questions

- "What does the pulsar_23mhz_conplot.py script do?"
- "How do I set up the casperfpga environment?"
- "Explain the SKARAB ADC board configuration"
- "What is the purpose of the bingo_dec16_32k firmware?"

The assistant can answer these questions in the user's preferred language.

## Troubleshooting

### Timeout Issues

If you encounter timeout errors like:
```
Error querying AI model: HTTPSConnectionPool(host='api.deepseek.com', port=443): Read timed out.
```

This usually happens due to network connectivity issues or slow API responses. Try these solutions:

1. Check your internet connection
2. Try again - temporary network issues are common
3. If behind a firewall or proxy, ensure it allows connections to api.deepseek.com
4. Consider using a VPN if there are regional restrictions

### API Key Issues

If you get authentication errors:
1. Verify your DEEPSEEK_API_KEY is correctly set in environment variables
2. Ensure the API key is valid and active in your DeepSeek account
3. Check that you haven't exceeded your API quota

### Other Issues

For other issues:
1. Check the terminal logs for detailed error messages
2. Ensure all dependencies are correctly installed
3. Make sure you've run the analyzer before starting the server