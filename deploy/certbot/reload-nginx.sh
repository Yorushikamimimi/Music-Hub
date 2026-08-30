#!/bin/sh
set -eu

nginx -t 2>&1
systemctl reload nginx
