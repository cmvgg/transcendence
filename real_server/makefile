all:
	@chmod +x setup_monitoring.sh
	@bash setup_monitoring.sh
	@docker-compose up --build -d

down:
	@docker-compose down

re: clean
	@docker-compose down && docker-compose up --build -d

run:
	@docker-compose down && docker-compose up --build -d && docker exec -it real_server-backend-1 bash

clean:
	@docker stop $$(docker ps -qa) || true;\
	docker rm $$(docker ps -qa) || true;\
	docker rmi -f $$(docker images -qa) || true;\
	docker volume rm $$(docker volume ls -q) || true;\
	docker network rm $$(docker network ls -q) || true;\
	docker system prune -f --volumes || true;\
	find . -name "__pycache__" -type d -exec rm -r {} +	;\
	find . -name "*.pyc" -delete 

.PHONY: all re down clean