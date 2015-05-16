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
	BUILD_FOLDER=build/development BACKEND=http://www.backend.dev FRONTEND=http://www.production.dev PORT=8082 npm run development-build

production-build: install
	bundle exec compass compile
	BUILD_FOLDER=build/production BACKEND=http://pmis.burgercom.co.za FRONTEND=http://insight.burgercom.co.za PORT=8082 npm run build

demo-build: install
	bundle exec compass compile
	BUILD_FOLDER=build/demo BACKEND=http://pmis-demo.burgercom.co.za FRONTEND=http://insight-demo.burgercom.co.za PORT=8084 npm run build

deploy:
	ssh -t pmis " \
	export PATH=~/.virtualenvs/pmis/bin:~/.rbenv/shims:/opt/node/bin:/usr/local/bin:/usr/bin:/bin; \
	cd /var/www/pmis && \
	git pull && \
	cd server && \
	npm install && \
	gulp && \
	SECRET_KEY='34234v*eh#_gq618si+0gucd!fpkr2n07gxuy4m$mg_ss&_0h-ktm1fgdf' BASE_URL=http://pmis.burgercom.co.za python manage.py collectstatic && \
	cd ../insight && \
	make production-build demo-build && \
	sudo chgrp -R webapp . && \
	sudo supervisorctl restart all"
