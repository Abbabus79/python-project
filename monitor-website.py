import requests
import smtplib
import os
import paramiko
import boto3
import time
import schedule

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

ec2_client = boto3.client('ec2', region_name="us-west-2")


def restart_server_and_container():
    # restart ec2 server
    print('Rebooting the server...')
    nginx_server = ec2_client.load()
    nginx_server.reboot()

    # restart the application
    while True:
        nginx_server = ec2_client.load()
        if nginx_server.status == 'running':
            time.sleep(5)
            restart_container()
            break


def send_notification(email_msg):
    print('Sending an email...')
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f"Subject: SITE DOWN\n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)


def restart_container():
    print('Restarting the application...')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='139.162.130.236', username='root',
                key_filename='/Users/nanajanashia/.ssh/id_rsa')
    stdin, stdout, stderr = ssh.exec_command('docker start c3e706bc905e')
    print(stdout.readlines())
    ssh.close()


def monitor_application():
    try:
        response = requests.get('http://li1388-236.members.linode.com:8080/')
        if response.status_code == 200:
            print('Application is running successfully!')
        else:
            print('Application Down. Fix it!')
            msg = f'Application returned {response.status_code}'
            send_notification(msg)
            restart_container()
    except Exception as ex:
        print(f'Connection error happened: {ex}')
        msg = 'Application not accessible at all'
        send_notification(msg)
        restart_server_and_container()


schedule.every(5).minutes.do(monitor_application)

while True:
    schedule.run_pending()
