from django.core.mail import EmailMessage
from django.conf import settings
import os
from json_excel_converter import Converter 
from json_excel_converter.xlsx import Writer
import re

# Send emails to the receivers list with the weather report
def send_mass_mail(receivers, excel_file_path):
    msg = EmailMessage('Weather Report', 'Here is your weather report!', settings.EMAIL_HOST_USER, receivers)
    msg.content_subtype = "html"  
    msg.attach_file(excel_file_path)
    msg.send()

# Generate the excel file with the weather report
def generate_excel_report(weather_data):
    file_name = os.path.join(settings.MEDIA_ROOT, 'weather_report.xlsx')
    conv = Converter()
    conv.convert(weather_data, Writer(file=file_name))
    return file_name

# Validate email address
def validate_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex,email)):
        return True
    else:   
        return False
