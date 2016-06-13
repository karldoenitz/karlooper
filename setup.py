from distutils.core import setup

setup(
    name='karlooper',
    version='0.1.5',
    packages=[
        'karlooper',
        'karlooper.autoreload',
        'karlooper.config',
        'karlooper.escape',
        'karlooper.http_parser',
        'karlooper.router',
        'karlooper.template',
        'karlooper.utils',
        'karlooper.web'
    ],
    url='https://github.com/karldoenitz/karlooper',
    license='',
    author='lizhihao',
    author_email='karlvorndoenitz@gmail.com',
    description='karloop plus frame work'
)
