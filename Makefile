myIp := $(shell curl https://ipinfo.io/ip)

.PHONY: say_hi

help:
	@echo "This is short guide."
	@echo "Clone ngfg.project in same folder as ngfg"
	@echo "type 'make install' to install docker and clone client repository "
	@echo "type 'make const' to replace local constants by your machine data"
	@echo "after all finished, start project by entering 'sudo docker-compose up' twice (first time to build docker images, second time to run project)"

getMyIp:
	@echo $(myIp)
say_hi:
	@echo Hi

install:
	@echo installing all dependencies...
	sudo apt install docker.io;
	sudo curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
	sudo chmod +x /usr/local/bin/docker-compose
	echo "Finished, you can run 'make const' now"

const:
	@echo changing constants....
	cd ../;
	if [! -f src/app/ngfg-сredentials.json ]; then @echo 'make const' is not executed, pls get your Google API credentials and put them into ngfg/src/app/ngfg-сredentials.json; fi
	if [ -f src/app/ngfg-сredentials.json ]; then cd src/app; sed -i 's/localhost/$(myIp)/g' helper/constants.py ; sed -i "s/'ngfg.com:8000'/None/g" config.py; cd ../../; fi
	if [ -f src/app/ngfg-сredentials.json ]; then sed -i "s/Redis(password=REDIS_PASSWORD)/Redis(host='redis', password=REDIS_PASSWORD)/g" src/app/__init__.py; sed -i 's/gevent==1.4.0/gevent==1.5a2/g' requirements.txt; fi
	if [ -f src/app/ngfg-сredentials.json ]; then cd ../ngfg.client/ngfg.client/src/constants/; sed -i 's/ngfg.com/$(myIp)/g' index.js; sed -i 's/localhost/$(myIp).xip.io/g' index.js; fi
	@echo constans changed.
