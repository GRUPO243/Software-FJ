import tkinter as tk
# 'tkinter' es la biblioteca estándar de Python para crear interfaces gráficas de usuario (GUI) al usar 'as tk', creamos un alias corto para no tener que escribir 'tkinter' cada vez.
from tkinter import ttk, messagebox
# 'ttk' (Themed Tkinter) es un módulo dentro de tkinter que proporciona acceso a widgets con un aspecto más moderno y nativo (como botones, barras de progreso, etc.). 'messagebox' se importa específicamente para mostrar ventanas emergentes de alerta o confirmación.
import logging
# El módulo 'logging' se utiliza para registrar eventos, errores o mensajes de depuración en la consola o en un archivo, permitiendo rastrear el comportamiento del programa sin usar solo 'print'.
from SOFTWARE_FJ import Cliente, AlquilerEquipo, AlquilerSala, Asesoria, Reserva, Validaciones
# Aquí se importan elementos específicos desde un archivo local llamado 'SOFTWARE_FJ.py'. Esto indica una arquitectura modular donde la lógica de negocio está separada de la interfaz:                                                                         - Cliente: Clase para gestionar los datos de los usuarios.                                                                        - AlquilerEquipo, AlquilerSala, Asesoria: Clases que representan los servicios ofrecidos.                                         - Reserva: Clase encargada de coordinar las fechas y vinculaciones de los servicios.                                              - Validaciones: Probablemente un conjunto de funciones o clase para verificar formatos (emails, fechas, etc.).


# Definimos la clase principal que construirá la interfaz gráfica

