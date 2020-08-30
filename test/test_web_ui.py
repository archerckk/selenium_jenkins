from selenium import webdriver
import os
import  configparser
import sys

def get_config():
    config=configparser.ConfigParser()
    if sys.platform=='win32':
        os.environ['HOMEPATH']='C:/test'
        config.read(os.path.join(os.environ['HOMEPATH'],'selenium.ini'))
    else:
        config.read(os.path.join(os.environ['HOME'],'selenium.ini'))
    print(config)
    return config
class TestWeb:



    def setup(self):
        pass