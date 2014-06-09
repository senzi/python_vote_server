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
shark = '''            __                              
     o                 /' )                             
                     /'   (                          ,  
                 __/'     )                        .' `;
  o      _.-~~~~'          ``---..__             .'   ; 
    _.--'  b)                       ``--...____.'   .'  
   (     _.      )).      `-._                     <    
    `\|\|\|\|)-.....___.-     `-.         __...--'-.'.  
      `---......____...---`.___.'----... .'         `.; 
                                       `-`           `  
'''
welcome ='''
__        _______ _     ____ ___  __  __ _____ 
\ \      / / ____| |   / ___/ _ \|  \/  | ____|
 \ \ /\ / /|  _| | |  | |  | | | | |\/| |  _|  
  \ V  V / | |___| |__| |__| |_| | |  | | |___ 
   \_/\_/  |_____|_____\____\___/|_|  |_|_____|
This voting system is written in python
It can be voted to select the most popular food 
in the Southern District Canteen
                     [written by]:
           panjiansen&ouyangxiaohui
******************************************************
This work is licensed under the Creative Commons 
Attribution 4.0 International License. 
To view a copy of this license
visit http://creativecommons.org/licenses/by/4.0/.
******************************************************
if you want to exit , please input "quit"
ok,please input your student number:
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
print 'This is the server of the voting system.'
print 'input:<telnet %s %s>connect to system' % (ip,PORT)


goodbye = '''

********************************
*   thank you for your voting     
*   here is the result                    
*   Input:'quit' to quit               
*   Hit 'Enter' to update the result     
*   have fun  !                              
********************************
@In case of cheating, a user only has one chance to log in and to vote,
@the voting result will not be visible when you log out.
'''

class vote(LineReceiver):
	def __init__(self, users):
		self.number = None
		self.users = users
		self.realname = None
		self.state = "get_name"
		self.food = None

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
			self.sendLine("This number is existed, please input again!")
			return
		elif len(number) == 10:
			try:
				temp = int(number)
			except ValueError:
				self.sendLine("please do not input nonnumeric character")
				return
			self.realname = check_name(number)
			if self.realname == 'unknow_name':
				self.sendLine("Hello, but I think you are not in this class.(?)")
				return
			self.sendLine(shark)
			print_food(self)
			self.sendLine("\nHello %s, please pick a number from 1 to 18." % (self.realname))
			self.number = number
			self.users[number] = self
			self.state = "vote"
		else :
			self.sendLine("The student number should be 10 digits, please try again!")
			return 
	def handle_vote(self, message):
		if message == "quit" :
			self.transport.loseConnection()	
		f = open('vote_result.data','a')
		try:
			message = int(message)
		except ValueError:
			self.sendLine("Please input the right number you want to vote, please do not input nonnumeric character.")
			return
		self.food = findfood(`message`)
		if message<=18 and not message == 0:
			write = "%s,%s,%s\n" % (self.realname,self.number,message)
			f.write(write) 
			f.close()
			self.vote = message
			message = "%s<%s>vote:%s" % (self.realname,self.number,self.food)
			print message
			self.state = "voted"
			self.sendLine("Thank you, your vote has been recorded. Hit 'Enter' to see the result .")
		else:
			self.sendLine("There are only 18 options, please Enter the number from 1 to 18.")
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
	namelist = open("list.data",'rU')
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
	vote_result = open("vote_result.data",'rU')
	for line in vote_result:
		line = line.strip()
		result = line.split(',')[-1]
		addWord(result,wcDict)
		totalcount = totalcount + 1
	vote_result.close

def printlist(wcDict,self) :
	food_name = None
	global totalcount
	temp_total = totalcount
	totalcount = 0
	valKeyList=[]
	for key,val in wcDict.items():
		valKeyList.append((val,key))
	valKeyList.sort(reverse = True)
	send_temp = '  %-6s    |%5s|%5s' % ('name','count','  %  ')
	self.sendLine (send_temp)
	send_temp = '_'*25
	self.sendLine (send_temp)
	for val,key in valKeyList:
		food_name = findfood(key)
		Probability = val*100/float(temp_total)
		send_temp = '  %-12s|  %-4d|%5.2f%%|' % (food_name,val,Probability)
		self.sendLine (send_temp)

def print_result(self):
	totalcount = 0
	wcDict = {}
	processLine(wcDict)
	printlist(wcDict,self)

def print_food(self):
	width = 4
	flag = False
	format = '<%s> %-12s(%s)'
	food_list = open("food_list.data",'r')
	for line in food_list :
		food_number = line.split(',')[0]
		food_name     = line.split(',')[1]
		food_price      = line.split(',')[2]
		if flag :
			send_temp = send_temp + format % (food_number,food_name,food_price)
			self.sendLine(send_temp)
		else:
			send_temp = format % (food_number,food_name,food_price) + '  |  '
		flag = not flag
	food_list.close()

def findfood(n):
	temp = None
	food_list = open("food_list.data",'rU')
	for line in food_list :
		food_number = line.split(',')[3]
		food_name     = line.split(',')[1]
		if food_number == n :
			temp =  food_name
	return temp		
	food_list.close()

reactor.listenTCP(PORT, voteFactory())
reactor.run()