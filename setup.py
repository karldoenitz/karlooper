from distutils.core import setup

setup(
    name='karlooper',
    version='0.1.1',
    packages=[
        'karlooper',
        'karlooper.utils',
        'karlooper.config',
        'karlooper.router',
        'karlooper.server',
        'karlooper.http_parser'
    ],
    url='https://github.com/karldoenitz/karlooper',
    license='',
    author='lizhihao',
    author_email='karlvorndoenitz@gmail.com',
    description='karloop plus frame work'
)
