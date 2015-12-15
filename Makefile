run:
	python manage.py runserver
	
clear:
	python manage.py flush

setup:
	python manage.py migrate

tests:
	python manage.py test
	
run_citeseer:
	cd lib/CiteSeerExtractor/src && python service.py 8081

run_grobid:
	cd lib/grobid/grobid-service && mvn -Dmaven.test.skip=true jetty:run-war

req:
	pip freeze > requirements.txt