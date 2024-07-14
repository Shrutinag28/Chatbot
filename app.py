from flask import Flask, request, jsonify, render_template
from chatbot import ChatBot
from forecasting import SalesForecaster
from chatgpt_api import ChatGPTAPI

app = Flask(__name__)

# Initialize the chatbot, forecaster, and ChatGPT API
chatbot = ChatBot()
forecaster = SalesForecaster()
chatgpt_api = ChatGPTAPI()

@app.route('/')
def index():
    return render_template('index.html')  # Assuming you have an index.html template in your templates folder

# @app.route('/chat', methods=['POST'])
# def chat():
#     # Get the user's message from the request
#     message = request.json['message']
    
#     # Check if the message is related to sales forecasting
#     if 'forecast' in message.lower():
#         # Get the sales data and pass it to the forecasting model
#         sales_data = chatbot.get_sales_data()
#         forecast = forecaster.predict(sales_data)
        
#         # Generate a response based on the sales forecast
#         response = f"Based on the sales forecasting model, we predict that sales will increase by {forecast}% next quarter."
#     else:
#         # Use the ChatGPT API to generate a response to the user's message
#         response = chatgpt_api.generate_response(message)
    
#     return jsonify({'response': response})

if __name__ == '__main__':
    app.run()
