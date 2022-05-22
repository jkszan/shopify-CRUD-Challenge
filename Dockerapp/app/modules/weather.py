from flask import g
import requests
from os import environ

# This file implements calls to the OpenWeatherAPI

def getWeather(city, country):

    openWeatherKey = environ['WEATHER_APIKEY']

    # Calling open weather API as json
    apiCall = 'https://api.openweathermap.org/data/2.5/weather?q={},{}&APPID={}&units=metric'.format(city, country, openWeatherKey)
    resp = requests.get(apiCall)

    # Raising error if API Call did not return successfully
    resp.raise_for_status()

    # Converting response data to readable dict
    jsonResp = resp.json()

    # Parsing information from API return
    temp = jsonResp["main"]["temp"]
    feels_like = jsonResp["main"]["feels_like"]
    humidity = jsonResp["main"]["humidity"]
    windspeed = jsonResp["wind"]["speed"]
    weather = jsonResp["weather"][0]

    # Creating a description of this city's weather
    currentWeather = 'Currently, it is {}°C and feels like {}°C. There {} with a humidity of {} and a windspeed of {}km/h'
    weatherDescription = formatWeatherDescription(weather['id'], weather['description'])

    g.appLogger.info('Got weather information for {}, {}'.format(city, country) )

    return currentWeather.format(temp, feels_like, weatherDescription, humidity, windspeed)

# This helper function creates a gramatically correct description based on the weather code returned by the API
def formatWeatherDescription(weatherCode, description):

    weatherDescription = 'is indeterminate weather'

    if (weatherCode < 600 or weatherCode == 800):
        weatherDescription = 'is a {}'.format(description)

    if (weatherCode > 800):
        weatherDescription = 'are {}'.format(description)

    if (weatherCode == 781):
        weatherDescription = 'is an active tornado'

    if (weatherCode == 771):
        weatherDescription = 'are squals throughout'

    if (weatherCode < 771 and weatherCode >= 700):
        weatherDescription = 'is {} throughout'.format(description)

    return weatherDescription