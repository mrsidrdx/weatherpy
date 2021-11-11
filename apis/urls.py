from .views import LoginAPI, LogoutAPI, get_weather_info_list, send_weather_report_mail
from django.urls import path

urlpatterns = [
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('get-weather-data/', get_weather_info_list, name='get_weather_data'),
    path('send-weather-report-mail/', send_weather_report_mail, name='send_weather_report_mail'),
]