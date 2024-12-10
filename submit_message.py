import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

# Function to send the email
def send_email(name, email, message):
    from_email = "your_email@example.com"
    to_email = "jjustinslee@gmail.com"
    subject = "New Message from Contact Form"

    # Create the email body
    body = f"Message from: {name} ({email})\n\n{message}"

    # Set up the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login("your_email@example.com", "your_password")
            server.sendmail(from_email, to_email, msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('contact.html', 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/submit_message':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            form_data = parse_qs(post_data.decode('utf-8'))

            name = form_data.get('name', [''])[0]
            email = form_data.get('email', [''])[0]
            message = form_data.get('message', [''])[0]

            send_email(name, email, message)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"We will get back to you soon.")
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Starting server on port 8080...")
    httpd.serve_forever()