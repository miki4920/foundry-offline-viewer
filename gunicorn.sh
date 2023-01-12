#!/bin/bash
gunicorn --chdir app app:app -b 0.0.0.0:8000