# karlooper([中文文档点击此处](https://github.com/karldoenitz/karlooper/blob/master/%E4%BD%BF%E7%94%A8%E5%89%8D%E9%98%85%E8%AF%BB.md))
![karlooper logo](https://github.com/karldoenitz/karlooper/blob/master/documentations/images/logo.jpg "this is karlooper logo")  
a python web micro-framework, single thread, asyncio

# News
The framework support Python 3!

# Install
depend: jinja2.8  
python version: >=2.6.6  
download the package or check out the project  
then cd to the project folder  
run these commands:  

    sudo python setup.py install  

or use ```pip```:

    pip install karlooper

# Demo
## hello world
```python
# -*-coding:utf-8-*-

from karlooper.web.application import Application
from karlooper.web.request import Request

__author__ = 'karlvorndoenitz@gmail.com'


class HelloHandler(Request):
    def get(self):
        return self.http_response("Hello,World!")

handlers = {
    "/hello": HelloHandler
}

if __name__ == '__main__':
    application = Application(handlers, port=8000)
    application.run()

```
### run _hello world_
    python index.py
then open the web browser and go to "http://127.0.0.1:8000/hello", you will see ```hello world```.

# Compare performance with Tornado
OS: Ubuntu 14.04 LTS  
CPU: Intel core i5 2.5GHz  
Memory: 10G DDR3 1600GHz  
## tornado
```
karl@karl-Inspiron-N4050:~$ ab -n 10000 -c 50 http://localhost:9999/hello
This is ApacheBench, Version 2.3 <$Revision: 1706008 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 1000 requests
Completed 2000 requests
Completed 3000 requests
Completed 4000 requests
Completed 5000 requests
Completed 6000 requests
Completed 7000 requests
Completed 8000 requests
Completed 9000 requests
Completed 10000 requests
Finished 10000 requests


Server Software:        TornadoServer/4.4.2
Server Hostname:        localhost
Server Port:            9999

Document Path:          /hello
Document Length:        12 bytes

Concurrency Level:      50
Time taken for tests:   7.041 seconds
Complete requests:      10000
Failed requests:        0
Total transferred:      2070000 bytes
HTML transferred:       120000 bytes
Requests per second:    1420.32 [#/sec] (mean)
Time per request:       35.203 [ms] (mean)
Time per request:       0.704 [ms] (mean, across all concurrent requests)
Transfer rate:          287.12 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       3
Processing:     2   35  10.7     28     198
Waiting:        2   35  10.7     28     198
Total:          4   35  10.7     28     200

Percentage of the requests served within a certain time (ms)
  50%     28
  66%     46
  75%     47
  80%     47
  90%     48
  95%     49
  98%     51
  99%     52
 100%    200 (longest request)
```
## karlooper
```
karl@karl-Inspiron-N4050:~$ ab -n 10000 -c 50 http://localhost:8080/hello-world
This is ApacheBench, Version 2.3 <$Revision: 1706008 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 1000 requests
Completed 2000 requests
Completed 3000 requests
Completed 4000 requests
Completed 5000 requests
Completed 6000 requests
Completed 7000 requests
Completed 8000 requests
Completed 9000 requests
Completed 10000 requests
Finished 10000 requests


Server Software:
Server Hostname:        localhost
Server Port:            8080

Document Path:          /hello-world
Document Length:        20 bytes

Concurrency Level:      50
Time taken for tests:   1.204 seconds
Complete requests:      10000
Failed requests:        0
Total transferred:      1360000 bytes
HTML transferred:       200000 bytes
Requests per second:    8307.10 [#/sec] (mean)
Time per request:       6.019 [ms] (mean)
Time per request:       0.120 [ms] (mean, across all concurrent requests)
Transfer rate:          1103.29 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.2      0       4
Processing:     1    6   1.3      6      16
Waiting:        1    6   1.2      6      16
Total:          5    6   1.3      6      16

Percentage of the requests served within a certain time (ms)
  50%      6
  66%      6
  75%      6
  80%      6
  90%      6
  95%      8
  98%     12
  99%     13
 100%     16 (longest request)
```

# Documentation
[click here](https://github.com/karldoenitz/karlooper/blob/master/documentations/document.md)

# Diagram
![karlooper diagram](https://github.com/karldoenitz/karlooper/blob/master/documentations/images/karlooper_architecture_diagram.png "this is karlooper diagram")

# Notice
This framework has been used on the linux version of [CubeBackup for Google Apps](http://www.cubebackup.com), which is a local backup solution for Google Apps data.   
If you find bugs or know how to fix them,  please send a message to karlvorndoenitz@gmail.com, special thanks.   
