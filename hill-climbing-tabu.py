"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo, y los empates se resuelvan de forma aleatoria.
Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from problem import OptProblem
from random import choice
from time import time


class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        while True:

            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)

            # Buscar las acciones que generan el mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val == max(diff.values())]

            # Elegir una accion aleatoria
            act = choice(max_acts)

            # Retornar si estamos en un optimo local 
            # (diferencia de valor objetivo no positiva)
            if diff[act] <= 0:

                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            else:

                actual = problem.result(actual, act)
                value = value + diff[act]
                self.niters += 1


class HillClimbingReset(LocalSearch):
    """Algoritmo de ascension de colinas con reinicio aleatorio."""

    # COMPLETAR


class Tabu(LocalSearch):
    """Algoritmo de busqueda tabu."""

    def criterio_parada(cont_sm : int, value : float) -> bool:
        """Criterio de parada para la busqueda tabu
        Se combinan 2 criterios:
        1)Numero de iteraciones sin mejora
        2)Valor de umbral
        """
        max_cont_sm = 10 #Ir probando 
        valor_umbral = -90000 #Este valor lo saque del enunciado, hill dio un valor de -87840 (ir probando)
        return cont_sm == max_cont_sm and value >= valor_umbral

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con busqueda tabu.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        #Almaceno el mejor, inicialmente el estado inicial y su valor objetivo
        best = actual
        best_value = value

        #Inicializo la lista tabu
        tabu = []
        max_len = 10 #Ir probando y determinar experimentalmente el mejor valor

        #Inicializo contador de iteraciones sin mejoras
        cont_sm = 0

        while not self.criterio_parada(cont_sm, sucesor_value):
            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)

            #Filtro las acciones no tabu
            no_tabues = {act : val for act, val in diff.items() if act not in tabu}

            # Buscar las acciones que generan el mayor incremento de valor obj
            max_acts = [act for act, val in no_tabues.items() if val == max(no_tabues.values())]

            # Elegir una accion aleatoria
            act = choice(max_acts)

            #Almacenamos el sucesor de aplicar la accion elegida
            sucesor = problem.result(actual, act)

            #Almacenamos el valor objetivo del sucesor
            sucesor_value = problem.obj_val(sucesor)

            #Si el valor objetivo del sucesor es mejor que el mejor valor 
            #objetivo actual, actualizamos el mejor objetivo actual con
            #el mismo y reinicio contador sin mejora
            if sucesor_value > best_value:
                best = sucesor
                best_value = sucesor_value
                cont_sm = 0  

            #Incremento contador sin mejora
            cont_sm+=1 

            #Si la lista tabu llega a tener su capacidad maxima
            #elimino el primer elemento de la misma (el mas viejo)
            if len(tabu) == max_len:
                tabu = tabu[1:]
            
            #Agrego la accion a la lista
            tabu.append(act)

            #Nos movemos al sucesor
            actual = sucesor
            value = value + diff[act]
            self.niters += 1

        #Retornamos la mejor solucion encontrada o #Retornamos si se cumple el criterio de parada
        self.tour = best
        self.value = best_value
        end = time()
        self.time = end-start
        return

