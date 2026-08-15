#!/bin/bash
set -e

echo "=================================================="
echo "⚡ Menghubungkan Replica 3 (DB4) ke Master via GTID..."
echo "=================================================="

docker exec -i mysql-replica3 mysql -uroot -prootpassword <<EOF
STOP REPLICA;
ALTER USER IF EXISTS 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'rootpassword';
FLUSH PRIVILEGES;
CHANGE REPLICATION SOURCE TO
    SOURCE_HOST='mysql-replica1',
    SOURCE_PORT=3306,
    SOURCE_USER='repl_user',
    SOURCE_PASSWORD='repl_password',
    SOURCE_AUTO_POSITION=1;
START REPLICA;
SET GLOBAL read_only = ON;
SET GLOBAL super_read_only = ON;
EOF

sleep 2
echo "✅ Status Replikasi pada Replica 3 (DB4):"
docker exec -i mysql-replica3 mysql -uroot -prootpassword -e "SHOW REPLICA STATUS\G" | grep -E "Replica_IO_Running|Replica_SQL_Running|Seconds_Behind_Master|Source_Host"
