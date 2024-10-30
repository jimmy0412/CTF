FROM ubuntu:bionic

RUN apt-get update
RUN apt-get install xinetd -qy
RUN useradd -m bounty_program
RUN chown -R root:root /home/bounty_program
RUN chmod -R 755 /home/bounty_program

CMD ["/usr/sbin/xinetd","-dontfork"]