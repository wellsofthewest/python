import string
import random

def getPass(length=12, char=string.ascii_uppercase+string.digits+string.ascii_lowercase+string.punctuation):
  return ''.join(random.choice(char) for x in range(length))    
