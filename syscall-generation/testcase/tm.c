#include "tm.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>


#define TRACE_MARKER_PATH      "/sys/kernel/tracing/trace_marker"

int tm_fd;

int open_tm()
{
    int fd = open(TRACE_MARKER_PATH, O_WRONLY);
    if (fd < 0) {
        perror("Failed to open trace_marker");
        exit(1);
    }

    return fd;
}

void tm_write_start(int fd, char *syscall, char *options)
{
    char buf[64];
    strcpy(buf, syscall);
    strcat(buf, " start ");
    strcat(buf, options);
    strcat(buf, "\n");
    write(fd, buf, sizeof(buf));
}

void tm_write_end(int fd, char *syscall)
{
    char buf[64];
    strcpy(buf, syscall);
    strcat(buf, " end\n");
    write(fd, buf, sizeof(buf));
}
