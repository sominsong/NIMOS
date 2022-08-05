IMAGE=$1

# check number of arguments
if [ $# -ne 1 ] ; then
	echo "Usage: $0 image_name"
	exit 0
fi

# mongod (mongodb) / httpd (httpd) / nginx (nginx)
echo "Setting ftrace for ${IMAGE}..."
case ${IMAGE} in
    "mongodb")
        echo "Traced process name is 'mongod'"
        pids=$(ps -efT | grep 'mongod ' | grep -v "grep" | awk '{print $3}' | sed '$d' | uniq)
        ;;
    "mysql")
        echo "Traced process name is 'mysqld'"
        pids=$(ps -efT | grep 'mysqld' | grep -v "grep" | awk '{print $3}' | sed '$d' | uniq)
        ;;
    "httpd")
        echo "Traced process name is 'httpd'"
        pids=$(ps -efT | grep 'httpd ' | grep -v "grep" | awk '{print $3}' | sed '$d' | uniq)
        ;;
    "nginx")
        echo "Traced process name is 'nginx'"
        pids=$(ps -efT | grep 'nginx' | grep -v "grep" | awk '{print $3}' | sed '$d' | uniq)
        ;;
    "redis")
        echo "Traced process name is 'redis-server'"
        pids=$(ps -efT | grep 'redis-server' | grep -v "grep" | awk '{print $3}' | sed '$d' | uniq)
        ;;
    "mariadb")
        echo "Traced process name is 'mariadbd'"
        pids=$(ps -efT | grep 'mariadbd' | grep -v "grep" | awk '{print $3}' | sed '$d' | uniq)
        ;;
    "node")
        echo "Traced process name is 'node'"
        pids=$(ps -efT | grep ' node' | grep -v "grep" | grep -v "docker exec" | awk '{print $3}' | sed '$d' | uniq)
        ;;
    "tomcat")
        echo "Traced process name is 'tomcat'"
        pids=$(ps -efT | grep '1189142' | grep -v "grep" | awk '{print $3}' | sed '$d' | uniq)
        ;;
    "ubuntu")
        echo "Traced process name is 'containerd-shim'"
        pids=$(ps -efT | grep 'containerd-shim-runc-v2' | grep -v "grep" | awk '{print $3}' | sed '$d' | uniq)
        ;;
    *)
        echo "Invalid argument"
        exit 1
        ;;
esac

echo "start to setup ftrace"
echo "reset ftrace"
trace-cmd reset && sleep 1

echo "tracing off"
echo 0 > /sys/kernel/tracing/tracing_on && sleep 1

echo "nop tracer enabled"
echo "nop" > /sys/kernel/tracing/current_tracer && sleep 1

echo "enable syscall events"
echo "1" > /sys/kernel/tracing/events/syscalls/enable && sleep 1

echo "set_event_pid enabled"
echo "${pids}" > /sys/kernel/tracing/set_event_pid && sleep 1

echo "set event-fork option"
echo event-fork > /sys/kernel/tracing/trace_options && sleep 1

echo "set saved_cmdlines_size to 32768"
echo 32768 > /sys/kernel/tracing/saved_cmdlines_size && sleep 1

echo "set norecord-tgid option"
echo norecord-tgid > /sys/kernel/tracing/trace_options && sleep 1

echo "ftrace setup completed"

