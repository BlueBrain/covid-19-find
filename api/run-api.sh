#!/usr/bin/env bash

export FLASK_ENV=production
export STATIC_DATA_DIR=../static

waitress-serve --call 'covid19find:create_app'

