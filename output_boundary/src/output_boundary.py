import logging
import signal
import socket
from common.middleware import Middleware
from common.packet import Packet
from common.result_packet import ResultPacket


class OutputBoundary():
    def __init__(self, port: int, backlog: int, result_queues: dict[int, str]):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.listen(backlog)
        self.server_socket = server_socket
        self.port = port
        self.middleware = Middleware()
        self.client_socket = None
        self.eofs = {query: False for query in result_queues.keys()}

        for query, queue in result_queues.items():
            self.middleware.add_input_queue(
                queue,
                self._handle_query_result(query),
                self._handle_query_eof(query),
                auto_ack=False
            )

        logging.info("Listening for connections and replying results")

    def run(self):
        signal.signal(signal.SIGTERM, self.__graceful_shutdown)

        while True:
            client_socket, address = self.server_socket.accept()
            logging.info("Connection from %s", address)
            with client_socket:
                self.__handle_client_connection(client_socket)

    def _handle_query_result(self, query: int):
        def handle_result(result: Packet):
            result_packet = ResultPacket(query, result)
            encoded_result = result_packet.encode()
            try:
                self.client_socket.sendall(encoded_result)
                return True
            except BrokenPipeError:
                logging.error("Connection closed by client")
                self.middleware.stop()
                return False

        return handle_result

    def _handle_query_eof(self, query: int):
        def handle_eof():
            self.eofs[query] = True
            if all(self.eofs.values()):
                self._reset()

        return handle_eof

    def _reset(self):
        self.eofs = {query: False for query in self.eofs.keys()}
        self.middleware.stop()
        self.client_socket.close()
        self.client_socket = None

    def __handle_client_connection(self, client_socket: socket.socket):
        self.client_socket = client_socket
        self.middleware.start()

    def __graceful_shutdown(self, signum, frame):
        # TODO: Implement graceful shutdown
        raise NotImplementedError("Graceful shutdown not implemented")