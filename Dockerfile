FROM alpine
LABEL vendor=oftl

RUN apk update \
 && apk upgrade \
 && apk add \
    gcc \
    python3 \
    python3-dev \
    pytest \
    # limits.h
    musl-dev \
    linux-headers \
    bash \
    vim \
    curl

RUN pip3 install \
    dask[distributed] \
    bokeh

RUN mkdir /root/fask/
COPY fask/ /root/fask/
RUN mkdir /root/job/
COPY job/ /root/job

WORKDIR /root/
CMD ["python3", "-m", "job"]
