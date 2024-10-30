FROM ubuntu:22.04
MAINTAINER ice1187

RUN apt update && apt install -y openssh-server xxd
RUN mkdir /var/run/sshd
EXPOSE 22

RUN useradd -ms /bin/bash ais3
RUN sed -i.bak -E 's/^ais3:!:/ais3:$1337$5P9T6lkeH4e3RO449w6d6G2O6b4p76e314dsG4Q7417oO555$4L99xi8ZjdfbtYb487dabxH1fh1Xaban7P0Mbfp1Ha90722c:/g' /etc/shadow

RUN  cp /usr/lib/x86_64-linux-gnu/security/pam_unix.so /usr/lib/x86_64-linux-gnu/security/pam_unix.so.bak
COPY ./pam_unix.so /usr/lib/x86_64-linux-gnu/security/pam_unix.so
#COPY ./flag.txt /home/ais3/flag.txt

CMD ["/usr/sbin/sshd", "-D"]
