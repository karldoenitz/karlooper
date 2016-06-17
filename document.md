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
HTTP get method
```python
def post()
```
HTTP post method
```python
def put()
```
HTTP put method
```python
def head()
```
HTTP head method
```python
def options()
```
HTTP options method
```python
def delete()
```
HTTP delete method
```python
def trace()
```
HTTP trace method
```python
def connect()
```
HTTP connect method
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
```python
def get_parameter(key, default=None)
```
Get the value of the argument with the given name.  
If key does not exist, return default.  
This method return the value in HTTP body or url.  
```python
def decode_parameter(key, default=None)
```
Get the value of the argument with the given name.  
If the given name does not exist, return default.  
This method return the value in HTTP body or url.  
The value must be urlencoded.  
```python
def get_http_request_message()
```
Get the http request message.  
### Output
```python
def set_header(self, header_dict)
```
Sets the given response header name and value.  
For example:
```python
self.set_header({
    "Content-Type": "application/json",
    "Content-Length": "65"
})
```
The key in _**header_dict**_ is the HTTP header name.  
The value in _**header_dict**_ is the HTTP header value.  
```python
def clear_header(self, header_dict)
```
Clears an outgoing header, undoing a previous set_header call.
```python
def response_as_json(data)
```
Return json data.
```python
def render(template_path, **kwargs)
```
Renders the template with the given arguments as the response.
## karlooper.web.application
This model provides a class named Application.  
```python
class Application(handlers, settings=None, **kwargs)
```
A collection of request handlers that make up a web application.  
Instances of this class are callable and can be passed directly to HTTPServer to serve the application.  
**arguments in init method**  
  `handlers`: A dict contains urls and handlers mapping.  
  `settings`: A dict contains some settings.  
  `kwargs`: Other arguments, for example: _port_.  
**methods**
```python
def listen(port)
```
Starts an HTTP server for this application on the given port.  
```python
def run()
```
Run the web server.  
# karlooper.template
_**karlooper.template**_ provides a simple template system that compiles templates to Python code.
This template system based on jinja2.
# karlooper.escape
# karlooper.utils
# karlooper.logger
