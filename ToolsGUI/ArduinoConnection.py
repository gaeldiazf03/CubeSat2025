import serial
import serial.tools.list_ports
from threading import Thread
from queue import Queue, Empty
from typing import List
from Measurements import Singleton


def get_ports() -> List[str]:
    return [port.device for port in serial.tools.list_ports.comports()]


@Singleton
class ArduinoConnection:
    """
    Esta librería es para conectarse a cualquier tipo de Arduino o ESP32 con protocolo serial
    Alert: ¡Módulo creado con bastante ayuda de ChatGPT, por lo que intenta no modificarlo!
    Function: creando un hilo independiente, donde estará leyendo el serial en paralelo y regresando
    lo que recibe. Desde el tkinter se debe de actualizar cada cierto tiempo una función solamente
    para reflejar lo que recibes de este módulo. A este módulo hace falta un ejemplo de uso, pero es verdaderamente intuitivo.
    """
    running: bool = False
    cola: Queue = Queue()

    def __init__(self) -> None:
        self.vector: serial.Serial = serial.Serial()
        self.vector.port = ''
        self.vector.baudrate = 0
        self.vector.timeout = 0.0

    def connect(self, port: str, baud: int, timeout: float = 5) -> None:
        """Conectar al Serial seleccionado"""
        self.vector.port = port
        self.vector.baudrate = baud
        self.vector.timeout = timeout

        try:
            self.vector.open()
            self.running = True
            print(f"""
            ============================
            |   Port: {port}           |          
            |   Baudrate: {baud}       |
            ============================
            """)
        except Exception as e:
            raise Exception(e)

    def disconnect(self) -> None:
        """Desconectar del Serial"""
        if self.vector.is_open:
            self.running = False
            self.vector.close()
            self.vector.__del__()
            print("""
            ============================
            |   Arduino disconnected!  |
            ============================
            """)
        else:
            print("""
            ============================
            |   Never found Arduino!   |
            ============================
            """)

    def reading(self) -> None:
        """La lectura del serial se separa en paralelo y se almacena en una cola"""
        while self.running:
            try:
                data = str(self.vector.readline().strip().decode('utf-8'))
                self.cola.put(data)
            except serial.SerialException as e:
                print(f'Error al abrir puerto. {e}')
                print(f"""
                ============================
                |   Error en el puerto     |
                ============================
                """)
                self.running = False
            except AttributeError:
                pass
            except Exception as e:
                print(f"""
                ============================
                |   Error:\n               |
                |         {e}              |
                ============================
                """)

    def start_reading(self) -> None:
        """Inicia en paralelo"""
        Thread(target=self.reading, daemon=True).start()

    def get_reading(self):
        """Regresa la lectura del serial en paralelo"""
        try:
            return self.cola.get_nowait()
        except Empty:
            return None

    def send_data(self, data: str) -> None:
        """Mandar datos al serial en paralelo"""
        data = data + "\r\n"
        if self.vector.is_open:
            try:
                self.vector.write(data.encode('utf-8'))
            except serial.SerialException as e:
                print(f"""
                ============================
                | Error mandando los datos |
                | {e}                      |
                ============================
                """)
            except Exception as e:
                print(f"""
                ============================
                |   Error inesperado       |
                |   {e}                    |
                ============================
                """)

    def check_connection(self) -> bool:
        """Confirma que está disponible la conexión"""
        return self.vector.is_open

    def reset_connection(self):
        """Nos ayuda a limpiar el serial conectado"""
        self.vector.reset_input_buffer()
