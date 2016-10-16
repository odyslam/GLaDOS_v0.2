import poplib
from email import parser
import smtplib
from email.mime.text import MIMEText




class Mail_Client():

	def __init__(self,inc_mailserver,out_mailserver,username,password,forthnet_mail,my_mail):
		pop_conn = poplib.POP3_SSL(inc_mailserver)
		pop_conn.user(username)
		pop_conn.pass_(password)
		self.forthnet_mail = forthnet_mail
		self.my_mail = my_mail 


	def send_mail(address,subject,message):
	with open(textfile) as fp:
		fp.write(message)
		msg = MIMEText(fp.read())
	msg['Subject'] = subject
	msg['From'] = self.forthnet.mail
	msg['To'] = self.my_mail
	s = smtplib.SMTP(mailserver)
	s.send_message(msg)
	s.quit()



	def check_mail():
		pass


