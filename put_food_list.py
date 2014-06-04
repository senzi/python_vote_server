'''
width = 4
header_format = '%-*s%s(%s)'
format = '%-*s%s(%s)'
print header_format %(width,'No.','Item','Price')
food_list = open("food_list",'rU')
for line in food_list :
	food_number = line.split(',')[0]
	food_name     = line.split(',')[1]
	food_price      = line.split(',')[2]
	print  format % (width,food_number,food_name,food_price)
food_list.close()
'''

def printfood():
	flag = False
	width = 4
	header_format = '%-*s| %s(%s)'
	format = '<%s> %-12s(%s)'
	print header_format %(width,'<No.>','Item','Price')
	print '-*-'*6
	food_list = open("food_list",'r')
	for line in food_list :
		food_number = line.split(',')[0]
		food_name     = line.split(',')[1]
		food_price      = line.split(',')[2]
		if flag :
			print  format % (food_number,food_name,food_price)
		else:
			print  format % (food_number,food_name,food_price),
			print '  |  ',
		flag = not flag
	food_list.close()

def print_food(self):
	width = 4
	header_format = '%-*s| %s(%s)'
	format = '<%s>%s(%s)'
	print header_format %(width,'<No.>','Item','Price')
	print '-*-'*6
	food_list = open("food_list",'r')
	for line in food_list :
		food_number = line.split(',')[0]
		food_name     = line.split(',')[1]
		food_price      = line.split(',')[2]
		temp_sendLine =  format % (food_number,food_name,food_price)
		self.sendLine(temp_sendLine)
	food_list.close()

def findfood(n):
	temp = None
	food_list = open("food_list",'rU')
	for line in food_list :
		food_number = int(line.split(',')[3])
		food_name     = line.split(',')[1]
		if food_number == n :
			temp =  food_name
	return temp		
	food_list.close()

printfood()
		