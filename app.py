import os
from dotenv import load_dotenv
from flask import Flask, request
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory


import logging

from twilio.twiml.messaging_response import MessagingResponse

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=os.getenv('GOOGLE_API_KEY'),
        temperature=0.7,
        max_tokens=1000
    )

except Exception as e:
    logger.error(f"Failed to initialize the language model or prompt: {e}")
    llm = None
    prompt_template = None

prompt_template = ChatPromptTemplate.from_messages([
        ("system","""You are a helpful and friendly WhatsApp chatbot who acts like a sports coach. Keep your responses:
    - Short and crisp but enthusiastic
    - Engaging and conversational
    - Use emojis occasionally 
    - helpful and concise
    - when someone asks u who build you tell my name: SAI ASHISH MISHRA"""),
    MessagesPlaceholder(variable_name="history"),
    ("human","{input}"),    
    ])
message_histories={}
def get_session_history(session_id: str) -> ChatMessageHistory:
    """
    Retrieves or creates a message history for a given session ID.
    """
    if session_id not in message_histories:
        logger.info(f"Creating new message history for session: {session_id}")
        message_histories[session_id] = ChatMessageHistory()
    return message_histories[session_id]

conversational_runnable = RunnableWithMessageHistory(
    runnable=prompt_template | llm,
    get_session_history=get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)


def get_langchain_response(message, user_id):
    try:
        # Get conversation chain for this user
        conversation = conversational_runnable.invoke( {"input": message},
            config={"configurable": {"session_id": user_id}})
        
        # Get response from LangChain
        response = conversation.content
        
        # Ensure response isn't too long for WhatsApp
        if len(response) > 1600:
            response = response[:1550] + "..."
        
        return response
        
    except Exception as e:
        logger.error(f"Error getting LangChain response: {str(e)}")
        return "Sorry, I'm having trouble processing your message right now. Please try again!"
    
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Get message details
        incoming_msg = request.values.get('Body', '').strip()
        from_number = request.values.get('From', '')
        
        logger.info(f"Received message from {from_number}: {incoming_msg}")
        
        # Skip empty messages
        if not incoming_msg:
            logger.warning("Received an empty message.")
            return '', 200
        
        # Get user ID for conversation memory
        user_id = from_number
        
        # Get response from LangChain
        bot_response = get_langchain_response(incoming_msg, user_id)
        
        # Create Twilio response
        resp = MessagingResponse()
        resp.message(bot_response)
        
        logger.info(f"Sent response to {from_number}: {bot_response[:100]}...")
        
        return str(resp)
        
    except Exception as e:
        logger.error(f"Error in webhook: {str(e)}")
        
        # Send error message to user
        resp = MessagingResponse()
        resp.message("Oops! Something went wrong. Please try again later. 🛠️")
        return str(resp)
'''
@app.route('/clear_memory/<user_id>', methods=['POST'])
def clear_user_memory(user_id):
    """
    Clear conversation memory for a specific user (useful for testing)
    """
    if user_id in message_histories:
        del message_histories[user_id]
        logger.info(f"Memory cleared for user {user_id}")
        return {'message': f'Memory cleared for user {user_id}'}, 200
    else:
        logger.warning(f"Attempted to clear memory for non-existent user: {user_id}")
        return {'message': f'No memory found for user {user_id}'}, 404
    
@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return {
            'status': 'healthy',
            'model': 'gemini-2.0-flash-exp',
            'framework': 'langchain',
            'active_conversations': len(user_conversation)
        }, 200'''

@app.route('/',methods =['GET'])
def home():
    return "THE APPLICATION IS RUNNING"

if __name__ == '__main__':
    message_histories.clear()
    # Verify environment variables
    required_vars = ['GOOGLE_API_KEY', 'TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing environment variables: {missing_vars}")
        exit(1)
    
    logger.info("Starting WhatsApp Chatbot with LangChain + Gemini 2.0 Flash...")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)