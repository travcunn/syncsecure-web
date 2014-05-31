LOGDIR=logs

.PHONY: base python-base redis-sessions webserver

all:
	@echo "make build -- build docker images"

$(LOGDIR):
	@mkdir -p $@

build: base python-base redis-sessions webserver
	docker images

base:
	docker build --no-cache --rm -t syncsecure/$@ $@

python-base:
	docker build --no-cache --rm -t syncsecure/$@ $@

redis-sessions:
	docker build --no-cache --rm -t syncsecure/$@ $@

webserver:
	docker build --no-cache --rm -t syncsecure/$@ $@


clean: clean-logs clean-images

clean-logs:
	-@rm -rf $(LOGDIR)

clean-images:
	-@docker images -q | xargs docker rmi
