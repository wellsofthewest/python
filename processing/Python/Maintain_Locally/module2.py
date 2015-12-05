analysts = [{'Name':'Christian Wells','Skillsets':{'Edit':True, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':True}},
{'Name':'Enabell Diaz','Skillsets':{'Edit':False, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':False}},
{'Name':'Brian Beegle','Skillsets':{'Edit':True, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':False}},
{'Name':'George Thompson','Skillsets':{'Edit':True, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':True}},
{'Name':'Pat Roberts','Skillsets':{'Edit':True, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':False}},
{'Name':'Glenn Burton','Skillsets':{'Edit':True, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':False}},
{'Name':'Quinn Francis','Skillsets':{'Edit':False, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':False}},
{'Name':'Tina Morgan','Skillsets':{'Edit':True, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':True}},
{'Name':'Christopher Thomas','Skillsets':{'Edit':True, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':True}},
{'Name':'Julia Lenhart','Skillsets':{'Edit':False, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':False}},
{'Name':'Qing Shi','Skillsets':{'Edit':False, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':False}},
{'Name':'Katie Cullen','Skillsets':{'Edit':False, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':False}},
{'Name':'Liting Cui','Skillsets':{'Edit':True, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':False}},
{'Name':'Matthew Ziebarth','Skillsets':{'Edit':True, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':True}},
{'Name':'Melanie Whalen','Skillsets':{'Edit':True, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':True}},
{'Name':'Steven Embree','Skillsets':{'Edit':True, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':True}},
{'Name':'Biraja Nayak','Skillsets':{'Edit':True, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':True}},
{'Name':'Jay Strahan','Skillsets':{'Edit':True, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':False}},
{'Name':'Liz Parrish','Skillsets':{'Edit':True, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':True}},
{'Name':'Sam Tompsett','Skillsets':{'Edit':True, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':False}},
{'Name':'Aarthi Dwarakanath','Skillsets':{'Edit':True, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':True}},
{'Name':'Harshini Pande','Skillsets':{'Edit':True, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':True}},
{'Name':'Ken Galliher','Skillsets':{'Edit':True, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':True}},
{'Name':'Jing Li','Skillsets':{'Edit':True, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':False}},
{'Name':'Simpy Verma','Skillsets':{'Edit':True, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':False}},
{'Name':'Justin Muise','Skillsets':{'Edit':True, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':False}}]


for analyst in analysts:
    print analyst['Name']
    for key, value in analyst['Skillsets'].iteritems():
        print "\t" + key, value