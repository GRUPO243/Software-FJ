from abc import ABC, abstractmethod
# Esta importación se usa para la abstracción
import logging
# Esta importación se usa para configurar los niveles de error, automáticamente añade la fecha, la hora y la línea de código donde ocurrió el problema en el archivo de logs.
from datetime import datetime
# Esta imoportación se usa para la gestión de fechas  y tiempos
import tkinter as tk
from tkinter import messagebox, scrolledtext

# A continuación, se definen las clases de excepción personalizadas mediante la herencia de la clase base (Exception) de Python. Estas clases permiten capturar errores específicos de validación de datos. Ante cualquier fallo durante la ejecución, la excepción será lanzada y capturada por el sistema de gestión de (logs), asegurando el registro detallado del evento sin interrumpir la continuidad del programa. 
class Validaciones (Exception):
    pass
# Validación de que los input no estén vacios
class VacioError (Validaciones):
    pass
# Validación de que (nombre) solo contenga string 
class NombreError (Validaciones):
    pass
# Validación de que (ID) sea númerico y que este en el rango asignado
class IdError (Validaciones):
    pass
# Validación de que la (edad) sea un entero y esté en el rango asignado
class EdadError (Validaciones):
    pass
# Validación de que (cargo) sea una de las opciones en la lista del programa
class CargoError (Validaciones):
    pass
# Validación de que (nombre_equipo) sea una de las opciones en la lista del programa
class NombreEquipoError (Validaciones):
    pass
# Validación de que los valores o precios sean positivos
class ValorPositivoError (Validaciones):
    pass
# Validación de cliente correctamente identificado
class ClienteError (Validaciones):
    pass
# Validación de que el formato de fecha sea correcto (AAAA-MM-DD)
class FechaError(Validaciones):
    pass
# Error cuando se intenta cancelar algo ya procesado o confirmar algo cancelado
class EstadoReservaError(Validaciones):
    pass
# Validación de que el servicio dado por el usuario sea un valido
class ServicioError (Validaciones):
    pass

# CONFIGURACIÓN DEL LOG

