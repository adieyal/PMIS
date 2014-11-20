.PHONY: default install embed build

default:
	@echo "No default"

dev-server:
	npm run dev-server

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
