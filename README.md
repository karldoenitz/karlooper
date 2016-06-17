# karlooper
a python web framework, single thread, asyncio

# install
depend: jinja2.8  
python version: >=2.6.6 and < 3.0  
download the package or check out the project  
then cd to the project folder  
run these commands:  

    sudo python setup.py install  

# demo
## hello world
```python
# -*-coding:utf-8-*-

from karlooper.web.application import Application
from karlooper.web.request import Request

__author__ = 'karlvorndoenitz@gmail.com'


class HelloHandler(Request):
    def get(self):
        return "Hello,World!"

handlers = {
    "/hello": HelloHandler,
}

if __name__ == '__main__':
    application = Application(handlers, port=8000)
    application.run()

```
### run hello world
    python index.py
then open the web browser and go to "127.0.0.1:8000/hello", you will see the hello world.

# Documentation
[click here](https://github.com/karldoenitz/karlooper/blob/master/documentations/document.md)

# Notice
This framework has been used on the linux version of [CubeBackup for Google Apps](http://www.cubebackup.com), which is a local backup solution for Google Apps data.   
If you find bugs or know how to fix them,  please send a message to karlvorndoenitz@gmail.com, special thanks.   
