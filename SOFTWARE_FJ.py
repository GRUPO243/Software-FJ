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
    # Clase abstracta que representa un servicio general. Hereda de ABC (Abstract Base Class), lo que significa que no se puede
    # crear un objeto directamente de esta clase, sino únicamente de sus clases hijas. Sirve como plantilla para definir atributos y métodos comunes.
    def __init__(self, cliente, fecha, costo_base):
    # Método constructor que se ejecuta automáticamente al crear un objeto. Recibe tres parámetros:- cliente: objeto de la clase Cliente que solicita el servicio.
    # - fecha: fecha en la que se realizará o registrará el servicio. - costo_base: valor inicial del servicio antes de impuestos o descuentos.
        try:
        # Intentamos convertir la fecha ingresada (que llega como texto) al formato AAAA-MM-DD utilizando datetime.strptime().
        # Esto permite verificar que la fecha tenga una estructura válida.
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
        # Si la fecha no cumple con el formato indicado o contiene valores inválidos (por ejemplo, 2026-13-40), Python genera un ValueError.
        # En ese caso, lanzamos una excepción personalizada llamada FechaError con un mensaje claro para el usuario.
            raise FechaError("Error: El formato de fecha debe ser AAAA-MM-DD (ej: 2026-05-01)")
            # Verificamos que el costo base sea un número mayor que cero. Primero convertimos el valor a float para aceptar tanto enteros
            # como números decimales.
        if float(costo_base) <= 0:
        # Si el costo es cero o negativo, se lanza una excepción personalizada.
            raise ValorPositivoError("Error: El costo base debe ser un valor positivo")
            # Validamos que el parámetro 'cliente' sea realmente un objeto de la clase Cliente.
            # isinstance() devuelve True si el objeto pertenece a esa clase. Validación de que el cliente sea un objeto válido y a su vez es una forma de blindar el codigo para que no se generen errores que ppuedan dañarlo
        if not isinstance(cliente, Cliente):
        # Si no es un objeto Cliente válido, se lanza una excepción personalizada para evitar errores posteriores.
            raise ClienteError("Error: El servicio requiere un objeto Cliente válido.")
            # Guardamos el objeto cliente en un atributo protegido. El prefijo "_" indica que este atributo no debería modificarse
            # directamente fuera de la clase, aunque sí puede ser utilizado por las clases hijas. En esta clase se usa solo un _ para los atributos para que las clases hijas a continuación puedan verlas
        self._cliente = cliente  
        # Guardamos la fecha validada.
        self._fecha = fecha
        # Guardamos el costo base convertido a tipo float para asegurar que siempre se maneje como un número decimal.
        self._costo_base = float(costo_base)

    @abstractmethod
    # Decorador que indica que este método es abstracto. Esto obliga a todas las clases hijas de Servicio a implementar
    # su propia versión de este método.
    def calcular_total(self, impuesto = 0.0, descuento_extra = 0.0):
    # Método abstracto encargado de calcular el valor final del servicio.
    # Parámetros:- impuesto: porcentaje o valor adicional que se suma al costo. - descuento_extra: descuento adicional que se resta al total.
    # Cada clase hija definirá su propia lógica para calcular el precio final. Por ejemplo, un servicio de hotel puede aplicar temporadas, mientras que un servicio de spa puede aplicar promociones.    
        """Método obligatorio para que las hijas calculen el precio final"""
        pass
        # 'pass' se utiliza porque este método no tiene implementación en la clase base; solo sirve como plantilla obligatoria.

# CLASE ALQUILER DE EQUIPOS

