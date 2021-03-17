import random
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

gmail_user = 'foo@example.com'
gmail_password = ''


def mail_students(students):
    presenter = random.choice(list(students.keys()))
    sent_from = gmail_user
    for email in students:
        to = email
        subject = 'Scores'
        if email == presenter:
            print(f"{to} is presenter")
            note = "\nYou’ve been randomly chosen to present a summary of the book in the next class. Looking forward to it!\n"
        else:
            note = ''
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sent_from
        message["To"] = to
        text = """\
        Dear %s, Your score for the book assignment is broken down below by question number.
        
        1. %s %s
        2. %s %s
        3. %s %s
        
        %s
    
        """ % (students[email][1], students[email][2], students[email][3], students[email][4], students[email][5], students[email][6],
               students[email][7], note)

        html = """\
        <html>
            <body>
            <p>Dear %s, Your score for the book assignment is broken down below by question number.</p>
            <ul>
                <li>%s %s</li>
                <li>%s %s</li>
                <li>%s %s</li>
            </ul>
            %s
            </body>
        <html>
        """ % (students[email][1], students[email][2], students[email][3], students[email][4], students[email][5], students[email][6],
               students[email][7], note)

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(gmail_user, gmail_password)
                server.sendmail(
                    sent_from, to, message.as_string()
                )

            print('Email sent!')
        except Exception as err:
            print(f'Something went wrong... {err}')


def read_input(filename):
    students = {}
    f = open(filename, "r")
    for x in f:
        name, data = x.split(',', 1)
        students[name] = data.rstrip("\n").split(',')
    return students


if __name__ == "__main__":
    mail_students(read_input('exam.csv'));
