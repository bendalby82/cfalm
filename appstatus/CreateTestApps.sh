#!/bin/bash

cd sampleapp
cf push testapp1 -b php_buildpack -m 36M -i 1
cf set-env testapp1 ALM_VERSION 1.23

cf push testapp2 -b php_buildpack -m 36M -i 2 --no-start
cf set-env testapp2 ALM_VERSION 2.4.1

cf push testapp3 -b php_buildpack -m 36M -i 1
cf set-env testapp3 ALM_VERSION 1.8

cf push testapp4 -b php_buildpack -m 36M -i 10 --no-start
cf set-env testapp4 ALM_VERSION v0.1

cf push testapp5 -b php_buildpack -m 36M -i 1

cf push testapp6 -b php_buildpack -m 36M -i 3

cf push testapp7 -b php_buildpack -m 36M -i 1
cf set-env testapp7 ALM_VERSION 5.9.2.b12345

cf push testapp8 -b php_buildpack -m 36M -i 2
cf set-env testapp8 ALM_VERSION 2

cf push testapp9 -b php_buildpack -m 36M -i 1
cf set-env testapp9 ALM_VERSION TEST

cf push testapp10 -b php_buildpack -m 36M -i 1
cf set-env testapp10 ALM_VERSION 19
