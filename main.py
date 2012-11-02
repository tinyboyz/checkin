'''
program main entrance.

@author: leon,zhang(itasoro@gmail.com)
'''
from qqbuycredits import Credits 
from time import sleep

def main():
    credits = Credits()
    while True:
        credits.sign()
        sleep(60)
    
    
if __name__ == '__main__':
    main()