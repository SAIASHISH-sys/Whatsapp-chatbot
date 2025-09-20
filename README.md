# WhatsApp Chatbot with LangChain and Gemini

This project is a sophisticated WhatsApp chatbot powered by Google's Gemini Pro model through the LangChain framework. It uses Flask for the web server and Twilio for WhatsApp messaging integration.

## Features

- **Conversational AI**: Utilizes Google's Gemini model for intelligent and human-like conversations.
- **Session Management**: Maintains a unique conversation history for each user.
- **WhatsApp Integration**: Seamlessly connects with WhatsApp using the Twilio API.
- **Flask Backend**: A lightweight and robust web server to handle webhook requests.
- **Customizable Persona**: The chatbot's personality can be easily configured in the prompt template.

## Prerequisites

Before you begin, ensure you have the following installed and configured:

- Python 3.8+
- `pip` (Python package installer)
- [ngrok](https://ngrok.com/download) for local development and testing.
- A [Twilio account](https://www.twilio.com/try-twilio) with a WhatsApp-enabled phone number.
- A [Google API Key](https://aistudio.google.com/app/apikey) with access to the Gemini API.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    A `requirements.txt` file is needed. You can create one with the following content:
    ```
    python-dotenv
    Flask
    langchain-google-genai
    langchain-core
    langchain-community
    twilio
    gunicorn
    ```
    Then run:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **Create a `.env` file** in the root of your project directory.

2.  **Add the following environment variables** to the `.env` file with your credentials:
    ```
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
    TWILIO_ACCOUNT_SID="YOUR_TWILIO_ACCOUNT_SID"
    TWILIO_AUTH_TOKEN="YOUR_TWILIO_AUTH_TOKEN"
    ```

## Running the Application

1.  **Start the Flask application:**
    ```bash
    gunicorn app:app
    ```
    The application will start on `http://127.0.0.1:8000`.

2.  **Expose your local server to the internet using ngrok:**
    Open a new terminal and run:
    ```bash
    ngrok http 8000
    ```
    ngrok will provide you with a public URL (e.g., `https://<unique-id>.ngrok.io`). Copy this URL.

## Usage

1.  **Configure the Twilio Webhook:**
    - Go to your Twilio console and navigate to the WhatsApp Sandbox settings (or your specific WhatsApp sender settings).
    - In the "WHEN A MESSAGE COMES IN" field, paste your ngrok forwarding URL and append `/webhook`. It should look like this:
      `https://<unique-id>.ngrok.io/webhook`
    - Make sure the HTTP method is set to `POST`.
    - Save the configuration.

2.  **Start Chatting:**
    - Send a message to your Twilio WhatsApp number from your phone.
    - The chatbot will respond, and you can start a conversation.

---
*This chatbot was built by SAI ASHISH MISHRA.*
