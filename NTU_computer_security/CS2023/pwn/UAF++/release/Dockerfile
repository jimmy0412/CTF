FROM ubuntu@sha256:4a45212e9518f35983a976eead0de5eecc555a2f047134e9dd2cfc589076a00d
MAINTAINER YingMuo

RUN apt-get update && \
    DEBAIN_FRONTEND=noninteractive apt-get install -qy xinetd

RUN useradd -m chal
RUN chown -R root:root /home/chal
RUN chmod -R 755 /home/chal

CMD ["/usr/sbin/xinetd", "-dontfork"]
