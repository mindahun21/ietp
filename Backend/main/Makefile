.PHONY: install
install:
	poetry install

.PHONY: runserver
runserver:
	poetry run python3 -m manage runserver

.PHONY: migrate
migrate:
	poetry run python3 -m manage migrate

.PHONY: migrations
migrations:
	poetry run python3 -m manage makemigrations


.PHONY: shell
shell:
	poetry run python3 -m manage shell

.PHONY: test
test:
	poetry run python3 -m manage test

.PHONY: superuser
superuser:
	poetry run python3 -m manage createsuperuser

.PHONY: tailwind
tailwind:
	poetry run python3 -m manage tailwind start


.PHONY: generate_patients
generate_patients:
	poetry run python3 -m manage generate_patients

.PHONY: graph_models
graph_models:
	poetry run python3 -m manage graph_models -a -o models_diagram.png