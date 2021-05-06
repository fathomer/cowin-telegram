from fake_useragent import UserAgent

ua = UserAgent()
header = {'User-Agent': str(ua.random)} 

def setHeader():
    global header
    global ua
    header = {'User-Agent': str(ua.random)} 

previous_sessions = []
count = 0
