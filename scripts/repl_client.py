#!/usr/bin/python

import os
import errno
import socket

NEWLINE = '\r\n'

TELNET_IS       = b'\x00'

TELNET_SE       = b'\xf0'
TELNET_GOA      = b'\xf9'
TELNET_SB       = b'\xfa'
TELNET_WILL     = b'\xfb'
TELNET_WONT     = b'\xfc'
TELNET_DO       = b'\xfd'
TELNET_DONT     = b'\xfe'
TELNET_IAC      = b'\xff'

TELOPT_TERMINAL_TYPE    = b'\x18'
TELOPT_EXTEND           = b'\xfe'

TELMSG_GOAHEAD  = TELNET_IAC + TELNET_GOA
TELMSG_TERM_BEGIN   = TELNET_IAC + TELNET_SB + TELOPT_TERMINAL_TYPE + TELNET_IS
TELMSG_TERM_END     = TELNET_IAC + TELNET_SE
TELMSG_EXTEND_BEGIN = TELNET_IAC + TELNET_SB + TELOPT_EXTEND + TELNET_IS
TELMSG_EXTEND_END   = TELNET_IAC + TELNET_SE

TELNET_CMDLIST_NOARG    = b'\xf1\xf2x\f3x\f4x\xf5\xf6\xf7\xf8\xf9'
TELNET_CMDLIST_ARG      = b'\xfb\xfc\xfd\xfe'

class Connection(object):

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.__buffer = ''

    def __recv(self):
        data = self.socket.recv(2048)
        if len(data) == 0:
            raise socket.error(errno.ECONNRESET, os.strerror(errno.ECONNRESET))
        self.__buffer += data
        return data

    def __pop_buffer(self):
        result = self.__buffer
        self.__buffer = ''
        return result

    def __pop_telnet_command(self, end=None):
        n = len(self.__buffer)
        i = self.__buffer.find(TELNET_IAC, 0, end)
        if i < 0:
            return None
        if n < i + 2:
            return None
        c = self.__buffer[i+1]
        if c in TELNET_CMDLIST_NOARG:
            result = self.__buffer[i:i+2]
            self.__buffer = self.__buffer[:i] + self.__buffer[i+2:]
            return result
        elif c in TELNET_CMDLIST_ARG:
            if n > i + 2:
                result = self.__buffer[i:i+3]
                self.__buffer = self.__buffer[:i] + self.__buffer[i+3:]
                return result
        elif c in TELNET_SB:
            j = self.__buffer.find(TELNET_IAC + TELNET_SE, i)
            if j > 0:
                result = self.__buffer[i:j+2]
                self.__buffer = self.__buffer[:i] + self.__buffer[j+2:]
                return result
        else:
            raise ValueError
        return None

    def __read(self):
        while True:
            while True:
                result = self.__pop_telnet_command()
                if result is None:
                    break
                elif result == TELMSG_GOAHEAD:   # GO AHEAD
                    return self.__pop_buffer()
                elif result.startswith(TELMSG_EXTEND_BEGIN):
                    self.__extendmsg = result[4:-2]
                    return ''
            self.__recv()

    def __write(self, data):
        if len(data) == 0:
            return
        self.socket.sendall(data)

    def __fake_telnet_negotiation(self):
        self.__write(TELNET_IAC + TELNET_WILL + TELOPT_TERMINAL_TYPE)
        self.__write(TELNET_IAC + TELNET_WILL + TELOPT_EXTEND)
        self.__write(TELMSG_TERM_BEGIN + 'REPLCLIENT' + TELMSG_TERM_END)

    def startup(self):
        self.__fake_telnet_negotiation()
        return self.__read()

    def shutdown(self, how):
        return self.socket.shutdown(how)

    def send_extendmsg(self, cmd):
        self.__write(TELMSG_EXTEND_BEGIN + cmd + TELMSG_EXTEND_END)
        result = self.__read()
        if result != '':
            raise ValueError
        extendmsg = self.__extendmsg.split('\n')
        self.__extendmsg = None
        return extendmsg

    def send_command(self, cmd):
        self.__write(cmd + NEWLINE)
        return self.__read()
