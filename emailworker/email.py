from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.config import configuration, EMAIL_SENT_HISTORY
import datetime
import smtplib
import logging

_email_logger = logging.getLogger("email")

def can_send_email(service_name, now):
    last_sent = EMAIL_SENT_HISTORY.get(service_name)
    if last_sent and (now - last_sent).total_seconds() < 1800:  # 1800 seconds = 30 minutes
        return False
    return True

def should_send_email(service_name):
    now = datetime.datetime.now()
    last_email_time = EMAIL_SENT_HISTORY.get(service_name)
    if last_email_time and (now - last_email_time).total_seconds() < 1800:
        return False
    return True

def send_email(service_name, status):
    now = datetime.datetime.now()
    if not can_send_email(service_name, now):
        last_sent = EMAIL_SENT_HISTORY.get(service_name).strftime("%Y-%m-%d %H:%M:%S")  # Format the last sent time
        _email_logger.warn(f"Alert email already sent for {service_name} at {last_sent} as it was in {status} state.")  # Include the last sent time in the message
        return False
        
    # Customize your email settings
    sender_email = configuration.get_property("sender_email")
    host = configuration.get_property("host")
    password = configuration.get_property("password")
    
    receiver_emails = configuration.get_property("receiver_emails")
    cc_emails = configuration.get_property("cc_emails")
    all_recipients = receiver_emails + cc_emails  # Combine recipients and CCs for the sendmail function

    message = MIMEMultipart()
    message["From"] = sender_email
    message['To'] = ", ".join(receiver_emails)  # Join the list into a single string separated by commas
    message['Cc'] = ", ".join(cc_emails)  # Do the same for CCs
    message["Subject"] = f"Alert: {service_name} is stopped"

    body = f"""\
                <html>
                <head></head>
                <body>
                    <p>Hi,</p>
                    <p>The <b>{service_name}</b> service is in <b>{status}</b> state. Please carry out system checks.</p>
                    <p>Thanks</p>
                </body>
                </html>
            """
    message.attach(MIMEText(body, "html"))
    try:
        server = smtplib.SMTP(host, 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, all_recipients, message.as_string())
        server.quit()
        EMAIL_SENT_HISTORY[service_name] = now
        email_sent_time = now.strftime("%Y-%m-%d %H:%M:%S")
        _email_logger.info(f"Alert mail sent for {service_name} at {email_sent_time} as it is in {status} state.")
        return True
    except Exception as e:
        _email_logger.error(f"Failed to send email for {service_name}: {str(e)}")
        return False