start:
	docker pull yzh44yzh/wg_forge_backend_env:1.1
	docker run -p 5432:5432 -d yzh44yzh/wg_forge_backend_env:1.1
bash_conteiner:
	docker exec -ti $(docker ps -q | head -n 1) bash
enter_db:
	psql ${DATABASE_CONNECTION}

stop:
	docker stop $(docker ps -q | head -n 1)
run:
	flask --app service run --port 8000
local_run :
	python3 service/server.py
tasks1_2: 
	python3 tasks1_2.py
test:
	poetry run pytest tests/test_app.py