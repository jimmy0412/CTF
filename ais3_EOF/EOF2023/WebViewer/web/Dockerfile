from node:18.8.0-alpine3.16

RUN apk add python3 

WORKDIR /app
COPY ./backend.js ./
COPY ./frontend.py ./

USER nobody
CMD ["python3", "frontend.py"]
