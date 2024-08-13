import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from decouple import config
import json
from formatter import format_transaction_details, format_transactions_to_excel

# Load transaction data from JSON
with open('statement.json') as file:
    transactions = json.load(file)

# Loop through transactions and format each one
formatted_transactions = ""
for transaction in transactions:
    formatted_transactions += format_transaction_details(transaction) + "\n"

def send_email():
    # Email configuration
    sender_email = "daemonlite73@gmail.com"
    receiver_email = "paakwesinunoo135@gmail.com"
    subject = "Transaction Statement"
    body = 'Kindly find the attached transaction statement. Thank you!'

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Generate the Excel file with transactions
    excel_file = format_transactions_to_excel(transactions)
    filename = "transaction_statement.xlsx"

    # Attach the file
    attachment = MIMEBase('application', 'octet-stream')
    with open(excel_file, "rb") as file:
        attachment.set_payload(file.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename={filename}')
    msg.attach(attachment)

    # Sending the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, config('EMAIL_HOST_PASSWORD'))
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
        
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

send_email()
