serve:
	invoker start invoker.ini

production-reindex:
	cd server && BASE_URL=http://pmis.burgercom.co.za python manage.py seed_indices

development-reindex:
	cd server && BASE_URL=http://www.backend.dev python manage.py seed_indices

clean-server:
	cd server && find . -name '*.pyc' -delete
