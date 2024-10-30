FROM node:17

# Create app directory
RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app
RUN apt update -y
RUN apt install -y strace 

COPY readflag.c /readflag.c
RUN echo 'AIS3{fake_flag}' > /flag
RUN chmod 0400 /flag && chown root:root /flag
RUN chmod 0444 /readflag.c && gcc /readflag.c -o /readflag
RUN chown root:root /readflag && chmod 4555 /readflag

COPY . .

RUN npm install
USER nobody
EXPOSE 3001

CMD ["strace", "-f","-v", "-s", "100000", "-e", "execve", "node","app.js" ]