class AlquilerEquipo(Servicio):
# Clase hija de Servicio. Representa un servicio especializado en el alquiler de equipos tecnológicos.
#  Hereda todos los atributos y validaciones de la clase Servicio (cliente, fecha y costo_base), y añade un atributo específico: nombre_equipo.
    def __init__(self, cliente, fecha, costo_base, nombre_equipo):
    # Método constructor de la clase AlquilerEquipo. 
    # Parámetros:- cliente: objeto de la clase Cliente que solicita el alquiler. - fecha: fecha del servicio en formato AAAA-MM-DD.- costo_base: valor inicial del alquiler. - nombre_equipo: nombre del equipo que se desea alquilar.
    # Llamamos al constructor de la clase padre (Servicio) para reutilizar todas sus validaciones: - formato correcto de la fecha - costo_base positivo - cliente válido    
        super().__init__(cliente, fecha, costo_base)
        # Lista de equipos permitidos por el sistema. Solo se podrán registrar alquileres con estos nombres.
        equipo_valido = ["PC_Pro", "Kit_RV", "Proyector_laser", "Tablet_digitalizadora", "Servidor_de_pruebas" ]
         # Verificamos que el equipo ingresado se encuentre en la lista de equipos válidos.
        if nombre_equipo not in equipo_valido:
         # Si el nombre no existe en la lista, lanzamos una excepción personalizada para informar al usuario.   
            raise NombreEquipoError ("Error: El equipo no se encuentra en la lista")
            # Guardamos el nombre del equipo en un atributo privado. El doble guion bajo (__) activa name mangling,
            # lo que impide el acceso directo desde fuera de la clase.
        self.__nombre_equipo = nombre_equipo
        

    def calcular_total(self, impuesto=0.0, descuento_extra=0.0):
    # Método sobrescrito de la clase Servicio. 
    # Calcula el valor final del alquiler aplicando: 1. Descuento según el tipo de cliente. 2. Descuento adicional opcional. 3. Impuesto opcional. Parámetros: - impuesto: porcentaje adicional (por ejemplo, 0.19 para 19%).- descuento_extra: porcentaje de descuento adicional   (por ejemplo, 0.10 para 10%).
    # Obtenemos el cargo o tipo de cliente utilizando el método getter definido en la clase Cliente. Ejemplo de valores posibles: "Estudiante", "Asociado".
        cargo = self._cliente.get_cargo() 
        # Inicializamos el total con el costo base heredado de la clase Servicio.
        total = self._costo_base
        # Guardamos el valor del impuesto como atributo del objeto. Esto puede ser útil si posteriormente se desea consultar.
        self.impuesto = impuesto
        # Guardamos el descuento adicional como atributo del objeto.
        self.descuento_extra = descuento_extra
        # Si el cliente es un Estudiante, se aplica un 30% de descuento. Esto significa que el cliente paga solo el 70% del valor.
        if cargo == "Estudiante":
            total *= 0.70  
        # Si el cliente es un Asociado, se aplica un 40% de descuento. Esto significa que el cliente paga solo el 60% del valor.
        elif cargo == "Asociado":
            total *= 0.60 
        # Aplicar descuento adicional. Si el usuario proporciona un valor mayor que cero, se calcula ese porcentaje y se resta al total actual.
        # Ejemplo: total = 100000 descuento_extra = 0.10 resultado = 90000    2. Aplicar descuento extra (Sobrecarga técnica) Si el usuario pasa un descuento_extra, se aplica sobre el total
        if descuento_extra > 0:
            total -= (total * descuento_extra)
        # Aplicar impuesto. Si el valor del impuesto es mayor que cero, se calcula ese porcentaje y se suma al total. 
        # Ejemplo: total = 90000 impuesto = 0.19 resultado = 107100
        if impuesto > 0:
            total += (total * impuesto)
        # Retornamos el valor final del alquiler después de aplicar todos los descuentos e impuestos correspondientes.    
        return total  
    
# CLASE SALA

# Esta clase representa el servicio de reserva de salas.
# Hereda de la clase abstracta Servicio.
class AlquilerSala(Servicio):
# Clase hija de Servicio que representa el alquiler o reserva de una sala por un número determinado de horas.    
    def __init__(self, cliente, fecha, costo_base, nombre_sala, hora):
    # Constructor que recibe el cliente, la fecha, el costo por hora, el nombre de la sala y la cantidad de horas reservadas.
        super().__init__(cliente, fecha, costo_base)
        # Llama al constructor de la clase padre para validar y asignar cliente, fecha y costo_base.
        if hora <= 0:
        # Verifica que la cantidad de horas sea mayor que cero.    
            raise ValorPositivoError("Error: Las horas deben ser mayores a 0")
        # Lanza una excepción si el número de horas es inválido.
        self.hora = int(hora)
        # Convierte el valor de horas a entero y lo almacena en el atributo hora.
        self.nombre_sala = nombre_sala
        # Guarda el nombre de la sala que será reservada.

    # Implementación del cálculo del costo
    def calcular_total(self, impuesto=0.0, descuento_extra=0.0):
    # Método que calcula el costo total del alquiler, pudiendo aplicar un impuesto opcional.
        total = self.hora * self._costo_base
        # Multiplica la cantidad de horas por el costo base por hora para obtener el subtotal.
        if impuesto > 0: total += (total * impuesto)
        # Si se especifica un impuesto mayor a cero, lo calcula y lo suma al subtotal.
        return total
        # Retorna el valor final del alquiler de la sala.


    # Descripción del servicio
    def descripcion(self):
    # Método que devuelve una descripción textual del servicio de alquiler.
       return f"Sala '{self.nombre_sala}' reservada por {self.hora} horas"
       # Retorna una cadena indicando el nombre de la sala y la cantidad de horas reservadas.


