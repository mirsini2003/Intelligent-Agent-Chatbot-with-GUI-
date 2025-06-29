# Intelligent-Agent-Chatbot-with-GUI
Multi-agent chatbot application in Python (With GUI)  

## Overview
This project is an interactive **multi-agent chatbot** application developed in **Python**, featuring a graphical user interface (GUI) that enables users to interact with three distinct agents:
- **Research Agent**: Answers research-based questions using external tools (search, Wikipedia, save to file).
- **Chat Agent**: Responds in a friendly, casual, and humorous way.
- **Math Agent**: Solves mathematical expressions and explains step-by-step.

The user types a query, selects the desired agent, and receives a text response both on-screen and via **text-to-speech (TTS)**.  
## Tech Stack
- **Python 3.x**-Programming Language
- **Tkinter** – GUI framework
- **pyttsx3** – Text-to-Speech functionality
- **dotenv** – Secure management of environment variables (e.g. API keys)
- **pydantic** – For data validation and structured response parsing
- **langchain** – Integration with LLMs (Mistral-7B via OpenRouter API)
- **multithreading** – For smooth user experience and responsive UI

## System Architecture
- - **Frontend (GUI)**:
  - Built using Tkinter
  - Text input/output areas
  - Agent selection interface
- **Agents**:
  - `Research Agent`: Performs search and saves content to file
  - `Chat Agent`: Friendly dialog agent
  - `Math Agent`: Parses and solves math expressions step-by-step
- **Services**:
  - Text-to-speech engine
  - Logging user interactions to `research_output.txt`
  - API key loading via `.env`
- **External APIs**:
  - **OpenRouter API**: Connects to Mistral-7B LLM
  - **Wikipedia/Search Tools** for information retrieval

## Challenges Faced
Handling structured response formatting from LLMs – solved using pydantic
Safe environment variable management – solved using python-dotenv
Concurrency issues with TTS and user interaction – addressed with threading
Finding an affordable/open LLM – resolved with OpenRouter + Mistral-7B  

## Contact:  
**Email:** mirsini.kafetsi@gmail.com  
**LinkedIn:** linkedin.com/in/myrsini-kafetsi  

Developed for the course: Intelligent Agents,
Department of Informatics, University of Piraeus


