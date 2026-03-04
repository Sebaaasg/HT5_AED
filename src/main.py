import os # Permite interactuar con los archivos de la computadora
import simpy
import statistics # Tiene fórmulas matemáticas listas para usar como el promedio
import matplotlib.pyplot as plt # Ayuda a generar las gráficas con líneas y puntos

# Se importa la clase que hecha en simulacion.py
from simulacion import SimuladorSistema

def ejecutar_escenario(cant_procesos, intervalo, ram=100, cpu_cap=1, vel=3):
    
    # Función auxiliar para instanciar el entorno y correr una configuración específica
    # Retorna el promedio y la desviación estándar de los tiempos
    
    # Se crea el reloj maestro que lleva el tiempo de esta prueba en particular
    env = simpy.Environment()

    # Se instancia el simulador con los parámetros que queremos probar, se crea la computadora virtual con los componentes indicados
    simulador = SimuladorSistema(
        env, 
        total_ram=ram, 
        cpu_capacidad=cpu_cap, 
        instrucciones_por_ciclo=vel
    )
    
    # Se corre la simulación y se guarda el registro de tiempos de todos los programas
    tiempos = simulador.correr_simulacion(cant_procesos, intervalo)
    
    # Se calcula el tiempo promedio usando la lista de resultados obtenidos
    promedio = statistics.mean(tiempos)

    # Se calcula la desviación estándar
    # Esto exige por lo menos dos datos y siempre se tendrá un mínimo de 25
    desviacion = statistics.stdev(tiempos) 
    
    # Se entregan los dos valores calculados a quien sea que haya llamado a esta función
    return promedio, desviacion

def main():
    # Primero se hace la preparación de la carpeta para guardar las imágenes
    # Se busca la ubicación de este código y se hace que retroceda una carpeta
    # para luego crear una nueva carpeta llamada "graficas" en dado caso no existiera
    ruta_graficas = os.path.join(os.path.dirname(__file__), "..", "graficas")

    # Si la carpeta ya existe, el programa no hace nada y sigue adelante sin dar error
    os.makedirs(ruta_graficas, exist_ok=True)

    # Parámetros obligatorios de la hoja de trabajo
    cantidades = [25, 50, 100, 150, 200]
    intervalos = [10, 5, 1]

    # Diccionario con los 4 escenarios (El original + las 3 optimizaciones)
    # Tiene el escenario base y las 3 estrategias de mejora
    escenarios = {
        "Base (RAM=100, 1 CPU, Vel=3)": {"ram": 100, "cpu_cap": 1, "vel": 3},
        "Estrategia A (RAM=200)":       {"ram": 200, "cpu_cap": 1, "vel": 3},
        "Estrategia B (CPU Vel=6)":     {"ram": 100, "cpu_cap": 1, "vel": 6},
        "Estrategia C (2 CPUs)":        {"ram": 100, "cpu_cap": 2, "vel": 3}
    }

    print("Iniciando batería de simulaciones de la HT5")

    # Segundo, se realiza la ejecución y recolección de datos
    # Se itera sobre cada intervalo para generar una gráfica comparativa por cada nivel de tráfico
    for intervalo in intervalos:

        # Se prepara un lienzo en blanco para dibujar la gráfica con un tamaño específico.
        plt.figure(figsize=(10, 6))

        print(f"\n================================================")
        print(f" RESULTADOS PARA INTERVALO DE LLEGADA: {intervalo}")
        print(f"================================================")
        
        # Este segundo ciclo evalúa cada una de las 4 estrategias dentro de ese ritmo de llegada
        for nombre_escenario, config in escenarios.items():

            # Lista vacía para ir guardando los promedios de esta estrategia en particular
            promedios_por_cantidad = []
            print(f"\n--- {nombre_escenario} ---")
            
            # Este tercer ciclo prueba las distintas cantidades de procesos
            for cant in cantidades:

                # Se llama a la función "laboratorio" pasándole las configuraciones
                promedio, desviacion = ejecutar_escenario(
                    cant_procesos=cant, 
                    intervalo=intervalo, 
                    ram=config["ram"], 
                    cpu_cap=config["cpu_cap"], 
                    vel=config["vel"]
                )

                # Se guarda el promedio obtenido en la lista para luego poder graficarlo
                promedios_por_cantidad.append(promedio)

                # Se muestra en pantalla el resultado de este experimento con un formato ordenado
                print(f"Procesos: {cant:<3} | Promedio: {promedio:>7.2f} | Desviación: {desviacion:>7.2f}")
            
            # Se agrega la línea de este escenario a la gráfica del intervalo actual
            # se dibuja su línea en el lienzo
            # La instrucción "marker='o'" pone un puntito visible en cada dato de la gráfica
            plt.plot(cantidades, promedios_por_cantidad, marker='o', label=nombre_escenario)

        # Tercero, se realiza la configuración y exportación de la gráfica
        # Se pone título, etiquetas para los lados y se muestra el cuadro de leyendas
        plt.title(f"Tiempo Promedio vs Procesos (Llegada cada {intervalo} unidades de tiempo)")
        plt.xlabel("Cantidad de Procesos")
        plt.ylabel("Tiempo Promedio en el Sistema")
        plt.legend()

        # Se coloca una cuadrícula punteada de fondo para que la imagen se lea mejor
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Se crea el nombre del archivo usando el intervalo actual 
        nombre_archivo = f"comparativa_intervalo_{intervalo}.png"

        # Unimos la ruta de la carpeta con el nombre de la imagen para saber dónde guardarla
        ruta_completa = os.path.join(ruta_graficas, nombre_archivo)

        # Se guarda la imagen en el disco duro
        plt.savefig(ruta_completa)

        # Se limpia el lienzo para la siguiente gráfica y evitar mezclar las líneas.
        plt.close() 

        
        print(f"\n[+] Gráfica exportada con éxito: graficas/{nombre_archivo}")

    print("\nSimulación terminada. Revisa la carpeta 'graficas'.")

# Esta condición asegura que el código principal solo corra si se ejecuta este archivo de forma directa
if __name__ == "__main__":
    main()