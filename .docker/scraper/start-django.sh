#!/usr/bin/env bash

celery -A trquake.celery.app worker -B --concurrency=15 -l INFO
