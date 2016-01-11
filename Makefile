serve:
	invoker start invoker.ini

production-reindex:
	cd server && BASE_URL=http://pmis.burgercom.co.za python manage.py seed_indices

development-reindex:
	cd server && BASE_URL=http://www.backend.dev python manage.py seed_indices

clean-server:
	cd server && find . -name '*.pyc' -delete

deploy-demo:
	ssh -t pmis " \
	export PATH=~/.virtualenvs/pmis/bin:~/.rbenv/shims:/opt/node/bin:/usr/local/bin:/usr/bin:/bin; \
	cd /var/www/demo && \
	git pull && \
	cd server && \
	npm install && \
	bower install && \
	cd static/bower_components/bootstrap-datepicker && npm install && grunt dist && cd ../../.. \
	gulp && \
	SECRET_KEY='34234v*eh#_gq618si+0gucd!fpkr2n07gxuy4m$mg_ss&_0h-ktm1fgdf' BASE_URL=http://pmis-demo.burgercom.co.za python manage.py collectstatic --noinput && \
	cd ../insight && \
	make demo-build && \
	sudo chgrp -R webapp . && \
	sudo /etc/init.d/nginx restart \
	sudo supervisorctl restart demo"

deploy-production:
	ssh -t pmis " \
	export PATH=~/.virtualenvs/pmis/bin:~/.rbenv/shims:/opt/node/bin:/usr/local/bin:/usr/bin:/bin; \
	cd /var/www/production && \
	git pull && \
	cd server && \
	npm install && \
	bower install && \
	cd static/bower_components/bootstrap-datepicker && npm install && grunt dist && cd ../../.. \
	gulp && \
	SECRET_KEY='34234v*eh#_gq618si+0gucd!fpkr2n07gxuy4m$mg_ss&_0h-ktm1fgdf' BASE_URL=http://pmis.burgercom.co.za python manage.py collectstatic --noinput && \
	cd ../insight && \
	make production-build && \
	sudo chgrp -R webapp . && \
	sudo /etc/init.d/nginx restart \
	sudo supervisorctl restart production"

.PHONY: serve production-reindex development-reindex deploy