# CLASE ASESORIA

# Esta clase representa el servicio de asesorías especializadas.
class Asesoria(Servicio):
# Clase hija de Servicio que representa un servicio de asesoría cobrado según la cantidad de horas trabajadas.

    def __init__(self, cliente, fecha, costo_base, asesoria, hora):
    # Constructor que recibe el cliente, la fecha, el costo por hora, el tipo de asesoría y la duración en horas.
        super().__init__(cliente, fecha, costo_base)
        # Llama al constructor de la clase padre para validar y asignar cliente, fecha y costo_base.
        if hora <= 0:
        # Verifica que la cantidad de horas ingresada sea mayor que cero.
            raise ValorPositivoError("Error: Las horas deben ser mayores a 0")
            # Lanza una excepción si el número de horas no es válido.
        self.hora = int(hora)
        # Convierte el valor de horas a entero y lo almacena en el atributo hora.
        self.asesoria = asesoria
        # Guarda el nombre o tipo de la asesoría que se va a prestar.

    # Implementación del cálculo del costo
    def calcular_total(self, impuesto=0.0, descuento_extra=0.0):
    # Método que calcula el costo total de la asesoría y permite aplicar un impuesto opcional.
        total = self.hora * self._costo_base
        # Multiplica la cantidad de horas por el costo base por hora para obtener el subtotal.
        if impuesto > 0: total += (total * impuesto)
        # Multiplica la cantidad de horas por el costo base por hora para obtener el subtotal.
        return total
        # Retorna el valor final que debe pagar el cliente por la asesoría.

    # Descripción del servicio
    def descripcion(self):
    # Método que genera una descripción legible del servicio prestado.
        return f"Asesoría '{self.asesoria}' realizada por {self.hora} horas"
        # Devuelve una cadena con el nombre de la asesoría y la cantidad de horas trabajadas.


# IMPLEMENTACIÓN DE LA CLASE RESERVA

