import simpy
import random


class SimuladorSistema:
    def __init__(self, env, total_ram=100, cpu_capacidad=1, 
                 instrucciones_por_ciclo=3, random_seed=42):
        
        self.env = env
        self.total_ram = total_ram
        self.cpu_capacidad = cpu_capacidad
        self.instrucciones_por_ciclo = instrucciones_por_ciclo
        
        random.seed(random_seed)

        # Recursos
        self.RAM = simpy.Container(env, init=total_ram, capacity=total_ram)
        self.CPU = simpy.Resource(env, capacity=cpu_capacidad)

        # Métricas
        self.tiempos_procesos = []

    def proceso(self, nombre):
        tiempo_llegada = self.env.now
        
        memoria_requerida = random.randint(1, 10)
        instrucciones_restantes = random.randint(1, 10)

        # Solicitar memoria
        yield self.RAM.get(memoria_requerida)

        while instrucciones_restantes > 0:
            
            with self.CPU.request() as request:
                yield request

                # Ejecuta por 1 unidad de tiempo
                yield self.env.timeout(1)

                instrucciones_restantes -= self.instrucciones_por_ciclo

                if instrucciones_restantes < 0:
                    instrucciones_restantes = 0

        # Termina el proceso
        yield self.RAM.put(memoria_requerida)

        tiempo_salida = self.env.now
        self.tiempos_procesos.append(tiempo_salida - tiempo_llegada)

    def generar_procesos(self, cantidad, intervalo):
        for i in range(cantidad):
            yield self.env.timeout(random.expovariate(1.0 / intervalo))
            self.env.process(self.proceso(f"Proceso {i}"))

    def correr_simulacion(self, cantidad_procesos, intervalo):
        self.env.process(self.generar_procesos(cantidad_procesos, intervalo))
        self.env.run()
        return self.tiempos_procesos