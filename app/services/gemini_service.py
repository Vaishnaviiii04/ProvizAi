# Place your GetPromptResponse function here
def GetPromptResponse(user_input: str) -> str:
    """
    Dummy function to simulate getting a response from an AI model.
    In a real application, this would integrate with an actual LLM API.
    """
    if "hello" in user_input.lower():
        return f"Hello there! You said: '{user_input}'. How can I assist you today?"
    elif "time" in user_input.lower():
        import datetime
        return f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}."
    elif "joke" in user_input.lower():
        return "Why don't scientists trust atoms? Because they make up everything!"
    else:
        return f"This is a hardcoded AI response based on your input: '{user_input}'. " \
               f"In a real scenario, I'd provide a more dynamic answer!"

# If EncryptionService is ONLY used by the AI response, it could stay here.
# But since encryption/decryption is a general utility, moving it to app/services/encryption_service.py is better.