class InterfazSoftwareFJ:
    def __init__(self, root):
    # El método __init__ se ejecuta automáticamente al crear un objeto de esta clase
        self.root = root
        # 'root' es la ventana principal de la aplicación que viene de Tkinter
        self.root.title("Software FJ - Sistema de Reservas")
        # Establece el texto que aparecerá en la barra de título de la ventana
        self.root.geometry("500x650")
        # Define el tamaño inicial de la ventana: 500 píxeles de ancho por 650 de alto
        
        
        # SECCIÓN 1: DATOS DEL CLIENTE
        tk.Label(root, text="REGISTRO DE CLIENTE", font=("Arial", 12, "bold")).pack(pady=10)
        # Creamos un título visual (Label) dentro de la ventana. pack(pady=10) lo coloca en la pantalla con un margen vertical de 10 píxeles.
        self.frame_cliente = tk.LabelFrame(root, text=" Información Personal ", padx=10, pady=10)
        # 'LabelFrame' es un contenedor con un borde y un título (" Información Personal ") para agrupar visualmente los campos de texto.
        self.frame_cliente.pack(padx=20, fill="x")
        # .pack(padx=20, fill="x") lo ajusta al ancho de la ventana con márgenes laterales.
        
        # CAMPOS DE ENTRADA (Grid Layout) 
        tk.Label(self.frame_cliente, text="Nombre:").grid(row=0, column=0, sticky="w")
        # Usamos .grid() para organizar los elementos en filas (row) y columnas (column) como una tabla.
        # Etiqueta y campo de texto para el Nombre
        self.ent_nombre = tk.Entry(self.frame_cliente)
        self.ent_nombre.grid(row=0, column=1, pady=2)

        tk.Label(self.frame_cliente, text="ID (6 dígitos):").grid(row=1, column=0, sticky="w")
        # Etiqueta y campo para el ID
        self.ent_id = tk.Entry(self.frame_cliente)
        self.ent_id.grid(row=1, column=1, pady=2)

        tk.Label(self.frame_cliente, text="Edad:").grid(row=2, column=0, sticky="w")
        # Etiqueta y campo para la Edad es)
        self.ent_edad = tk.Entry(self.frame_cliente)
        self.ent_edad.grid(row=2, column=1, pady=2)

        tk.Label(self.frame_cliente, text="Institución:").grid(row=3, column=0, sticky="w")
        # Etiqueta y campo para la Institución
        self.ent_inst = tk.Entry(self.frame_cliente)
        self.ent_inst.grid(row=3, column=1, pady=2)

        tk.Label(self.frame_cliente, text="Cargo:").grid(row=4, column=0, sticky="w")
        # Etiqueta y Menú Desplegable (Combobox) para el Cargo
        self.combo_cargo = ttk.Combobox(self.frame_cliente, values=["Estudiante", "Docente", "Asesor", "Asociado", "Comerciante", "Externo"], state="readonly", width=17)
        # El Combobox permite elegir de una lista predefinida (values) state="readonly" impide que el usuario escriba cosas que no están en la lista
        self.combo_cargo.grid(row=4, column=1, pady=2)

        # SECCIÓN 2: DATOS DEL SERVICIO
        
        # Título visual para separar la información del cliente de la del servicio.
        tk.Label(root, text="DATOS DEL SERVICIO", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Marco contenedor (LabelFrame) para agrupar los campos de configuración del servicio.
        self.frame_serv = tk.LabelFrame(root, text=" Configuración de Servicio ", padx=10, pady=10)
        self.frame_serv.pack(padx=20, fill="x")

        # Etiqueta y menú desplegable para elegir qué tipo de servicio se va a reservar.
        tk.Label(self.frame_serv, text="Tipo de Servicio:").grid(row=0, column=0, sticky="w")
        self.combo_tipo = ttk.Combobox(self.frame_serv, values=["Alquiler de Equipo", "Reserva de Sala", "Asesoría"], state="readonly", width=17)
        self.combo_tipo.grid(row=0, column=1, pady=2)
        # bind vincula un evento (seleccionar una opción del combo) con una función (actualizar_campos_especificos). Esto hace que la interfaz "reaccione" al cambio de selección.
        self.combo_tipo.bind("<<ComboboxSelected>>", self.actualizar_campos_especificos)

        # Campo para ingresar la fecha. Nota: El texto (AAAA-MM-DD) sirve de guía visual.
        tk.Label(self.frame_serv, text="Fecha (AAAA-MM-DD):").grid(row=1, column=0, sticky="w")
        self.ent_fecha = tk.Entry(self.frame_serv)
        self.ent_fecha.grid(row=1, column=1, pady=2)

        # Campo para ingresar el precio unitario o base del servicio seleccionado.
        tk.Label(self.frame_serv, text="Costo Base ($):").grid(row=2, column=0, sticky="w")
        self.ent_costo = tk.Entry(self.frame_serv)
        self.ent_costo.grid(row=2, column=1, pady=2)

        # CAMPOS DINÁMICOS 
        # Estos elementos se guardan en variables (self.lbl_especifico) para poder cambiar su texto más tarde.self.lbl_especifico = tk.Label(self.frame_serv, text="Selección:")
        self.lbl_especifico = tk.Label(self.frame_serv, text="Selección:")
        self.lbl_especifico.grid(row=3, column=0, sticky="w")
        # Input donde se escribirá el nombre del equipo, sala o tema.
        self.ent_especifico = tk.Entry(self.frame_serv) 
        self.ent_especifico.grid(row=3, column=1, pady=2)

        # Campo para la cantidad de tiempo (horas o días dependiendo del contexto).
        tk.Label(self.frame_serv, text="Cant. (Horas/Días):").grid(row=4, column=0, sticky="w")
        self.ent_cantidad = tk.Entry(self.frame_serv)
        self.ent_cantidad.grid(row=4, column=1, pady=2)

        # BOTÓN DE ACCIÓN
        
        # Botón principal. bg="#2E7D32" le da un color verde. 'command=self.ejecutar_aplicacion' indica qué función debe correr cuando se haga clic.
        self.btn_procesar = tk.Button(root, text="GENERAR RESERVA Y FACTURA", bg="#2E7D32", fg="white", font=("Arial", 10, "bold"), command=self.ejecutar_aplicacion)
        self.btn_procesar.pack(pady=20)

    # Función que cambia el texto de la etiqueta según el tipo de servicio elegido.
    def actualizar_campos_especificos(self, event):
        # Obtiene el valor actual del Combobox.
        tipo = self.combo_tipo.get()
        if tipo == "Alquiler de Equipo":
            self.lbl_especifico.config(text="Nombre del Equipo:")
        elif tipo == "Reserva de Sala":
            self.lbl_especifico.config(text="Nombre de Sala:")
        else:
            self.lbl_especifico.config(text="Tema Asesoría:")

    # Función principal que procesa la lógica de negocio al presionar el botón.
    def ejecutar_aplicacion(self):
        try:
            # Bloque para intentar convertir las entradas de texto en números.
            try:
                cantidad_num = int(self.ent_cantidad.get())
                costo_num = float(self.ent_costo.get())
            except ValueError:
                # Si el usuario escribió letras en vez de números, lanzamos una excepción personalizada.
                raise Validaciones("Error: El costo y la cantidad deben ser valores numéricos.")
            # 1. Intentar crear una instancia de la clase Cliente con los datos de los Entry.
            # Aquí se usan los 'get()' para extraer lo que el usuario escribió en la interfaz.
            cliente = Cliente(
                self.ent_nombre.get(), 
                self.ent_id.get(), 
                self.ent_edad.get(), 
                self.ent_inst.get(), 
                self.combo_cargo.get()
            )

            # 2. INTENTAR CREAR EL SERVICIO SEGÚN LA ELECCIÓN 
            
            # Extraemos los valores actuales de los campos de la interfaz para usarlos en la lógica.
            tipo = self.combo_tipo.get()
            fecha = self.ent_fecha.get()
            costo = self.ent_costo.get()
            detalle = self.ent_especifico.get()
            cant = self.ent_cantidad.get()

            # Estructura condicional para instanciar la clase correspondiente según el 'tipo' seleccionado.
            if tipo == "Alquiler de Equipo":
                # Crea un objeto de la clase AlquilerEquipo pasando el cliente y los detalles.
                servicio = AlquilerEquipo(cliente, fecha, costo_num, detalle)
            # Crea un objeto AlquilerSala (incluye cantidad_num para las horas/días).
            elif tipo == "Reserva de Sala":
                servicio = AlquilerSala(cliente, fecha, costo_num, detalle, cantidad_num)
            # Crea un objeto Asesoria con los parámetros necesarios.
            elif tipo == "Asesoría":
                servicio = Asesoria(cliente, fecha, costo_num, detalle, cantidad_num)
            else:
                # Si por alguna razón el combo está vacío o no coincide, lanzamos un error manual.
                raise Validaciones("Debe seleccionar un tipo de servicio.")

            # 3. CREAR Y PROCESAR LA RESERVA 
            
            # Se crea el objeto 'Reserva' que vincula al cliente con el servicio generado arriba.
            reserva = Reserva(cliente, servicio, f"{cantidad_num} unidades/tiempo")
            # Llama al método para validar internamente que la reserva puede realizarse.
            reserva.confirmar_reserva()
            
            # MOSTRAR FACTURA Y RESULTADOS
            
            # Calculamos el costo total llamando al método del objeto 'servicio' (aplica reglas de negocio).
            total = servicio.calcular_total()
            # Ejecuta la lógica final de la reserva (como guardar en base de datos o archivos logs).
            reserva.procesar_reserva() 
            
            # Lanza una ventana emergente (Pop-up) de éxito con el resumen de la transacción.
            # ':.2f' formatea el número total a dos decimales.
            messagebox.showinfo("ÉXITO", f"Reserva Procesada\nCliente: {cliente.get_nombre()}\nTotal: ${total:.2f}")

        # GESTIÓN DE ERRORES (EXCEPCIONES)
        except Validaciones as e:
            # Captura errores específicos definidos en tu lógica (ej: IDs mal formados, campos vacíos). Muestra el mensaje de error al usuario y guarda el registro en el archivo log.
            messagebox.showerror("Error de Validación", str(e))
            logging.error(f"Interfaz - Error: {e}")
        except Exception as e:
            # Captura cualquier otro error no previsto (errores de sistema, fallos de memoria, etc.). Se usa 'logging.critical' porque son fallos que podrían detener el programa.
            messagebox.showerror("Error Crítico", f"Ocurrió un error inesperado: {e}")
            logging.critical(f"Interfaz - Crítico: {e}")

# PUNTO DE ENTRADA DEL PROGRAMA 

# Esta condición asegura que el código de abajo solo se ejecute si este archivo es el principal.
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazSoftwareFJ(root)
    root.mainloop()