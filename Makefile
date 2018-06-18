# expected from environment
# ifeq (${BASE},)
#   $(error environment variable BASE is not set)
# endif

DOCKER=/usr/bin/docker
PYTEST=/usr/bin/pytest
FIND=/usr/bin/find
# CURL=/usr/bin/curl
# TAR=/usr/bin/tar

IMAGE=ondewo
CONTAINER=ondewo01

# fetch_data:
# 	${CURL} https://www.cs.cmu.edu/~./enron/enron_mail_20150507.tar.gz --output /data/mail.tar.gz
# 	${TAR} xzvf data/mail.tar.gz

build:
	$(warning "make sure needed config files are available")
	${DOCKER} build --tag ${IMAGE} --file Dockerfile src/

run:
	${DOCKER} run --rm -it --publish 127.0.0.1:8787:8787 ${IMAGE}

inspect:
	${DOCKER} run --rm -it --publish 127.0.0.1:8787:8787 ${IMAGE} bash

clean:
	${FIND} . -name *pyc | xargs rm -f
	${FIND} . -name __pycache__ | xargs rm -rf
	${FIND} . -name .pytest_cache | xargs rm -fr
	${FIND} . -name dask-worker-space | xargs rm -fr

distclean: clean
	${DOCKER} rm ${CONTAINER}
	${DOCKER} rmi ${IMAGE}

test:
	${DOCKER} run --rm -it --publish 127.0.0.1:8787:8787 ${IMAGE} ${PYTEST} fask/
	${DOCKER} run --rm -it --publish 127.0.0.1:8787:8787 ${IMAGE} ${PYTEST} job/