class Reserva:
 # Clase que representa una reserva realizada por un cliente para un servicio específico durante un tiempo determinado.
    def __init__(self, cliente, servicio, duracion):
    # Constructor que recibe el cliente, el servicio reservado y la duración estimada de la reserva.
        if not isinstance(cliente, Cliente):
        # Verifica que el parámetro cliente sea realmente un objeto de la clase Cliente.
            raise ClienteError("Error: Se requiere un cliente válido para la reserva.")
            # Lanza una excepción si el cliente no es válido.
        if not isinstance(servicio, Servicio):
        # Verifica que el parámetro servicio sea una instancia de la clase Servicio o de alguna de sus clases hijas.
            raise ServicioError("Error: Se requiere un servicio válido.")
            # Lanza una excepción si el servicio no es válido.
        
        self.__cliente = cliente
        # Almacena el objeto cliente en un atributo privado para proteger su acceso directo.
        self.__servicio = servicio
        # Guarda el objeto servicio asociado a la reserva en un atributo privado.
        self.__duracion = duracion 
        # Guarda la duración de la reserva como texto, por ejemplo "2 horas" o "3 días".
        self.__estado = "Pendiente" 
        # Inicializa el estado de la reserva como "Pendiente" hasta que sea confirmada o cancelada.

    # MÉTODO: CONFIRMAR
    def confirmar_reserva(self):
    # Método que cambia el estado de la reserva a "Confirmada" si aún no ha sido cancelada.
        if self.__estado == "Cancelada":
        # Verifica si la reserva ya fue cancelada anteriormente.
            logging.error(f"Intento de confirmar reserva cancelada - ID: {self.__cliente.get_id()}")
            # Registra en el archivo de log un intento inválido de confirmación.
            raise EstadoReservaError("Error: No se puede confirmar una reserva que ya fue cancelada.")
            # Lanza una excepción para impedir la confirmación.
        self.__estado = "Confirmada"
        # Cambia el estado de la reserva a "Confirmada".
        logging.info(f"Reserva CONFIRMADA - Cliente: {self.__cliente.get_nombre()} - ID: {self.__cliente.get_id()}")
        # Registra en el log que la reserva fue confirmada exitosamente.
        print(f"Reserva confirmada para {self.__cliente.get_nombre()}.")
        # Muestra un mensaje en consola informando que la reserva fue confirmada.

    # MÉTODO: CANCELAR
    def cancelar_reserva(self):
    # Método que permite cancelar una reserva siempre y cuando aún no haya sido procesada y cobrada.
        if self.__estado == "Procesada":
        # Verifica si la reserva ya fue procesada, es decir, si el servicio ya fue facturado.
            raise EstadoReservaError("Error: No se puede cancelar un servicio que ya fue procesado y cobrado.")
            # Lanza una excepción para impedir la cancelación.
        self.__estado = "Cancelada"
        # Cambia el estado actual de la reserva a "Cancelada".
        print(f"Reserva cancelada exitosamente.")
        # Muestra un mensaje en consola indicando que la cancelación se realizó correctamente.

    # MÉTODO: PROCESAR (PAGO Y LOG)
    def procesar_reserva(self, es_empresa=False):
    # Método que calcula el pago final, aplica IVA si corresponde y cambia el estado a "Procesada".
        iva = 0.19 if es_empresa else 0.0
        # Si el cliente es una empresa se aplica un IVA del 19%; de lo contrario, no se aplica impuesto.
        try:
        # Inicia un bloque de manejo de excepciones para capturar cualquier error durante el procesamiento.
            if self.__estado != "Confirmada":
            # Verifica que la reserva haya sido confirmada antes de procesarla.
                raise EstadoReservaError("Error: La reserva debe estar 'Confirmada' para ser procesada.")
                # Lanza una excepción si la reserva no está confirmada.
            
            total = self.__servicio.calcular_total(impuesto=iva)
            # Llama al método calcular_total del servicio y le envía el IVA para obtener el valor final a pagar.
            self.__estado = "Procesada"
            # Cambia el estado de la reserva a "Procesada", indicando que ya fue cobrada.
            logging.info(f"Reserva PROCESADA - Cliente: {self.__cliente.get_nombre()} - Total: ${total:.2f} (IVA: {iva})")
            # Registra en el archivo de log la información del procesamiento exitoso.
            print("\n" + "="*30)
            # Imprime una línea decorativa de 30 signos "=" precedida por un salto de línea.
            print("SISTEMA DE PROCESAMIENTO FJ")
            # Imprime el título del comprobante generado por el sistema.
            print(f"Cliente: {self.__cliente.get_nombre()}")
            # Muestra el nombre del cliente que realizó la reserva.
            print(f"Servicio: {type(self.__servicio).__name__}")
            # Muestra el nombre de la clase del servicio reservado.
            print(f"Duración: {self.__duracion}")
            # Muestra la duración registrada para la reserva.
            print(f"Total Final: ${total:.2f}")
            # Muestra el valor final a pagar con dos decimales.
            print("="*30)
            # Imprime otra línea decorativa para cerrar el comprobante.
            
        except Exception as e:
        # Captura cualquier excepción que ocurra durante el procesamiento.
            logging.error(f"Fallo al procesar reserva: {e}")
            # Registra en el archivo de log el detalle del error ocurrido.
            raise e
            # Vuelve a lanzar la excepción para que pueda ser manejada en otra parte del programa.

    # Getter para consultar el estado actual
    def get_estado(self):
    # Método getter que permite consultar el estado actual de la reserva.
        return self.__estado
        # Retorna el valor del atributo privado __estado.

if __name__ == "__main__":
# Este bloque solo se ejecuta cuando el archivo se corre directamente y no cuando es importado desde otro módulo.
# Aquí se pueden escribir pruebas del programa para verificar su funcionamiento sin afectar la interfaz gráfica.
    pass
    # Instrucción vacía utilizada como marcador para indicar que no hay código de prueba por el momento.
        