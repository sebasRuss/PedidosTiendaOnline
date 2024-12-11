import threading
import time
import queue
import random

# Cola compartida con capacidad máxima de 5 pedidos
cola_pedidos = queue.Queue(maxsize=5)

# Variable compartida para contar el número total de pedidos
contador_pedidos = 0
# Lock para proteger el acceso al contador de pedidos
lock = threading.Lock()

# Contador para los pedidos procesados
pedidos_procesados = 0

def cliente(id_cliente):
    #variable global para el contador de los pedidos
    global contador_pedidos
    while True:
        with lock:
            if contador_pedidos >= 15:
                break
            pedido = f"Pedido-{contador_pedidos + 1}"
            cola_pedidos.put(pedido)  # Agregar pedido a la cola
            print(f"Cliente {id_cliente} generó el pedido: {pedido}")
            contador_pedidos += 1
        time.sleep(1 + (random.random() * 1))  # Pausa aleatoria entre 1 y 2 segundos

def empleado(id_empleado):
    # variable global para el contador de los pedidos
    global pedidos_procesados
    while True:
        try:
            # Timeout de 2 segundos
            pedido = cola_pedidos.get(timeout=2)
            print(f"Empleado {id_empleado} procesando el pedido: {pedido}")
            # Pausa aleatoria entre 2 y 3 segundos
            time.sleep(2 + (random.random() * 1))
            with lock:
                pedidos_procesados += 1
            cola_pedidos.task_done()  # Indicar que el pedido ha sido procesado
        except queue.Empty:
            if pedidos_procesados >= 15:  # Terminar cuando se procesen todos los pedidos
                break

# Crear hilos para los clientes y empleados
hilos_clientes = [threading.Thread(target=cliente, args=(i,)) for i in range(1, 4)]
hilos_empleados = [threading.Thread(target=empleado, args=(i,)) for i in range(1, 3)]

# Iniciar los hilos
for hilo in hilos_clientes:
    hilo.start()
for hilo in hilos_empleados:
    hilo.start()

# Esperar a que todos los hilos terminen
for hilo in hilos_clientes:
    hilo.join()
for hilo in hilos_empleados:
    hilo.join()
