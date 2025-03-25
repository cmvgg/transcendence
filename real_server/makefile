all:
	@docker-compose up --build -d

down:
	@docker-compose down

re:
	@docker-compose down && docker-compose up --build -d && docker exec -it real_server-backend-1 bash

clean:
	@docker stop $$(docker ps -qa) || true;\
	docker rm $$(docker ps -qa) || true;\
	docker rmi -f $$(docker images -qa) || true;\
	docker volume rm $$(docker volume ls -q) || true;\
	docker network rm $$(docker network ls -q) || true;\
	docker system prune -f --volumes

.PHONY: all re down clean