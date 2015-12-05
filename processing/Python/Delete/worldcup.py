print " World cup party invite. Do you like soccer yes or no?"
	
soccer = raw_input (">")
	
if soccer == "yes":
	print "Is oliver also invited?"
	print "1. of course he is."
	print "2. no dogs allowed."
	
	dog = raw_input (">")
	
	if dog == "1":
		print " We shall be attending the party."
	elif dog == "2" :
		print "We deline the invitation."
	else:
		print "Let'd bring him anyway."

elif soccer == "no":
	print "Will you absence offend anyone?"
	print "1. Yes"
	print "2. No"
	print "3. Maybe"
	
	absence = raw_input (">")
	
	if absence == "1" or absence == "3":
		print "We should go for a little bit." 
	else:
		print " lets snuggle and watch netflix instead."
	
else:
	print " no one likes soccer, It's america." 