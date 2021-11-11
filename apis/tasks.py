from weatherpy.celery import app
import requests
from django.conf import settings
from .models import AccountManager, EmailAddresses

# Celery task to send emails of Weather excel report every 30 minutes
@app.task(name='send_weather_report_email_task')
def send_weather_report_email_task():
    print('Sending weather report summary')
    email_objects = EmailAddresses.objects.values_list('email_address', flat=True)
    email_list = list(email_objects)
    try:
        account_manager = AccountManager.objects.get(username='mrsidrdx')
    except AccountManager.DoesNotExist:
        return {'error': 'Account manager does not exist'}
    access_token = account_manager.token
    session = requests.Session()
    session.headers.update({'Authorization': 'Token {0}'.format(access_token)})
    response = session.post('{0}/api/send-weather-report-mail/'.format(settings.HOSTNAME_URL),
                json = {'email_list':email_list}
                ).json()
    return response