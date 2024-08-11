from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from datetime import datetime
import pandas
import random
import smtplib
import os

load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
SENDER_NAME = os.getenv("NAME")

today = datetime.now()
today_tuple = (today.month, today.day)

data = pandas.read_csv("birthdays.csv")
bd_dict = {(row["month"], row["day"]): row for (index, row) in data.iterrows()}

if today_tuple in bd_dict:
    bd_person = bd_dict[today_tuple]
    random_letter = f"letter_templates/letter_{random.randint(1, 5)}.txt"

    with (open(random_letter, 'r', encoding='utf-8') as letter_file):
        contents = letter_file.read()
        contents = contents.replace("{name}", bd_person["name"]).replace("[Your Name]", SENDER_NAME)

    msg = MIMEMultipart()
    msg["FROM"] = EMAIL
    msg["To"] = bd_person["email"]
    msg['Subject'] = "Happy Birthday!"
    msg.attach(MIMEText(contents, "plain", "utf-8"))

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(EMAIL, PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=bd_person["email"],
            msg=msg.as_string()
        )
