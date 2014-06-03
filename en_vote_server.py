#coding=utf-8
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import socket
import fcntl
import struct
import string 

def get_ip_address(ifname):
	skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	pktString = fcntl.ioctl(skt.fileno(), 0x8915, struct.pack('256s', ifname[:15]))
	ipString  = socket.inet_ntoa(pktString[20:24])
	return ipString

welcome ='''

__        _______ _     ____ ___  __  __ _____ 
\ \      / / ____| |   / ___/ _ \|  \/  | ____|
 \ \ /\ / /|  _| | |  | |  | | | | |\/| |  _|  
  \ V  V / | |___| |__| |__| |_| | |  | | |___ 
   \_/\_/  |_____|_____\____\___/|_|  |_|_____|
The voting system is written in python
you can use this voting system to elect 
the best food in the Southern District canteen

written by panjiansen & ouyangxiaohui

******************************************************
This work is licensed under the Creative Commons 
Attribution 4.0 International License. 
To view a copy of this license
visit http://creativecommons.org/licenses/by/4.0/.
******************************************************

if you want to quit , just ENTER "quit"

ok,please Enter your Student Number:
''' 
logo = '''
__        _______ _     ____ ___  __  __ _____ 
\ \      / / ____| |   / ___/ _ \|  \/  | ____|
 \ \ /\ / /|  _| | |  | |  | | | | |\/| |  _|  
  \ V  V / | |___| |__| |__| |_| | |  | | |___ 
   \_/\_/  |_____|_____\____\___/|_|  |_|_____|
'''
#server welcome 
ip = get_ip_address('eth0')
PORT = 4567
print logo
print 'This is the vote server.'
print 'use:<telnet %s %s>to connect the server' % (ip,PORT)


goodbye = '''

********************************
*   thank you for your voting     
*   here is the result                    
*   ## Enter:'quit' to quit ##                
*   Enter to update the result     
*   have fun  !                              
********************************
'''

class vote(LineReceiver):
	def __init__(self, users):
		self.number = None
		self.users = users
		self.realname = None
		self.state = "get_name"

	def connectionMade(self):
		self.sendLine(welcome) 

	def lineReceived(self, line):
		if line == "quit" :
			self.transport.loseConnection()
		if self.state == "get_name":
			self.handle_GETNAME(line)
		elif self.state == "vote":
			self.handle_vote(line)
		else:
			self.handle_print(line)
	def handle_GETNAME(self, number):
		if number == "quit" :
			self.transport.loseConnection()
		elif self.users.has_key(number):
			self.sendLine("this number is used !")
			return
		elif len(number) == 10:
			self.realname = check_name(number)
			if self.realname == 'unknow_name':
				self.sendLine("hello,but i think you are not in this class.(?)")
				return
			self.sendLine("Hello %s ,please pick a number from 1 to 10  " % (self.realname))
			self.number = number
			self.users[number] = self
			self.state = "vote"
		else :
			self.sendLine("The number should be 10 number ,please try again!")
			return 
	def handle_vote(self, message):
		if message == "quit" :
			self.transport.loseConnection()	
		f = open('vote_result','a')
		try:
			message = int(message)
		except ValueError:
			self.sendLine("please Enter the right number you want to vote")
			return
		if message<=10 and not message == 0:
			write = "%s,%s,%s\n" % (self.realname,self.number,message)
			f.write(write) 
			f.close()
			self.vote = message
			message = "%s<%s>vote:%s" % (self.realname,self.number,self.vote)
			print message
			self.state = "voted"
			self.sendLine("done , you are voted  Enter to see the result .")
		else:
			self.sendLine("please Enter the number from 1 to 10")
			return
	def handle_print(self,message):
		self.sendLine(goodbye)
		print_result(self)
		if message == "quit" :
			self.transport.loseConnection()

class voteFactory(Factory):
	def __init__(self):
		self.users = {} # maps user names to vote instances
	def buildProtocol(self, addr):
		return vote(self.users)

def check_name(check_name):
	namelist = open("list",'rU')
	check_name = int(check_name)
	realname =  'unknow_name'
	for line in namelist:
		number = int(line.split(',')[1])
		if  number == check_name :
			realname =  line.split(',')[2]
	namelist.close()		
	return realname

def addWord(w,wcDict):
	if w in wcDict :
		wcDict[w] += 1
	else :
		wcDict[w] = 1

totalcount = 0
def processLine(wcDict) :
	global totalcount
	vote_result = open("vote_result",'rU')
	for line in vote_result:
		line = line.strip()
		result = line.split(',')[-1]
		addWord(result,wcDict)
		totalcount = totalcount + 1
	vote_result.close

def printlist(wcDict,self) :
	global totalcount
	temp_total = totalcount
	totalcount = 0
	valKeyList=[]
	for key,val in wcDict.items():
		valKeyList.append((val,key))
	valKeyList.sort(reverse = True)
	send_temp = '%-5s| %5s| %5s' % ('Item','Count','Probability')
	self.sendLine (send_temp)
	send_temp = '_'*25
	self.sendLine (send_temp)
	for val,key in valKeyList:
		Probability = val*100/float(temp_total)
		send_temp = ' %-5s %3d %9.2f%%' % (key,val,Probability)
		self.sendLine (send_temp)

def print_result(self):
	totalcount = 0
	wcDict = {}
	processLine(wcDict)
	printlist(wcDict,self)

reactor.listenTCP(PORT, voteFactory())
reactor.run()