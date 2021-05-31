import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime   
import imaplib
import sys
import json
from dotenv import load_dotenv
load_dotenv()
class Backup:    
    def __init__(self):    
                              
        self.date=datetime.now().strftime("%d.%m.%Y_%H:%M:%S")          
        self.clients=json.load(open('projects.json',))
        self.backDirectory=os.getenv('BACKUP_DIRECTORY') 
        self.senderEmail=os.getenv('SENDER_EMAIL')   
        self.senderPass=os.getenv('SENDER_PASSWORD')
        self.receiverEmail=os.getenv('RECEIVER_EMAIL')
        self.ServerName=os.getenv('SERVER_NAME')
        
    def startBackup(self,client):         
        DbName=client['db_name']
        DbPassword=client['db_password']
        DBUserName=client['db_username']
        os.system("cd "+self.backDirectory+" && pg_dump postgresql://"+DBUserName+":"+DbPassword+"@127.0.0.1:5432/"+DbName+" > "+DbName+"_"+self.date+".sql")
        print('processing '+client['domain']+' at '+self.date)
        
    def sendBackupEmail(self,db_name,domain):
    
        prepareMessage = MIMEMultipart()
        prepareMessage['From'] = self.senderEmail
        prepareMessage['To'] = self.receiverEmail
        prepareMessage['Subject'] =domain+' has been backed up at '+self.date      
        body ='''
                <br>
                Server: <b>{}</b>
                <br>
                Domain: <b>{}</b>
                <br>    
                Database Name: <b>{}</b>
                <br>
                Backup Time: <b>{}</b>
                <br>
                Backup File: <b>{}_{}.sql</b>
                '''.format(self.ServerName,domain,db_name,self.date,db_name,self.date)
        prepareMessage.attach(MIMEText(body, 'html'))
        filename = self.backDirectory+db_name+'_'+self.date+".sql"
        attachment = open(self.backDirectory+db_name+'_'+self.date+".sql", "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        prepareMessage.attach(part)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.senderEmail, self.senderPass)
        text = prepareMessage.as_string()
        server.sendmail(self.senderEmail, self.receiverEmail, text)
        server.quit()
        print('sent email to '+domain)
        
    def destroyBackUps(self):

        print("\nstart deleting backups")
        os.system("find "+self.backDirectory+" -iname '*.sql' -exec rm -r {} \;")
        print("all backups have been deleted")

    def deleteSentEmails(self):  
        
        print('\ndeleting emails')     
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(self.senderEmail, self.senderPass)
        mail.select('"[Gmail]/Sent Mail"')
        typ, data = mail.search(None, 'ALL')
        mail.store('1:*', '+X-GM-LABELS', '\\Trash')             
        mail.expunge()
        print('finished \n')
        
    def process(self):
    
        print('backing up \n')
        for client in self.clients:            
            self.startBackup(client)
            self.sendBackupEmail(client['db_name'],client['domain'])
        self.destroyBackUps()
        self.deleteSentEmails()            
        print('\ndone backing up')
        
start = Backup()
start.process()
