default:
	@echo "No default"

install:
	bundle install
	rbenv rehash
	npm install

embed:
	npm run build
	mkdir -p ../server/project/apps/v2/static/v2
	cp -a config/dev-server-public/* ../server/project/apps/v2/static/v2
	cp -a build/public/* ../server/project/apps/v2/static/v2
