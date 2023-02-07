#!/usr/bin/env bash

celery -A trquake.celery.app worker -B --concurrency=50 -l INFO
