#!flask/bin/python
from app import app
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t','--test', action='store_true', help='test help')
args = parser.parse_args()

server_port = 5000

if(args.test == True):
	app.config['TESTING'] = True
	server_port = 5001
	print " * Running with test configuration"


app.run(host='0.0.0.0', port=server_port)
