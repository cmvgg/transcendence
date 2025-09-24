all:
	@docker-compose --profile core down
	@chmod +x setup_monitoring.sh
	@bash setup_monitoring.sh
	@chmod +x setup_certs.sh
	@bash setup_certs.sh
	@docker-compose --profile core --profile monitoring up --build -d

core:
	@chmod +x setup_monitoring.sh
	@bash setup_monitoring.sh
	@chmod +x setup_certs.sh
	@bash setup_certs.sh
	@docker-compose --profile core up -d
 
down:
	@docker-compose down

down_monitor:
	docker-compose --profile monitoring down

re: clean
	@docker-compose down && docker-compose --profile core --profile monitoring up --build -d

run:
	@docker-compose down && docker-compose --profile core --profile monitoring up --build -d && docker exec -it real_server-backend-1 bash

clean:
	@docker stop $$(docker ps -qa) || true;\
	docker rm -f $$(docker ps -qa) || true;\
	docker rmi -f $$(docker images -qa) || true;\
	docker volume rm $$(docker volume ls -q) || true;\
	docker network rm $$(docker network ls -q) || true;\
	docker system prune -f --volumes || true;\
	find . -name "__pycache__" -type d -exec rm -r {} +	;\
	find . -name "*.pyc" -delete 
	rm -rf media

.PHONY: all re down clean