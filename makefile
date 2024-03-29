ifeq ($(OS),Windows_NT)     # is Windows_NT on XP, 2000, 7, Vista, 10...
    SHELL=cmd.exe
endif

all:
	@echo "Available commands: \n\
		make installdeps : to install poetry and other dependent packages\n\
		make createmigrations: generate the migration files for defined models \n\
		make install : to install poetry, other dependent packages, and create migrations \n\
		make migrate : creates tables in database \n\
		make adminuser : creates a superuser to access the django admin \n\
		make collectstatic : collectstatic and compress \n\
		make dev : runs django development server \n\
		make run : run the django application \n\
		make shell : start a poetry shell with all required packages available in the environment \n\
		make lint : runs linters on all project files and shows the changes \n\
		make typecheck : run the static type check  \n\
		make test : run the test suite  \n\
		make coverage : runs tests and creates a report of the coverage \n\
		make production : run the the django application by docker-compose \n\
	"

installdeps:
	python3 -m pip install poetry
	poetry install

createmigrations:
	poetry run python manage.py makemigrations

install: installdeps createmigrations

migrate:
	poetry run python manage.py migrate --database default
	poetry run python manage.py migrate --database mongodb

collectstatic:
	poetry run python manage.py collectstatic
	poetry run python manage.py compress

dev:
	poetry run python manage.py runserver

run:
	# the default settings file is development, it can be changed
	# for any of the others, please don't use development setting in production
	poetry run gunicorn livevil_blog.wsgi:application --bind localhost:8000

shell:
	@echo 'Starting poetry shell. Press Ctrl-d to exit from the shell'
	poetry shell

lint:
	# starts a poetry shell, shows yapf diff and then fixes the files
	# does the same for isort
	@echo '---Running yapf---'
	poetry run yapf livevil_blog -r -d
	poetry run yapf livevil_blog -r -i
	@echo '---Running isort---'
	poetry run isort livevil_blog --diff
	poetry run isort livevil_blog --atomic

typecheck:
	@echo 'Running static type check'
	poetry run mypy livevil_blog

coverage:
	@echo 'Running tests and making coverage files'
	poetry run coverage run manage.py test
	poetry run coverage report
	poetry run coverage html
	@echo 'to see the complete report, open ./coverage_html_report/index.html on the coverage_html_report folder'

adminuser:
	test $(password) || (echo '>> password is not set. (e.g password=mysecretpassword)'; exit 1)
	@echo 'creating Django admin user'
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
	User.objects.create_superuser('admin', '', '$(password)')" \
	| poetry run python manage.py shell
	@echo 'Username: admin , Password: $(password)'

test:
	@echo 'Running tests'
	poetry run python manage.py test

production:
	docker-compose -f production.yml build
	docker-compose -f production.yml up
