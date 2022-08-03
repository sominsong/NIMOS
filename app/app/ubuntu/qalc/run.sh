service strace-docker restart

# cross product (vector)
docker run --rm myqalc bash -c "sleep 1; qalc 'cross((1; 2; 3); (4; 5; 6))'"

# hadamard product (matrix)
docker run --rm myqalc bash -c "sleep 1; qalc 'hadamard([[1; 2; 3]; [4; 5; 6]]; [[7; 8; 9]; [10; 11; 12]])'"
