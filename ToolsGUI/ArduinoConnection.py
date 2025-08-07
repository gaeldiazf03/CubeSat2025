from serial import Serial, SerialException
from serial.tools.list_ports import comports
from threading import Thread, Lock
from queue import Queue, Empty
from typing import List, Optional
from Measurements import Singleton


def get_ports() -> List[str]:
    """Lista de puertos seriales disponibles"""
    return [port.device for port in comports()]


@Singleton
class ArduinoConnection:
    """
    Esta librería es para conectarse a cualquier tipo de Arduino o ESP32 con protocolo serial
    Alert: ¡Módulo creado con bastante ayuda de ChatGPT, por lo que intenta no modificarlo!
    Function: creando un hilo independiente, donde estará leyendo el serial en paralelo y regresando
    lo que recibe. Desde el tkinter se debe de actualizar cada cierto tiempo una función solamente
    para reflejar lo que recibes de este módulo. A este módulo hace falta un ejemplo de uso, pero es verdaderamente intuitivo.
    Example:
        arduino = ArduinoConnection()
        arduino.connect()
        arduino.start_reading()

        while True:
            data = arduino.get_reading()
            if data:
                print(data)
    """
    VALID_BAUDS     = {9600, 19200, 38400, 57600, 115200}

    def __init__(self) -> None:
        self._serial: Serial  = Serial()
        self._serial.port     = ''
        self._serial.baudrate = 0
        self._serial.timeout  = 0.0

        self._running: bool   = False
        self._cola: Queue     = Queue(maxsize=1000)
        self._lock: Lock      = Lock()

    def connect(self, port: str, baud: int, timeout: float = 5) -> None:
        """Conectar al Serial seleccionado"""

        if baud not in self.VALID_BAUDS:
            raise ValueError(f"Invalid baudrate. Must be one of {self.VALID_BAUDS}")

        with self._lock:
            self._serial.port     = port
            self._serial.baudrate = baud
            self._serial.timeout  = timeout

            try:
                self._serial.open()
                self._running = True
                print(f"""
                ============================
                |   Port: {port}           |          
                |   Baudrate: {baud}       |
                ============================
                """)
            except SerialException as e:
                raise ConnectionError(f"Fallo al conectar al puerto {port}: {e}")

    def disconnect(self) -> None:
        """Desconectar del Serial"""
        if not self._running:
            print("""
            ============================
            |   Arduino never found (R)|
            ============================
            """)
            return

        if not self._serial.is_open:
            print("""
            ============================
            |   Arduino never found (S)|
            ============================
            """)
            return

        with (self._lock):
            self._running = False
            self._serial.close()
            print("""
            ============================
            |   Arduino disconnected!  |
            ============================
            """)

    def reading(self) -> None:
        """La lectura del serial se separa en paralelo y se almacena en una _cola"""
        while self._running:
            try:
                if data := self._serial.readline().decode('utf-8').strip():
                    with self._lock:
                        self._cola.put(data)
            except (SerialException, AttributeError) as e:
                with self._lock:
                    self._running = False
                print(f"""
                ============================
                |   Error en el puerto     |
                ============================
                {e}
                """)

    def start_reading(self) -> None:
        """Inicia en paralelo"""
        if not self._running:
            raise RuntimeError("""
            ============================
            |   Sin conectarse.        |
            |   Llama a connect().     |
            ============================
            """)
        Thread(target=self.reading, daemon=True).start()

    def get_reading(self) -> Optional[str]:
        """Regresa la lectura del serial en paralelo"""
        with self._lock:
            try:
                return self._cola.get_nowait()
            except Empty:
                return None

    def send_data(self, data: str) -> None:
        """Mandar datos al serial en paralelo"""
        if not self._running:
            raise RuntimeError(f"""
            ============================
            |   Sin conectarse.        |
            |   Llama a connect().     |
            ============================
            """)

        with self._lock:
            try:
                self._serial.write(f"{data}\r\n".encode('utf-8'))
            except SerialException as e:
                print(f"""
                ============================
                | Error mandando los datos |
                ============================
                {e}
                """)

    def check_connection(self) -> bool:
        """Confirma que está disponible la conexión"""
        return self._serial.is_open

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
