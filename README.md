ProvizAI – Smart Banking Chatbot

ProvizAI is an AI‑powered chatbot designed to provide real‑time banking insights such as deposits, loans, transactions, and customer analytics. It integrates Google Gemini for natural language understanding and supports parallel function calling, enabling simultaneous retrieval of multiple datasets for faster, more comprehensive responses.

Features:
Natural language banking queries powered by Google Gemini.
Parallel function calling to fetch multiple datasets (e.g., deposits + revenue) in a single response.
Secure AES‑encrypted communication between frontend and backend.
Real-time analytics on deposits, loans, transactions, and customer demographics.
Flask API backend with database logging of user chats.

Designed for seamless integration with banking dashboards or apps.

Tech Stack

Backend:

Python (Flask)

Google Gemini API

MySQL (chat history logging)

Security:

AES Encryption (request/response)

Architecture:

REST API endpoints for AI response and chat retrieval

Parallel API calls for analytics data fetching

Other Tools:

Flask-CORS for cross-origin support

JSON/Gzip compression for optimized API responses

API Endpoints:

GET /GetAIResponse:-

Accepts encrypted user input.

Returns AI‑generated response (natural language).

GET /GetAIChat :- Fetches past chat history for a user (decrypted).
