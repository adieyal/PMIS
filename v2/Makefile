.PHONY: default hot-dev-server dev-server install embed build server

default:
	@echo "No default"

hot-dev-server:
	npm run hot-dev-server

dev-server:
	npm run dev-server

server: build
	BACKEND=http://pmis.burgercom.co.za FRONTEND=http://insight.burgercom.co.za PORT=8082 npm run dev-server

install:
	bundle install
	rbenv rehash
	npm install

embed:
	npm run build
	mkdir -p ../server/project/apps/v2/static/v2
	cp -a config/dev-server-public/* ../server/project/apps/v2/static/v2
	cp -a build/public/* ../server/project/apps/v2/static/v2

build:
	bundle exec compass compile
