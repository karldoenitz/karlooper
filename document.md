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
For example:
```python
handlers = {
    "/hello": HelloHandler
}
application = Application(handlers, port=8080)
application.run()
```
If not define the port in anywhere, the server will run on the port 80.
**arguments in init method**  
  `handlers`: A dict contains urls and handlers mapping.  
  `kwargs`: Other arguments, for example: _port_.  
  `settings`: A dict contains some settings.  
  - `template`: config the template files directory.  
  - `cookie`:  config the security cookie's security key.  

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
_**Methods**_:
```python
def render(template_path, **kwargs)
```
Renders the template with the given arguments as the response.  
```python
def render_string(template_string, **kwargs)
```
Renders the template string data with the given arguments as the response.  
# karlooper.escape
_**karlooper.escape**_ provides some escaping/unescaping methods for HTML, URLs, and others.
## Escaping functions
```python
def xhtml_escape(value)
```
Escapes a string so it is valid within HTML or XML.  
Escapes the characters <, >, ", ', and &. When used in attribute values the escaped strings must be enclosed in quotes.
```python
def xhtml_unescape(value)
```
Un-escapes an XML-escaped string.
```python
def url_escape(value, plus=True)
```
Returns a URL-encoded version of the given value.  
If plus is true (the default), spaces will be represented as “+” instead of “%20”.   
This is appropriate for query strings but not for the path component of a URL.  
Note that this default is the reverse of Python’s urllib module.
```python
def url_unescape(value, plus=True)
```
Decodes the given value from a URL.  
The argument may be either a byte or unicode string.  
If encoding is None, the result will be a byte string.  
Otherwise, the result is a unicode string in the specified encoding.  
If plus is true (the default), plus signs will be interpreted as spaces (literal plus signs must be represented as “%2B”).  
This is appropriate for query strings and form-encoded values but not for the path component of a URL.  
Note that this default is the reverse of Python’s urllib module.
## Byte/unicode conversions
```python
def to_unicode(value)
```
Converts a string argument to a unicode string.  
If the argument is already a unicode string or None, it is returned unchanged.  
Otherwise it must be a byte string and is decoded as utf8.
```python
def to_basestring(value)
```
Converts a byte or unicode string into type str.
```python
def utf8(value)
```
Converts a string argument to a byte string.  
If the argument is already a byte string or None, it is returned unchanged.  
Otherwise it must be a unicode string and is encoded as utf8.
# karlooper.utils
_**karlooper.utils**_ provides `security` and `parse_command_line` models.
# karlooper.logger
_**karlooper.logger**_ provides a model to write the log to file.