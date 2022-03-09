int tm_fd;
int open_tm();
void tm_write_start(int fd, char *syscall, char *options);
void tm_write_end(int fd, char *syscall);