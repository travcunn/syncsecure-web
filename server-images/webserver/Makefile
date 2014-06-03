build:
	docker build -t webserver .

test:
	coverage run tests.py

verify:
	pyflakes app
	pep8 app

clean:
	find . -name *.pyc -delete

run:
	./run.py

install:
	pip install -r requirements.txt
