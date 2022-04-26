#daily_status_report
""" Retrieves: \
        1. last row of FITS Count file
        2. List of any files not yet uploaded to GMN Database \
    as email and / or text message.\
    Run as either cron job or call from RMS external script.\
    Expects smtp server installed locally.\
    version 0.6.1 - added check of FILES_TO_UPLOAD.inf.\
    version 0.6 - convert to using tail command"""
        
import smtplib
import os
import subprocess # requires python 3.5 or higher

""" Initialize parameters \
        Carrier sms gateways:\
            TMobile - @tmomail.net \
            Verizon - @vtext.com \
            ATT - @txt.att.net    """

send_email = True
send_text = False
from_addr = 'us000?gmn@gmail.com'
to_addr = 'myself@me.com', 'someone@gmail.com'
sms_gateway = '5555555555@txt.att.net'
path_to_fits_counts_file = "/home/pi/RMS_data/csv/US000?_fits_counts.txt" 
path_to_files_to_upload_file = "/home/pi/RMS_data/FILES_TO_UPLOAD.inf"


""" Open the fits_count file and get last row"""  
last_line = subprocess.run(['tail','-1', path_to_fits_counts_file], capture_output=True, text=True)

""" Check whether any files remain to be uploaded"""

filesize = os.path.getsize(path_to_files_to_upload_file)
if (filesize == 0):
    upload_status = "    All files uploaded"
else:
    with open(path_to_files_to_upload_file, 'r') as upload_file:
        upload_status = "Files not uploaded:\r\n" + upload_file.read()
    

""" Open an instance of the smtp client"""  

client = smtplib.SMTP('localhost')

""" Compose and send email and / or sms message """

status_msg = ("""\
    Subject: US000? Daily Status Report

    """ + str(last_line.stdout) + upload_status)
 
if send_email:    
    client.sendmail(from_addr,to_addr,status_msg)  
    
if send_text:
    client.sendmail(from_addr,sms_gateway,status_msg)
    
client.quit()

