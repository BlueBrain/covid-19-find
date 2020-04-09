#!/usr/bin/env bash
set -e

rm -rvf release release.tar.gz

mkdir release

cp -rv api  release
cp -rv dist release/static

tar -zcvf release.tar.gz release

