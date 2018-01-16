def send_mail(send_from, send_to, subject, text, files=None,
              server="127.0.0.1"):
    
    import smtplib

    from os.path import basename
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.utils import COMMASPACE, formatdate    
    
    
    #assert isinstance(send_to, list)

    #retrieve password from file on sharc
    with open ('/home/pc1tsx/secret/password.txt', "r") as myfile:
        password=myfile.read().replace('\n', '') 
        
    msg = MIMEMultipart(
        From=send_from,
        To=COMMASPACE.join(send_to),
        Date=formatdate(localtime=True),
        Subject=subject
    )
    msg.attach(MIMEText(text))

    msg['Subject']=subject
    msg['To']=send_to

    for f in files or []:
        with open(f, "rb") as fil:
            msg.attach(MIMEApplication(
                fil.read(),
                Content_Disposition='attachment; filename="%s"' % basename(f),
                Name=basename(f)
            ))

    try:
        smtp = smtplib.SMTP(server, 587,timeout=30)
        smtp.ehlo() #status
        smtp.starttls()   
        smtp.ehlo() #status
        #Next, log in to the server
        smtp.login("t.stafford@sheffield.ac.uk", password)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()
        print("Successfully sent email")
    except:
       print("Error: unable to send email")
       
       
'''       
send_from='t.stafford@sheffield.ac.uk'
subject='complete email'
send_to='tom@idiolect.org.uk' 
bodytext="no body text"
send_mail(send_from,send_to,subject,bodytext,None,'smtp.gmail.com')
'''
