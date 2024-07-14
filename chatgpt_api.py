import openai

class ChatGPTAPI:
    def __init__(self):
        # Initialize the ChatGPT API with your API key
        openai.api_key = "sk-proj-rctCdZEavxbB7AyPTknkT3BlbkFJi3BK2phc9WXf14ERi8tR"
    
    def generate_response(self, message):
        # Use the ChatGPT API to generate a response to the user's message
        response = openai.Completion.create(
            engine="davinci",
            prompt=message,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        
        return response.choices[0].text.strip()