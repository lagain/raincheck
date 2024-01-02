import requests
from twilio.rest import Client
import time

def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    return data

def send_text(account_sid, auth_token, from_number, to_number, message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body = message,
        from_ = from_number,
        to = to_number
    )
    return message.sid

def main():
    # OpenWeatherMap API key and city
    openweather_api_key = "YOUR_OPENWEATHERMAP_API_KEY"
    city_name = "YOUR_CITY_NAME"

    # Twilio SID, auth token, and Twilio phone number
    twilio_account_sid = "YOUR_TWILIO_ACCOUNT_SID"
    twilio_auth_token = "YOUR_TWILIO_AUTH_TOKEN"
    twilio_from_number = "YOUR_TWILIO_PHONE_NUMBER"

    # Phone number of recipient
    to_phone_number = "RECIPIENT_PHONE_NUMBER"

    while True:
        weather_data = get_weather(openweather_api_key, city_name)
        weather_description = weather_data['weather'][0]['description']
        rain_keywords = ['rain', 'drizzle', 'thunderstorm']

        if any(keyword in weather_description.lower() for keyword in rain_keywords):
            message = f"Move your car! There's bad weather in {city_name}. Weather: {weather_description}"
            send_text(twilio_account_sid, twilio_auth_token, twilio_from_number, to_phone_number, message)

        # Check the weather every hour (adjust time.sleep() value as needed)
        time.sleep(3600)

if __name__ == "__main__":
    main()
