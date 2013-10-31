import sys

from common import msg
from common.protocols import floo_proto


class EmacsProtocol(floo_proto.FlooProtocol):
    ''' Speaks floo proto, but is given the conn and we don't want to reconnect '''
    MAX_RETRIES = -1
    INITIAL_RECONNECT_DELAY = 0
    CLIENT = 'Emacs'

    def __init__(self, host, port, secure):
        super(EmacsProtocol, self).__init__(host, port, secure)
        self._needs_handshake = False

    def fd_set(self, readable, writeable, errorable):
        if not self._sock:
            return
        fileno = self.fileno()
        errorable.append(fileno)
        readable.append(fileno)
        if len(self) > 0:
            writeable.append(fileno)

    def reconnect(self):
        msg.error("emacs connection died")
        sys.exit(1)

    def stop(self):
        self.cleanup()

    def connect(self, sock=None):
        self.emit('connected')
        self._sock = sock
        self.connected = True
