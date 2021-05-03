from python:3.8-alpine
ENV PATH="/scripts:${PATH}"

COPY ./requirements.txt ./requirements.txt
RUN apk update && \
apk add --no-cache graphviz ttf-freefont && \
apk add --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip install -r /requirements.txt
RUN apk del .tmp

RUN mkdir /jsonToImg
COPY ./* /jsonToImg
WORKDIR /jsonToImg
