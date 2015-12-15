run:
	python src/manage.py runserver
	
clear:
	python src/manage.py flush

setup:
	python src/manage.py migrate

tests:
	python src/manage.py test

test_core:
	python src/manage.py test core
	
test_lib:
	python src/manage.py test lib
	
run_citeseer:
	cd lib/CiteSeerExtractor/src && python service.py 8081

run_grobid:
	cd lib/grobid/grobid-service && mvn -Dmaven.test.skip=true jetty:run-war

req:
	pip freeze > requirements.txt