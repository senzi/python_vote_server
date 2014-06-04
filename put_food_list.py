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