NAME="inquisitor.py"

PINK="\033[35;1m"
GREEN="\033[32;1m"
TEAL="\033[36;1m"
BLUE="\033[34;1m"
RED="\033[31;1m"
END="\033[0m"

build:
	docker-compose build
	docker-compose up -d

client:
	docker exec -it ftp_client sh

server:
	docker exec -it ftp_server sh

inquisitor:
	docker exec -it inquisitor /bin/bash

clean:
	docker-compose down

IP_CLIENT := $(shell docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ftp_client)
IP_SERV := $(shell docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ftp_server)

MAC_CLIENT := $(shell docker inspect --format='{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' ftp_client)
MAC_SERV := $(shell docker inspect --format='{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' ftp_server)

info:
	@echo $(TEAL)">> IP server:	"$(END)$(IP_SERV)"\n"
	@echo $(TEAL)">> MAC server:	"$(END)$(MAC_SERV)"\n"
	@echo $(GREEN)">> IP client:	"$(END)$(IP_SERV)"\n"
	@echo $(GREEN)">> MAC client:	"$(END)$(MAC_SERV)"\n"

run: 
	@echo $(GREEN)">> Run this command: "$(END)
	@echo python3 program/$(NAME) $(IP_SERV) $(MAC_SERV) $(IP_CLIENT) $(MAC_CLIENT)

.PHONY: build client server inquisitor info clean fclean run