FROM alpine:3.12

WORKDIR /usr/bin

COPY go-cqhttp_linux_amd64 .

WORKDIR /data

CMD [ "/usr/bin/go-cqhttp_linux_amd64", "-faststart" ]