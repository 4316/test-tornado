#!/bin/sh

pip_install:
	pip install tornado


dev-run:
	./app.py

test-run:
	./test_tornado.py 

run: dev-run