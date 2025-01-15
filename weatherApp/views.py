import urllib.request
import json
from django.shortcuts import render
from urllib.parse import urlencode, quote_plus

def index(request):
    data = {}  # Initialize data variable to avoid issues when it's empty

    if request.method == 'POST':
        city = request.POST.get('city', '').strip()  # Get city input and remove leading/trailing spaces

        if not city:
            data['error'] = "Please enter a city name."  # If city is empty, show an error
        else:
            # Use urlencode to properly encode query parameters
            params = {
                'q': city,
                'units': 'metric',
                'appid': '837e7a0b5ffcfa7310470e42e60ee3af'
            }
            url = 'http://api.openweathermap.org/data/2.5/weather?' + urlencode(params, quote_via=quote_plus)

            # Debugging: Print the constructed URL to check correctness
            print("Requesting URL:", url)

            # Make the API request
            response = urllib.request.urlopen(url)
            source = response.read()

            if response.status == 200:  # Check if the response was successful (HTTP 200 OK)
                list_of_data = json.loads(source)

                # Process the data from the API response
                data = {
                    "country_code": str(list_of_data['sys']['country']),
                    "coordinate": str(list_of_data['coord']['lon']) + ', ' + str(list_of_data['coord']['lat']),
                    "temp": str(list_of_data['main']['temp']) + ' °C',
                    "pressure": str(list_of_data['main']['pressure']),
                    "humidity": str(list_of_data['main']['humidity']),
                    'main': str(list_of_data['weather'][0]['main']),
                    'description': str(list_of_data['weather'][0]['description']),
                    'icon': list_of_data['weather'][0]['icon'],
                }
            else:
                data['error'] = "Failed to retrieve data. Please check the city name or try again later."

    return render(request, "html/index.html", data)
