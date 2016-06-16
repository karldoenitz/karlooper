# karlooper.web
_**karlooper.web**_ provides a simple web framework with asynchronous features.
## karlooper.web.request
This model provides a class named Request.  
```python
class Request(http_data_dict, http_message, settings)
```
Base class for HTTP request handlers.
Subclasses must define at least one of the methods defined in the “Entry points” section below.  
### Entry points
```python
def get()
```
http get method
```python
def post()
```
http post method
```python
def put()
```
http put method
```python
def head()
```
http head method
```python
def options()
```
http options method
```python
def delete()
```
http delete method
```python
def trace()
```
http trace method
```python
def connect()
```
http connect method
### Cookies
```python
def get_cookie(key, default=None)
```
Gets the value of the cookie with the given name, else default.
```python
def set_cookie(key, value, expires_days=1, path="/")
```
Sets the given cookie name/value with the given options.
```python
def get_security_cookie(key, default=None)
```
Gets the value of the cookie with the given name, else default.
The value of the cookie is decoded.
```python
def set_security_cookie(key, value, expires_days=1, path="/")
```
Sets the given cookie name/value with the given options.
The value of the cookie is encoded.
### Input
### Output
## karlooper.web.application
This model provides a class named Application.  
# karlooper.template
_**karlooper.template**_ provides a simple template system that compiles templates to Python code.
This template system based on jinja2.
# karlooper.escape
# karlooper.utils
# karlooper.logger
