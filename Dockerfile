FROM node:lts-stretch AS builder
WORKDIR /opt/build
ADD . ./
RUN yarn install
RUN yarn build



FROM python:3.7-stretch
WORKDIR /opt/covid-19-find
ADD api .
WORKDIR /opt/covid-19-find
RUN pip install -r requirements.txt
ENV DATA_DIR /tmp
ENV FLASK_ENV production
COPY --from=builder /opt/build/dist ./static
ENV STATIC_DATA_DIR /opt/covid-19-find/static
EXPOSE 8080
CMD ["waitress-serve", "--call", "covid19find:create_app"]