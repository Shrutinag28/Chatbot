from forecasting import SalesForecaster
from chatgpt_api import ChatGPTAPI

class ChatBot:
    def __init__(self):
        self.forecaster = SalesForecaster()
        self.chatgpt_api = ChatGPTAPI()
    
    def process_message(self, message):
        # Check if the message is related to sales forecasting
        if 'forecast' in message.lower():
            # Get the sales data and pass it to the forecasting model
            sales_data = [
                {'store_id': 1, 'date': '2023-01-01', 'weekly_sales': 10000},
                {'store_id': 2, 'date': '2023-01-02', 'weekly_sales': 12000},
                {'store_id': 1, 'date': '2023-01-08', 'weekly_sales': 11500},
                {'store_id': 2, 'date': '2023-01-09', 'weekly_sales': 13000},
            ]
            forecast = self.forecaster.predict(sales_data)
            
            # Generate a response based on the sales forecast
            response = f"Based on the sales forecasting model, we predict that sales will increase by {forecast}% next quarter."
        else:
            # Use the ChatGPT API to generate a response to the user's message
            response = self.chatgpt_api.generate_response(message)
        
        return response