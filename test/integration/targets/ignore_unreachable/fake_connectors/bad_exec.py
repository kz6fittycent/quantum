import quantum.plugins.connection.local as quantum_local
from quantum.errors import QuantumConnectionFailure

from quantum.utils.display import Display
display = Display()


class Connection(quantum_local.Connection):
    def exec_command(self, cmd, in_data=None, sudoable=True):
        display.debug('Intercepted call to exec remote command')
        raise QuantumConnectionFailure('BADLOCAL Error: this is supposed to fail')
