import urllib2

class Imp():

  @staticmethod
  def get_state():
    urllib2.urlopen("https://agent.electricimp.com/j9D9R5FQYOBy")

  @staticmethod  
  def send_state(state):
    # urllib2.urlopen("https://agent.electricimp.com/DISiQRNUIly9?stopped=" + state).read()
    urllib2.urlopen("https://agent.electricimp.com/j9D9R5FQYOBy?stopped=" + state).read()