# Configuración del archivo de logs donde se almacenarán los errores generados durante la ejecución del programa
logging.basicConfig(
    filename = "log.txt",
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(message)s")


# A partir de esta linea se crea la clase abstracta (persona), que heredará a cliente sus atributos, en esta clase se realiza la validación correspondiente a (nombre) e (ID). Esta clase define la estructura base para cualquier individuo en el sistema y a su vez, no permite instanciación directa, (ABC). Gestiona la identidad (Nombre/ID)
class Persona(ABC):
    def __init__(self, nombre, ID):
        # Esta validación evita strings vacíos o con puros espacios
        if not nombre.strip() or not ID.strip():
            raise VacioError ("Error: El espacio no tiene información")
        # A continuación se valida que si algún caracter en el nombre es un digito, este genere un error 
        if any(char.isdigit() for char in nombre):
            raise NombreError("Error: El nombre no puede contener números.")
        # Debe ser numérico y de 6 dígitos
        if not ID.isdigit():
            raise IdError ("Error: El ID solo debe contener numeros")
        if int(ID) < 100000 or int(ID) > 999999:
            raise IdError("Error: El numero de identificación no es valido")
        self.__nombre = nombre
        self.__ID = ID 
        
    # Se crean los métodos getter para que Cliente pueda leer estos datos luego
    def get_nombre(self):
        return self.__nombre

    def get_id(self):
        return self.__ID
        
# Creación de la clase (Cliente), quien hereda de (Persona) el nombre e ID. Añade atributos específicos y aplica filtros de edad y cargos autorizados por Software FJ.      
class Cliente(Persona):
    def __init__(self, nombre, ID, edad, institucion, cargo):
        # Se valida primero que (edad, institución y cargo) no estén vacios antes de que se ejecute (nombre e ID) en esta clase
        if not edad.strip() or not institucion.strip() or not cargo.strip():
            raise VacioError ("Error: El espacio no tiene información")
        super().__init__(nombre, ID)
        cargo_valido = ["Estudiante", "Docente", "Asesor", "Asociado", "Comerciante", "Externo"]
        if int(edad) < 18 or int(edad) > 99:
            raise EdadError ("Error: La edad está fuera del rango permitido")
        if cargo not in cargo_valido:
            raise CargoError ("Error: El cargo no se encuentra en la lista")
            
        self.edad = edad
        self.institucion = institucion
        self.__cargo = cargo
        
    def get_cargo(self):
        return self.__cargo 



# CONFIGURACIÓN DE SERVICIOS

# En este momento se inicia la creación de la clase servicio y las clases que harán que el usuario pueda contratar y adquirir un servicio por parte de Software-FJ
class Servicio(ABC):
    def __init__(self, cliente, fecha, costo_base):
        try:
            # Intentamos convertir el string a un objeto fecha real
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            raise FechaError("Error: El formato de fecha debe ser AAAA-MM-DD (ej: 2026-05-01)")
        # Validación de que el costo que se está ingresando sea un valor positivo
        if float(costo_base) <= 0:
            raise ValorPositivoError("Error: El costo base debe ser un valor positivo")
        
        # Validación de que el cliente sea un objeto válido y a su vez es una forma de blindar el codigo para que no se generen errores que ppuedan dañarlo
        if not isinstance(cliente, Cliente):
            raise ClienteError("Error: El servicio requiere un objeto Cliente válido.")

        # En esta clase se usa solo un _ para los atributos para que las clases hijas a continuación puedan verlas
        self._cliente = cliente  
        self._fecha = fecha
        self._costo_base = float(costo_base)

    @abstractmethod
    def calcular_total(self, impuesto = 0.0, descuento_extra = 0.0):
        """Método obligatorio para que las hijas calculen el precio final"""
        pass
    
# CLASE ALQUILER DE EQUIPOS

class AlquilerEquipo(Servicio):
    def __init__(self, cliente, fecha, costo_base, nombre_equipo):
        super().__init__(cliente, fecha, costo_base)
        equipo_valido = ["PC_Pro", "Kit_RV", "Proyector_laser", "Tablet_digitalizadora", "Servidor_de_pruebas" ]
        if nombre_equipo not in equipo_valido:
            raise NombreEquipoError ("Error: El equipo no se encuentra en la lista")
        self.__nombre_equipo = nombre_equipo
        

    def calcular_total(self, impuesto=0.0, descuento_extra=0.0):
        # Accedemos al cargo del cliente usando el getter que ya hiciste
        cargo = self._cliente.get_cargo() # Si el atributo es __cargo en Cliente
        total = self._costo_base
        self.impuesto = impuesto
        self.descuento_extra = descuento_extra
        
        if cargo == "Estudiante":
            total *= 0.70  # 30% de descuento
        elif cargo == "Asociado":
            total *= 0.60  # 40% de descuento
            
        # 2. Aplicar descuento extra (Sobrecarga técnica)
        # Si el usuario pasa un descuento_extra, se aplica sobre el total
        if descuento_extra > 0:
            total -= (total * descuento_extra)
            
        # 3. Aplicar impuestos (Sobrecarga técnica)
        if impuesto > 0:
            total += (total * impuesto)
            
        return total  
    
# CLASE SALA

# Esta clase representa el servicio de reserva de salas.
# Hereda de la clase abstracta Servicio.
class AlquilerSala(Servicio):
    def __init__(self, cliente, fecha, costo_base, nombre_sala, hora):
        super().__init__(cliente, fecha, costo_base)
        # Validación de hora
        if hora <= 0:
            raise ValorPositivoError("Error: Las horas deben ser mayores a 0")
        self.hora = int(hora)
        self.nombre_sala = nombre_sala

    # Implementación del cálculo del costo
    def calcular_total(self, impuesto=0.0, descuento_extra=0.0):
        total = self.hora * self._costo_base
        if impuesto > 0: total += (total * impuesto)
        return total

    # Descripción del servicio
    def descripcion(self):
       return f"Sala '{self.nombre_sala}' reservada por {self.hora} horas"


# CLASE ASESORIA

# Esta clase representa el servicio de asesorías especializadas.
class Asesoria(Servicio):

    def __init__(self, cliente, fecha, costo_base, asesoria, hora):
        super().__init__(cliente, fecha, costo_base)
        if hora <= 0:
            raise ValorPositivoError("Error: Las horas deben ser mayores a 0")
        self.hora = int(hora)
        self.asesoria = asesoria

    # Implementación del cálculo del costo
    def calcular_total(self, impuesto=0.0, descuento_extra=0.0): # Añadidos parámetros
        total = self.hora * self._costo_base
        if impuesto > 0: total += (total * impuesto)
        return total

    # Descripción del servicio
    def descripcion(self):
        return f"Asesoría '{self.asesoria}' realizada por {self.hora} horas"


# IMPLEMENTACIÓN DE LA CLASE RESERVA

class Reserva:
    def __init__(self, cliente, servicio, duracion):
        # Validación de que el cliente y servicio sean objetos válidos
        if not isinstance(cliente, Cliente):
            raise ClienteError("Error: Se requiere un cliente válido para la reserva.")
        if not isinstance(servicio, Servicio):
            raise ServicioError("Error: Se requiere un servicio válido.")
        
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion # Ej: "2 horas" o "3 días"
        self.__estado = "Pendiente" # Estado inicial por defecto

    # MÉTODO: CONFIRMAR
    def confirmar_reserva(self):
        if self.__estado == "Cancelada":
            logging.error(f"Intento de confirmar reserva cancelada - ID: {self.__cliente.get_id()}")
            raise EstadoReservaError("Error: No se puede confirmar una reserva que ya fue cancelada.")
        self.__estado = "Confirmada"
        logging.info(f"Reserva CONFIRMADA - Cliente: {self.__cliente.get_nombre()} - ID: {self.__cliente.get_id()}")
        print(f"Reserva confirmada para {self.__cliente.get_nombre()}.")

    # MÉTODO: CANCELAR
    def cancelar_reserva(self):
        if self.__estado == "Procesada":
            raise EstadoReservaError("Error: No se puede cancelar un servicio que ya fue procesado y cobrado.")
        self.__estado = "Cancelada"
        print(f"Reserva cancelada exitosamente.")

    # MÉTODO: PROCESAR (PAGO Y LOG)
    def procesar_reserva(self, es_empresa=False):
        # Si es empresa, le sumamos el IVA del 19%
        iva = 0.19 if es_empresa else 0.0
        try:
            if self.__estado != "Confirmada":
                raise EstadoReservaError("Error: La reserva debe estar 'Confirmada' para ser procesada.")
            
            total = self.__servicio.calcular_total(impuesto=iva)
            self.__estado = "Procesada"
            logging.info(f"Reserva PROCESADA - Cliente: {self.__cliente.get_nombre()} - Total: ${total:.2f} (IVA: {iva})")
            
            print("\n" + "="*30)
            print("SISTEMA DE PROCESAMIENTO FJ")
            print(f"Cliente: {self.__cliente.get_nombre()}")
            print(f"Servicio: {type(self.__servicio).__name__}")
            print(f"Duración: {self.__duracion}")
            print(f"Total Final: ${total:.2f}")
            print("="*30)
            
        except Exception as e:
            logging.error(f"Fallo al procesar reserva: {e}")
            raise e

    # Getter para consultar el estado actual
    def get_estado(self):
        return self.__estado

if __name__ == "__main__":
    # Aquí solo va código de prueba que no se ejecutará 
    # cuando la interfaz importe el archivo.
    pass
