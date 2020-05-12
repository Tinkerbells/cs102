import socket
import multiprocessing
import time
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] (%(processName)-10s) (%(threadName)-10s) %(message)s'
)


def worker_process(serversocket: socket.socket) -> None:
    while True:
        clientsocket, (client_address, client_port) = serversocket.accept()
        logging.debug(f"New client: {client_address}:{client_port}")

        while True:
            try:
                message = clientsocket.recv(1024)
                logging.debug(f"Recv: {message} from {client_address}:{client_port}")
            except OSError:
                break

            if len(message) == 0:
                break

            sent_message = message
            while True:
                sent_len = clientsocket.send(sent_message)
                if sent_len == len(sent_message):
                    break
                sent_message = sent_message[sent_len:]
            logging.debug(f"Send: {message} to {client_address}:{client_port}")

        clientsocket.close()
        logging.debug(f"Bye-bye: {client_address}:{client_port}")


def main(host: str = 'localhost', port: int = 8090) -> None:
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    serversocket.bind((host, port))
    serversocket.listen(128)

    print(f"Starting TCP Echo Server at {host}:{port}")

    NUMBER_OF_PROCESS = multiprocessing.cpu_count()
    processes = []
    logging.debug(f"Number of processes: {NUMBER_OF_PROCESS}")
    for _ in range(NUMBER_OF_PROCESS):
        process = multiprocessing.Process(target=worker_process,
            args=(serversocket,))
        process.start()
        processes.append(process)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        for p in processes:
            p.terminate()
        serversocket.close()


if __name__ == "__main__":
    main()
