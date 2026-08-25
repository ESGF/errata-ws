#!/bin/bash
set -e

source /home/esprimod/.esdoc/credentials

export ERRATA_WS_HOME=/home/esprimod/opt/errata-ws

exec /usr/bin/supervisord \
    -c /home/esprimod/opt/errata-ws/ops/config/supervisord.conf