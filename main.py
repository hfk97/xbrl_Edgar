import subprocess
import sys
import importlib



# function that imports a library if it is installed, else installs it and then imports it
def getpack(package):
    try:
        return (importlib.import_module(package))
        # import package
    except ImportError:
        subprocess.call([sys.executable, "-m", "pip", "install", package])
        return (importlib.import_module(package))
        # import package



bs4=getpack("bs4")
from bs4 import BeautifulSoup
urllib=getpack("urllib")
request=getpack("urllib.request")
re=getpack("re")
from urllib.request import Request


def make_soup(url):
    page = open(url)
    soup = BeautifulSoup(page.read(), 'html.parser')
    return soup


soup=make_soup("/Users/Felix/Desktop/table.html")

soup.findAll('p')



