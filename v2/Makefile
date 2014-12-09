.PHONY: default hot-dev-server dev-server install embed build server

default:
	@echo "No default"

hot-dev-server:
	npm run hot-dev-server

dev-server:
	npm run dev-server

droplet-server:
	BACKEND=http://pmis.burgercom.co.za FRONTEND=http://insight.burgercom.co.za PORT=8082 npm run dev-server

production-server:
	BACKEND=http://pmis.burgercom.co.za FRONTEND=http://insight.burgercom.co.za PORT=8082 npm run start
	# hot-dev-server

# Assume git, nodejs and npm are installed
install:
	sudo apt-get install build-essential ruby ruby-dev
	sudo gem install bundler
	bundle install
	npm install
	bower install

development-build: install
	bundle exec compass compile
	BACKEND=http://www.backend.dev FRONTEND=http://www.production.dev PORT=8082 npm run build

production-build: install
	bundle exec compass compile
	BACKEND=http://pmis.burgercom.co.za FRONTEND=http://insight.burgercom.co.za PORT=8082 npm run build

deploy:
	ssh pmis "cd /var/www/PMIS; newgrp pmis; git pull; BASE_URL=http://pmis.burgercom.co.za make reindex; cd v2; make production-build; sudo supervisorctl restart all"
