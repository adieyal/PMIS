serve:
	invoker start invoker.ini

production-reindex:
	cd server && BASE_URL=http://pmis.burgercom.co.za python manage.py seed_indices

development-reindex:
	cd server && BASE_URL=http://www.backend.dev python manage.py seed_indices

clean-server:
	cd server && find . -name '*.pyc' -delete

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

local-build-and-deploy:
	# cd insight && make production-build demo-build
	rsync -avz --delete insight/build/ pmis:/var/www/pmis/build
	ssh -t pmis " \
	export PATH=~/.virtualenvs/pmis/bin:~/.rbenv/shims:/opt/node/bin:/usr/local/bin:/usr/bin:/bin; \
	cd /var/www/pmis && \
	git pull && \
	cd server && \
	npm install && \
	gulp && \
	SECRET_KEY='34234v*eh#_gq618si+0gucd!fpkr2n07gxuy4m$mg_ss&_0h-ktm1fgdf' BASE_URL=http://pmis.burgercom.co.za python manage.py collectstatic && \
	cd ../insight && \
	sudo chgrp -R webapp . && \
	sudo supervisorctl restart all"

.PHONY: serve production-reindex development-reindex deploy
