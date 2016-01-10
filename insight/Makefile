.PHONY: default hot-dev-server dev-server install embed build server

default:
	@echo "No default"

hot-dev-server:
	npm run hot-dev-server

dev-server:
	npm run dev-server

production-server:
	BACKEND=http://pmis.burgercom.co.za FRONTEND=http://insight.burgercom.co.za PORT=8082 npm run production-server
	# hot-dev-server

demo-server:
	BACKEND=http://pmis-demo.burgercom.co.za FRONTEND=http://insight-demo.burgercom.co.za PORT=8084 npm run start

# Assume git, nodejs and npm are installed
install:
	# sudo apt-get install build-essential ruby ruby-dev
	# sudo gem install bundler
	bundle install
	npm install
	bower install

development-build:
	BACKEND=http://www.backend.dev FRONTEND=http://www.production.dev PORT=8082 npm run development-build

production-build:
	BACKEND=http://pmis.burgercom.co.za FRONTEND=http://insight.burgercom.co.za PORT=8082 npm run build

demo-build:
	BACKEND=http://pmis-demo.burgercom.co.za FRONTEND=http://insight-demo.burgercom.co.za PORT=8084 npm run build
