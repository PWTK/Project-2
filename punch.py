import sys
from tornado.curl_httpclient import CurlAsyncHTTPClient
from tornado.ioloop import IOLoop
import collections
import time


class benchmark():
    def __init__(self, conc, ioloop, req): #client initialization
        self.concurrent = conc
        self.counter = collections.Counter()
        self.client = CurlAsyncHTTPClient(max_clients=self.concurrent,
                                          defaults=dict(request_timeout=float(20), P2Tag="u5680975_u5880036"))
        self.ioloop = ioloop
        self.loopstop = req
        self.avgtime = []
        self.req =req

    def fetch(self, url):   #sending request
        self.client.fetch(url, callback=self.handle_response)
        # print response.code

    def handle_response(self, response):  #do many things with response
        # print response.code
        self.loopstop -= 1
        self.avgtime.append(response.request_time)
        if response.code == 200:
            self.counter.update({str(200): 1}) #pushing 200 request ok into counter
        if self.loopstop == 0:  #breaking the loop
            self.avgtime.sort()
            self.ioloop.instance().stop() #printing the result
            print "Completed Request: " + str(self.counter["200"])
            print "Failed Request: " + str(self.counter["200"]-self.req)
            print "Total Request: " + str(self.req)
            print "Percentage of the requests served within a certain time (ms)"
            print "50%       " + str(self.avgtime[int(len(self.avgtime)/2.0)]*10**3)
            print "60%       " + str(self.avgtime[int(len(self.avgtime)/1.66)]*10**3)
            print "70%       " + str(self.avgtime[int(len(self.avgtime)/1.428)]*10**3)
            print "80%       " + str(self.avgtime[int(len(self.avgtime)/1.25)]*10**3)
            print "90%       " + str(self.avgtime[int(len(self.avgtime)/1.11)]*10**3)
            print "100%      " + str(self.avgtime[-1])

def start(input): #starting point
    ioloop = IOLoop.instance()#loop starting
    ioloop.add_callback(loop, *input)
    ioloop.start()


def loop(*input):                #loop components
    nummconn = int(input[1])
    nummreq = int(input[0])
    url = input[-1]
    bm = benchmark(nummconn, IOLoop.instance(), nummreq)
    for i in xrange(nummreq): #DDoS
        bm.fetch(url)


if __name__ == '__main__': #input
    a = sys.argv
    x = []
    x.append(a[2])
    x.append(a[4])
    x.append(a[5])
    start_time = time.time() #start stop measurement
    start(x)
    elapsed_time = time.time() - start_time
    print('Time taken for the test %f seconds' % (elapsed_time))
    print('Average request per second {} [req/s]').format(elapsed_time/int(a[2]))

