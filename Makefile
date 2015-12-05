install:
	sudo apt-get install python-pip python-dev build-essential
	sudo pip install requests
	sudo pip install urllib3
	
yowsup-install:
	sudo python setup.py install

run:
	yowsup-cli demos --config yowsup-cli.config -y
