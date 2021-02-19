FROM node:lts-stretch AS builder
WORKDIR /opt/build
ADD . ./
RUN yarn install
RUN yarn build


FROM python:3.7-stretch

WORKDIR /app

ADD api .


WORKDIR /app

RUN pip install -r requirements.txt --no-cache-dir

ENV DATA_DIR /tmp
ENV FLASK_ENV production
COPY --from=builder /opt/build/dist ./static
ENV STATIC_DATA_DIR /app/static
RUN chgrp -R 0 . && \
    chmod -R g+rwx .

EXPOSE 8080
CMD ["waitress-serve", "--call", "covid19find:create_app"]
