#!/bin/bash

docker exec -i f91e6c7ee34f /bin/bash -c "export TERM=xterm && mysql -phinhct -uroot" < data_dump.sql