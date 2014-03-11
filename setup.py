import Qingblog
from email.utils import parseaddr
from setuptools import setup

author, author_email = parseaddr(Qingblog.__author__)


setup(
    name='Qingblog',
    version=Qingblog.__version__,
    author=author,
    author_email=author_email,
    # url='https://github.com/pythoncn/june',
    packages=['Qingblog'],
    license=open('License').read()
)
