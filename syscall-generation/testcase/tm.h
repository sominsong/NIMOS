#ifndef __TM_H__
#define __TM_H__

int tm_fd;
int open_tm();
void tm_write_start(int fd, char *syscall, char *options);
void tm_write_end(int fd, char *syscall);

#endif