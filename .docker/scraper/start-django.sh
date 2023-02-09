#!/usr/bin/env bash

celery -A trquake.celery_service.app worker -B --concurrency=15 -l INFO
