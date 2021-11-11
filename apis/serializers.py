from rest_framework import serializers

# WeatherInfo Class to create the object of OpenWeatherMapAPI response
class WeatherInfo(object):
    def __init__(self, lon, lat, weather_id, weather_main, weather_description, weather_icon, base, temp, feels_like, temp_min, temp_max, pressure, humidity, sea_level, grnd_level, visibility, wind_speed, wind_deg, wind_gust, clouds_all, dt, sys_country, sys_sunrise, sys_sunset, timezone, id, city_name, cod):
        self.lon = lon
        self.lat = lat
        self.weather_id = weather_id
        self.weather_main = weather_main
        self.weather_description = weather_description
        self.weather_icon = weather_icon
        self.base = base
        self.temp = temp
        self.feels_like = feels_like
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.pressure = pressure
        self.humidity = humidity
        self.visibility = visibility
        self.sea_level = sea_level
        self.grnd_level = grnd_level
        self.wind_speed = wind_speed
        self.wind_deg = wind_deg
        self.wind_gust = wind_gust
        self.clouds_all = clouds_all
        self.dt = dt
        self.sys_country = sys_country
        self.sys_sunrise = sys_sunrise
        self.sys_sunset = sys_sunset
        self.timezone = timezone
        self.id = id 
        self.city_name = city_name
        self.cod = cod

# WeatherInfoSerializer class to serialize the object of WeatherInfo class
class WeatherInfoSerializer(serializers.Serializer):
    city_name = serializers.CharField()
    lon = serializers.FloatField()
    lat = serializers.FloatField()
    weather_id = serializers.IntegerField()
    weather_main = serializers.CharField()
    weather_description = serializers.CharField()
    weather_icon = serializers.CharField()
    base = serializers.CharField()
    temp = serializers.FloatField()
    feels_like = serializers.FloatField()
    temp_min = serializers.FloatField()
    temp_max = serializers.FloatField()
    pressure = serializers.FloatField()
    humidity = serializers.FloatField()
    sea_level = serializers.FloatField()
    grnd_level = serializers.FloatField()
    visibility = serializers.FloatField()
    wind_speed = serializers.FloatField()
    wind_deg = serializers.FloatField()
    wind_gust = serializers.FloatField()
    clouds_all = serializers.FloatField()
    dt = serializers.IntegerField()
    sys_country = serializers.CharField()
    sys_sunrise = serializers.IntegerField()
    sys_sunset = serializers.IntegerField()
    timezone = serializers.IntegerField()
    id = serializers.IntegerField()
    cod = serializers.IntegerField()
