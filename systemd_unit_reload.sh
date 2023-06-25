#!/bin/bash

run () {
    SERVICE_NAME="hydrapp"
    systemctl stop $SERVICE_NAME.service
    systemctl daemon-reload
    systemctl start $SERVICE_NAME.service
    systemctl status $SERVICE_NAME.service --no-pager
}

run
