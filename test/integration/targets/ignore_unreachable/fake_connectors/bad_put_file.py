import quantum.plugins.connection.local as quantum_local
from quantum.errors import QuantumConnectionFailure

from quantum.utils.display import Display
display = Display()


class Connection(quantum_local.Connection):
    def put_file(self, in_path, out_path):
        display.debug('Intercepted call to send data')
        raise QuantumConnectionFailure('BADLOCAL Error: this is supposed to fail')
