#!/bin/sh

pip_install:
	pip install tornado
	pip install mock


dev-run:
	./app.py

test-run:
	./test_tornado.py 

run: dev-run