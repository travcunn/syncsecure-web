LOGDIR=logs

.PHONY: base python-base redis-cache redis-sessions sentry webserver

all:
	@echo "make build -- build docker images"

$(LOGDIR):
	@mkdir -p $@

build: base python-base redis-cache redis-sessions sentry webserver
	docker images

base:
	docker build --no-cache --rm -t syncsecure/$@ $@

python-base:
	docker build --no-cache --rm -t syncsecure/$@ $@

redis-cache:
	docker build --no-cache --rm -t syncsecure/$@ $@

redis-sessions:
	docker build --no-cache --rm -t syncsecure/$@ $@

sentry:
	docker build --no-cache --rm -t syncsecure/$@ $@

webserver:
	docker build --no-cache --rm -t syncsecure/$@ $@


clean: clean-logs clean-images clean-containers

clean-logs:
	-@rm -rf $(LOGDIR)

clean-images:
	-@docker images -q | xargs docker rmi

clean-containers:
	-@docker ps -a -q | xargs docker rm
