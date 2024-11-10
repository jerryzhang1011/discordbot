import os
import requests
# https://openweathermap.org/api/one-call-3
class WeatherForecast:
    def __init__(self):

        self.api_key = os.getenv('WEATHER_API_KEY')
        self.geo_decode = {
            "Waterloo": (43.464258,-80.52041),
            "Toronto": (43.653226,-79.383184)
        }

    def get_weather(self, city):
        url = f'https://api.openweathermap.org/data/3.0/onecall?lat={self.geo_decode[city][0]}&lon={self.geo_decode[city][1]}&appid={self.api_key}&units=metric'
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Debug - Error Response: {res.text}")
        data = res.json()
        if res.status_code == 200:
            current_temp = data['current']['temp']
            mintemp_c = data['daily'][0]['temp']['min']
            maxtemp_c = data['daily'][0]['temp']['max']
            daily_temp = data['daily'][0]['temp']['day']
            eve_temp = data['daily'][0]['temp']['eve']
            humidity = data['current']['humidity']
            daily_rain_chance = data['daily'][0]['pop']
            description = data['daily'][0]['weather'][0]['description']
        
            weather_info = (
                f"{city} 的天气情况如下:\n"
                f"当前气温: {current_temp} °C\n"
                f"白天平均气温 {daily_temp} °C\n"
                f"傍晚平均气温 {eve_temp} °C\n"
                f"最高气温 {maxtemp_c} °C\n"
                f"最低气温 {mintemp_c} °C\n"
                f"湿度: {humidity}%\n"
                f"天气: {description}\n"
                f"降水概率: {daily_rain_chance}%\n"
                
            )
            return weather_info
        else:
            print(f"Error: Unable to fetch weather data for {city}. Please check the city name or API key.")


    def get_weather_report(self):
        waterloo_weather = self.get_weather("Waterloo")
        toronto_weather = self.get_weather("Toronto")
        
        report = f"{waterloo_weather}\n \n{toronto_weather}"
        return report



# print(WeatherForecast().get_weather_report())
