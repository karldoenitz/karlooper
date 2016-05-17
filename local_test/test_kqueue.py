#!/usr/bin/env python

"""
Example on using Kqueue/Kevent on BSD/Mac
using Python.
The TCP server essentially echoes back the
message it receives on the client socket.
"""

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SHUT_WR
import sys
import select

__author__ = "Ishwor Gurung <ishwor@develworx.com>"
__license__ = "3 clause BSD"


def handle_connection(cl_socket):
    """
        Handle each client socket. Receive data on it and send
        the data back to the client. If there are no more data
        available on the read side, shutdown and close the
        socket.
    """
    while True:
        m = cl_socket.recv(1024)
        print m
        if m and len(m) > 0:
            http_data = "HTTP/1.0 200 OK\r\n" \
                        "HOST: 127.0.0.1\r\n" \
                        "Content-Type: text/html\r\n" \
                        "Content-Length: 62\r\n\r\n" \
                        "<html><head><title>test</title></head><body>test</body></html>"
            cl_socket.send(http_data)
        else:
            cl_socket.shutdown(SHUT_WR)
            cl_socket.close()
            break


def main():
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 9999))
    s.listen(10)
    kq = select.kqueue()
    # Initialise the master fd(s.fileno()) from server socket
    kevent = select.kevent(
        s.fileno(),
        filter=select.KQ_FILTER_READ,  # we are interested in reads
        flags=select.KQ_EV_ADD | select.KQ_EV_ENABLE
    )

    while True:
        revents = kq.control([kevent], 1, None)
        for event in revents:
            if event.filter == select.KQ_FILTER_READ:
                cl, _ = s.accept()
                handle_connection(cl)


if __name__ == "__main__":
    sys.exit(main())
