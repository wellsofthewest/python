analysts = "Matthew Ziebarth, Melanie Whalen, Steven Embree, Biraja Nayak, Jay Strahan, Liz Parrish, Sam Tompsett, Aarthi Dwarakanath, Harshini Pande, Ken Galliher, Jing Li, Simpy Verma, Justin Muise"
list = analysts.split(", ")

list.sort()


testDic = {'Name':'Matthew Ziebarth','Skillsets':{'Edit':True, 'Client':True, 'Admin':True, 'General':True, 'ProdTools':True}}



for key, value in testDic.iteritems():
    if key == 'Name':
        print key
    if key == 'Skillsets':
        for skill, bool in value.iteritems():
            print skill, bool






