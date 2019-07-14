# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time
import pymongo
#-------------------------------------------------
client = pymongo.MongoClient()
db = client.noval
collection = db.xiuzhen
#-------------------------------------------------
t = 1
c = 0
while True:
    t += 1
    url = 'https://www.booktxt.net/1_1439/'
    headers = {
        'User_Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2)' +
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    r = requests.get(url, headers=headers).content
    bs = BeautifulSoup(r, 'lxml', from_encoding='utf-8')
    for each in bs.find_all(class_="box_con"):
        for i in each.find_all('a'):
            href = i.get('href')
            title = i.string
            href = url + href
            if href.find('html') == -1:
                pass
            else:
                if collection.find_one({'Link':href}) == None:

                    response = requests.get(href, headers=headers).content
                    r = BeautifulSoup(response, 'lxml', from_encoding='uft-8')
                    content = r.find_all(id="content")[0]
                    content = str(content).replace('<br/>', '\n')
                    content = content.replace('<div id="content">', '')

                    mail_host = "smtp.gmail.com"  
                    mail_user = "Email account"  
                    mail_pass = "Password" 

                    sender = 'Same as mail_user'  
                    receivers = ['Receiver email address']  

                    title = title  
                    message = MIMEText(content, 'plain', 'utf-8')  
                    message['From'] = "{}".format(sender)
                    message['To'] = ",".join(receivers)
                    message['Subject'] = title

                    try:
                        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  
                        smtpObj.login(mail_user, mail_pass)  
                        smtpObj.sendmail(sender, receivers, message.as_string())  
                        print("mail has been send successfully.")
                    except smtplib.SMTPException as e:
                        print(e)


                    collection.insert_one({'Title':title,'Link':href})
                    c = c + 1

    if c == 0:
        print("running " +str(t) + " times," + " no new chapter find")
    else:
        print("running " +str(t) + " times," + ' Find new chapter')
        c = 0
    time.sleep(86400)
