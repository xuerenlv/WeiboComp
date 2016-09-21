#coding:utf-8


import traceback
try:
    import logging
except ImportError:
    s = traceback.format_exc()
    print s

class WeiboSearchLog:  
      
    def __init__(self):
        pass
    
    def get_scheduler_logger(self):
        return logging.getLogger("schedulerLog")
    
    def get_proxy_logger(self):
        return logging.getLogger("proxyLog")
    

if __name__ == "__main__":
    print "xhj"
    pass