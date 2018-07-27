from flask import Flask, render_template, request, redirect
from flask_restful import Resource, Api
import json, string, random, os
from urllib.parse import urlsplit, urlencode, quote_plus
from urllib.request import urlopen, Request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
api = Api(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    return response

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            result = request.form
            fjson = 'data.json'

            if not os.path.isfile(fjson):
                with open(fjson, 'w+') as outfile:
                    json.dump({}, outfile)

            number = '91'+ result['mobile'].strip()
            recipient = result['email'].strip()
            url = result['querystring'].strip()
            
            if len(url) == 0 or len(recipient) == 0 or len(number) == 0:
                errorResp = {}
                errorResp['status'] = 'Empty url or email or number'
                return json.dumps(errorResp)
            shorturl= url_generator()

            with open(fjson) as json_file:
                json_decoded = json.load(json_file)

            for key, value in json_decoded.items():
                 if value == url:
                    emailStatus = send_mail(recipient, request.url_root+key, value)
                    message = "Please pay using this link: " + request.url_root+key
                    smsResp = sendSMS(number, message)
                    exitResp = {}
                    exitResp['status'] = 'success'
                    exitResp['shortURL'] = request.url_root+key
                    exitResp['upiLink'] = value
                    exitResp['emailStatus'] = emailStatus
                    exitResp['smsResp'] = 'smsResp'
                    exitJson = json.dumps(exitResp)
                    return str(exitJson)

            json_decoded[shorturl] = url

            with open(fjson, 'w+') as json_file:
                json.dump(json_decoded, json_file)

            emailStatus = send_mail(recipient, request.url_root+shorturl, json_decoded[shorturl])
            message = "Please pay using this link: " + request.url_root+shorturl
            smsResp = sendSMS(number, message)
            newResp = {}
            newResp['status'] = 'success'
            newResp['shortURL'] = request.url_root+shorturl
            newResp['upiLink'] = json_decoded[shorturl]
            newResp['emailStatus'] = emailStatus
            newResp['smsResp'] = 'smsResp'
            newJson = json.dumps(newResp)
            return str(newJson)
        except:
            errorResp = {}
            errorResp['status'] = 'failed'
            return json.dumps(errorResp)
        

    return render_template('index.html')


class URLSHORT(Resource):
    def get(self, url):
        try:
            with open('data.json') as json_file:
                json_decoded = json.load(json_file)
            if url in json_decoded:
                return redirect(json_decoded[url])
            errorResp = {}
            errorResp['status'] = 'Wrong ShortURLy!'
            return json.dumps(errorResp)
        except:
            errorResp = {}
            errorResp['status'] = 'Something Wrong! Please retry.'
            return json.dumps(errorResp)
        


def url_generator(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def sendSMS(number, message):
    apikey = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    numbers = number
    data =  urlencode({'apikey': apikey, 'numbers': numbers, 'message' : message})
    data = data.encode('utf-8')
    request = Request("https://api.textlocal.in/send/?")
    f = urlopen(request, data)
    fr = f.read()
    return(fr)


def send_mail(recipient, shorturl, url):

    user="xxxxxx@gmail.com"
    pwd="xxxxxxxxx"

    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = recipient
    msg['Subject'] = "New Payment Request From BillionLoans"
    body = "Please pay using this link {0} ".format(shorturl)
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        message = msg.as_string()
        server.sendmail(msg['From'], msg['To'], message)
        server.close()
        return "Success"
    except:
        return "Failed"


api.add_resource(URLSHORT, '/<url>')

if __name__ == '__main__':
   app.run(host='0.0.0.0',debug=True)
