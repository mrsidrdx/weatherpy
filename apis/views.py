from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView, LogoutView as KnoxLogoutView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import api_view, permission_classes
from .serializers import WeatherInfo, WeatherInfoSerializer
import requests
from django.conf import settings
from .utils import send_mass_mail, generate_excel_report, validate_email
from django.http import JsonResponse
from .models import AccountManager

# Login API Extending from KnoxLoginView, adding extra ability to store token
# in the database to use in scheduled tasks.
# 1. A POST Request
# 2. Permissions : Allow any user to login
# 3. Request Body : {'username': 'mrsidrdx', 'password': 'mrsidrdx'}
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        login_response = super(LoginAPI, self).post(request, format=None)
        account_manager, created = AccountManager.objects.get_or_create(username=request.data['username'])
        account_manager.token = login_response.data['token']
        account_manager.save()
        return login_response

# Logout API Extending from KnoxLogoutView, adding extra ability to delete 
# AccountManager instance for the user
# 1. A POST Request
# 2. Permissions : Only authenticated user can logout
# 3. Header Body : {'Authorization': 'Token <token>'} 
# Use <token> from the response of Login API
class LogoutAPI(KnoxLogoutView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        try:
            account_manager = AccountManager.objects.get(username=request.user.username)
            account_manager.delete()
        except AccountManager.DoesNotExist:
            return JsonResponse({'message': 'Account Manager does not exist'}, status=400)
        return super(LogoutAPI, self).post(request, format=None)

# Get Weather Info API - Get weather info of 30 cities mentioned in the function
# 1. A GET Request
# 2. Permissions : Only authenticated user can access this API
# 3. Header Body : {'Authorization': 'Token <token>'}
# Use <token> from the response of Login API
# A default pagination is used to limit the number of cities returned - 10 cities
# Change limit and offset by adding query parameters to the API call
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_weather_info_list(request):
    paginator = LimitOffsetPagination()
    cities_list = ['Delhi', 'Shimla', 'Chennai', 'Bhubaneswar', 'Bangalore', 'Hyderabad', 'Ahmedabad', 'Kolkata', 'Surat', 'Pune', 'Jaipur', 'Lucknow', 'Kanpur', 'Nagpur', 'Indore', 'Thane', 'Bhopal', 'Patna', 'Vadodara', 'Ghaziabad', 'Ludhiana', 'Agra', 'Nashik', 'Ranchi', 'Faridabad', 'Meerut', 'Rajkot', 'Varanasi', 'Srinagar', 'Aurangabad']
    weather_info_list = []
    for city in cities_list:
        weather_data = requests.get('http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}'.format(city, settings.OPEN_WEATHER_MAP_API_KEY)).json()
        weather_object = WeatherInfo(
            lon = weather_data['coord']['lon'],
            lat = weather_data['coord']['lat'],
            weather_id = weather_data['weather'][0]['id'],
            weather_main = weather_data['weather'][0]['main'],
            weather_description = weather_data['weather'][0]['description'],
            weather_icon = weather_data['weather'][0]['icon'],
            base = weather_data['base'],
            temp = weather_data['main']['temp'] if 'temp' in weather_data['main'] else 0,
            feels_like = weather_data['main']['feels_like'] if 'feels_like' in weather_data['main'] else 0,
            temp_min = weather_data['main']['temp_min'] if 'temp_min' in weather_data['main'] else 0,
            temp_max = weather_data['main']['temp_max'] if 'temp_max' in weather_data['main'] else 0,
            pressure = weather_data['main']['pressure'] if 'pressure' in weather_data['main'] else 0,
            humidity = weather_data['main']['humidity'] if 'humidity' in weather_data['main'] else 0,
            sea_level = weather_data['main']['sea_level'] if 'sea_level' in weather_data['main'] else 0,
            grnd_level = weather_data['main']['grnd_level'] if 'grnd_level' in weather_data['main'] else 0,
            visibility = weather_data['visibility'],
            wind_speed = weather_data['wind']['speed'] if 'speed' in weather_data['wind'] else 0,
            wind_deg = weather_data['wind']['deg'] if 'deg' in weather_data['wind'] else 0,
            wind_gust = weather_data['wind']['gust'] if 'gust' in weather_data['wind'] else 0,
            clouds_all = weather_data['clouds']['all'],
            dt = weather_data['dt'],
            sys_country = weather_data['sys']['country'],
            sys_sunrise = weather_data['sys']['sunrise'],
            sys_sunset = weather_data['sys']['sunset'],
            timezone = weather_data['timezone'],
            id = weather_data['id'],
            city_name = weather_data['name'],
            cod = weather_data['cod']
        )
        weather_info_list.append(weather_object)
    query_set = weather_info_list
    context = paginator.paginate_queryset(query_set, request)
    serializer = WeatherInfoSerializer(context, many=True)
    return paginator.get_paginated_response(serializer.data)

# Send Weather Excel Report Via Email API
# 1. A POST Request
# 2. Permissions : Only authenticated user can access this API
# 3. Header Body : {'Authorization': 'Token <token>'}
# 4. Request Body : {'email_list': ['abc@xyz.com', 'dolphin@gmail.com']}
# Use <token> from the response of Login API
# Generated excel report from the Open Weather Map API is sent to valid email addresses.
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def send_weather_report_mail(request):
    access_token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
    receivers = request.data['email_list']
    session = requests.Session()
    session.headers.update({'Authorization': 'Token {0}'.format(access_token)})
    response = session.get('{0}/api/get-weather-data/?limit=30'.format(settings.HOSTNAME_URL)).json()
    weather_data = response['results']
    valid_email_ids = []
    for email in receivers:
        if validate_email(email):
            valid_email_ids.append(email)
    # Check whether there are any valid email ids
    if len(valid_email_ids) > 0:
        weather_report = generate_excel_report(weather_data)
        send_mass_mail(valid_email_ids, weather_report)
        return JsonResponse({
            'status' : 'success'
        })
    else:
        return JsonResponse({
            'status' : 'failure'
        })