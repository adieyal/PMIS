.PHONY: default hot-dev-server dev-server install embed build server

default:
	@echo "No default"

hot-dev-server:
	npm run hot-dev-server

dev-server:
	npm run dev-server

production-server:
	BUILD_FOLDER=build/production BACKEND=http://pmis.burgercom.co.za FRONTEND=http://insight.burgercom.co.za PORT=8082 npm run start
	# hot-dev-server

demo-server:
	BUILD_FOLDER=build/demo BACKEND=http://pmis-demo.burgercom.co.za FRONTEND=http://insight-demo.burgercom.co.za PORT=8084 npm run start

# Assume git, nodejs and npm are installed
install:
	# sudo apt-get install build-essential ruby ruby-dev
	# sudo gem install bundler
	bundle install
	npm install
	bower install

development-build: install
	bundle exec compass compile
	BUILD_FOLDER=build/development BACKEND=http://www.backend.dev FRONTEND=http://www.production.dev PORT=8082 npm run build

production-build: install
	bundle exec compass compile
	BUILD_FOLDER=build/production BACKEND=http://pmis.burgercom.co.za FRONTEND=http://insight.burgercom.co.za PORT=8082 npm run build

demo-build: install
	bundle exec compass compile
	BUILD_FOLDER=build/demo BACKEND=http://pmis-demo.burgercom.co.za FRONTEND=http://insight-demo.burgercom.co.za PORT=8084 npm run build

deploy:
	ssh -t pmis "cd /var/www/pmis && git pull && PATH=~/.virtualenvs/pmis/bin:/usr/bin:/bin make production-reindex && sudo /etc/init.d/elasticsearch stop && cd v2 && PATH=~/.rbenv/shims:/opt/node/bin:/usr/bin:/bin make production-build && sudo chgrp -R webapp . && sudo /etc/init.d/elasticsearch start && sudo supervisorctl restart all"
