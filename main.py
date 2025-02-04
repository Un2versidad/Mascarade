import random
from tabulate import tabulate

class Carta:
    def __init__(self, nombre, habilidad):
        self.nombre = nombre
        self.habilidad = habilidad

    def usar_habilidad(self, jugador, jugadores, corte):
        return self.habilidad(jugador, jugadores, corte)

    def __str__(self):
        return self.nombre


class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.oro = 6  # Cada jugador comienza con 6 monedas de oro
        self.cartas = []  # Cartas que tiene el jugador

    def esta_vivo(self):
        return self.oro > 0

    def __str__(self):
        return f"{self.nombre} (Oro: {self.oro})"


class Corte:
    def __init__(self):
        self.total_oro = 0

    def depositar(self, cantidad):
        self.total_oro += cantidad

    def retirar(self):
        cantidad = self.total_oro
        self.total_oro = 0
        return cantidad


class Juego:
    def __init__(self):
        self.jugadores = []
        self.corte = Corte()
        self.mazo = self.crear_mazo()
        self.cartas_mesa = []
        self.turno_actual = 0  # Contador de turnos
        self.campesinos_revelados = 0

    def crear_mazo(self):
        habilidades = [
            self.habilidad_juez,
            self.habilidad_obispo,
            self.habilidad_rey,
            self.habilidad_reina,
            self.habilidad_bufon,
            self.habilidad_ladron,
            self.habilidad_bruja,
            self.habilidad_espia,
            self.habilidad_campesino,
            self.habilidad_tramposo,
            self.habilidad_inquisidor,
            self.habilidad_viuda,
        ] * 1 + [self.habilidad_campesino]  # Dos campesinos
        nombres = [
            'El Juez', 'El Obispo', 'El Rey', 'La Reina', 'El Bufón',
            'El Ladrón', 'La Bruja', 'El Espía', 'El Campesino',
            'El Tramposo', 'El Inquisidor', 'La Viuda',
        ] * 1 + ['El Campesino']
        mazo = [Carta(nombre, habilidad) for nombre, habilidad in zip(nombres, habilidades)]
        random.shuffle(mazo)
        return mazo

    def agregar_jugadores(self):
        while True:
            try:
                num_jugadores = int(input("¿Cuántos jugadores? (2 - 13): "))
                if not 2 <= num_jugadores <= 13:
                    print("Número de jugadores no válido. Debe ser entre 2 y 13.")
                    continue
                break
            except ValueError:
                print("Entrada no válida. Introduce un número.")

        for _ in range(num_jugadores):
            while True:
                nombre = input("Ingrese el nombre del jugador: ").strip()
                if not nombre:
                    print("El nombre no puede estar vacío.")
                    continue
                if any(j.nombre == nombre for j in self.jugadores):
                    print("Este nombre ya está en uso. Elige otro.")
                    continue
                break
            jugador = Jugador(nombre)
            self.jugadores.append(jugador)

        self.repartir_cartas(num_jugadores)
        self.agregar_cartas_mesa(num_jugadores)

    def repartir_cartas(self, num_jugadores):
        num_cartas = 3 if num_jugadores == 2 else 2 if num_jugadores == 3 else 1
        for jugador in self.jugadores:
            jugador.cartas = [self.mazo.pop() for _ in range(num_cartas)]

    def agregar_cartas_mesa(self, num_jugadores):
        if num_jugadores >= 4:
            num_cartas_a_agregar = random.randint(1, 2)
            for _ in range(num_cartas_a_agregar):
                if self.mazo:
                    carta_mesa = self.mazo.pop()
                    self.cartas_mesa.append(carta_mesa)
                    print(f"La carta {carta_mesa} ha sido añadida a la mesa.")

    def iniciar_juego(self):
        while True:
            self.turno_actual += 1
            self.mostrar_estado_juego()
            for jugador in self.jugadores:
                if jugador.esta_vivo():
                    print(f"\nEs el turno de: {jugador}")
                    self.turno_jugador(jugador)
                    self.mostrar_estado_juego()
                    if jugador.oro >= 13:
                        print(f"¡{jugador.nombre} ha ganado el juego!")
                        return
            if all(not j.esta_vivo() for j in self.jugadores):
                ganador = max(self.jugadores, key=lambda j: j.oro)
                print(f"¡{ganador.nombre} gana con {ganador.oro} monedas!")
                return

    def mostrar_estado_juego(self):
        print("\n--- Estado del Juego ---")
        print("Jugadores:")
        tabla_jugadores = [[j.nombre, j.oro, ", ".join(str(c) for c in j.cartas)] for j in self.jugadores]
        print(tabulate(tabla_jugadores, headers=["Nombre", "Oro", "Cartas"], tablefmt="grid"))
        print("\nCartas en la mesa:", ", ".join(str(c) for c in self.cartas_mesa))
        print("Palacio de Justicia:", self.corte.total_oro, "monedas\n")

    def turno_jugador(self, jugador):
        while True:  # Bucle para permitir reintentos hasta que se complete una acción válida
            if self.turno_actual <= 4:  # Primeros cuatro turnos limitados a intercambios
                print(f"{jugador.nombre}, en este turno solo puedes realizar intercambios.")
                self.intercambiar_cartas(jugador)
            else:
                accion = input("Seleccione una opción (1.mirar, 2.intercambiar, 3.usar habilidad): ").strip().lower()
                if accion in ["1", "mirar"]:
                    self.ver_carta(jugador)
                    break  # Acción válida completada, salir del bucle
                elif accion in ["2", "intercambiar"]:
                    self.intercambiar_cartas(jugador)
                    break  # Acción válida completada, salir del bucle
                elif accion in ["3", "usar habilidad"]:
                    self.usar_habilidad(jugador)
                    break  # Acción válida completada, salir del bucle
                else:
                    print("Acción no válida. Por favor, selecciona una opción válida.")

            # Sí se completa una acción válida, salir del bucle y avanzar al siguiente jugador
            break

    @staticmethod
    def ver_carta(jugador):
        """Permite al jugador mirar en secreto su carta."""
        if jugador.cartas:
            print(f"{jugador.nombre}, tu carta es: {jugador.cartas[0]}")
        else:
            print(f"{jugador.nombre}, no tienes cartas para mirar.")

    def intercambiar_cartas(self, jugador):
        print("Intercambia cartas con otro jugador o con la mesa.")

        # Mostrar opciones de jugadores vivos
        for idx, j in enumerate(self.jugadores):
            if j != jugador and j.esta_vivo():
                print(f"{idx + 1}. {j.nombre} (Cartas: {[str(carta) for carta in j.cartas]})")

        print("0. Intercambiar con la mesa")

        try:
            # Pedir al jugador que seleccione un objetivo
            idx_objetivo = int(input("Seleccione el número del jugador (o 0 para intercambiar con la mesa): ")) - 1

            if 0 <= idx_objetivo < len(self.jugadores):
                jugador_objetivo = self.jugadores[idx_objetivo]

                # Verificar si el jugador objetivo es diferente del jugador actual
                if jugador_objetivo == jugador:
                    print("No puedes intercambiar cartas contigo mismo.")
                    return

                # Verificar si el jugador objetivo está vivo y tiene cartas
                if jugador_objetivo.esta_vivo() and jugador_objetivo.cartas:
                    # Verificar si el jugador actual tiene cartas
                    if not jugador.cartas:
                        print(f"{jugador.nombre} no tiene cartas para intercambiar.")
                        return

                    # Elegir cartas aleatorias para el intercambio
                    carta_jugador = random.choice(jugador.cartas)
                    carta_objetivo = random.choice(jugador_objetivo.cartas)

                    print(
                        f"{jugador.nombre} intercambia {carta_jugador} con {jugador_objetivo.nombre}, recibiendo {carta_objetivo}."
                    )

                    # Realizar el intercambio
                    jugador.cartas.remove(carta_jugador)
                    jugador_objetivo.cartas.remove(carta_objetivo)
                    jugador.cartas.append(carta_objetivo)
                    jugador_objetivo.cartas.append(carta_jugador)
                else:
                    print(f"{jugador_objetivo.nombre} no tiene cartas para intercambiar.")

            elif idx_objetivo == -1 and self.cartas_mesa:
                # Intercambiar con la mesa
                print("\nSelecciona una carta de la mesa para intercambiar:")
                for idx, carta in enumerate(self.cartas_mesa):
                    print(f"{idx + 1}. {carta}")

                idx_carta_mesa = int(input("Seleccione el número de la carta (0 para cancelar): ")) - 1

                if 0 <= idx_carta_mesa < len(self.cartas_mesa):
                    carta_mesa = self.cartas_mesa[idx_carta_mesa]

                    # Verificar si el jugador tiene cartas
                    if not jugador.cartas:
                        print(f"{jugador.nombre} no tiene cartas para intercambiar.")
                        return

                    carta_jugador = random.choice(jugador.cartas)
                    print(f"{jugador.nombre} intercambia {carta_jugador} con la carta de la mesa {carta_mesa}.")

                    # Realizar el intercambio
                    jugador.cartas.remove(carta_jugador)
                    jugador.cartas.append(carta_mesa)
                    self.cartas_mesa[idx_carta_mesa] = carta_jugador
                else:
                    print("No se realizó ningún intercambio.")
            else:
                print("Selección no válida.")

        except ValueError:
            print("Entrada no válida. Por favor, introduce un número.")
        except IndexError:
            print("Error: No hay cartas disponibles para intercambiar. Intenta de nuevo.")

    def usar_habilidad(self, jugador):
        if not jugador.cartas and not self.cartas_mesa:
            print(f"{jugador.nombre} no tiene cartas para usar habilidades.")
            return

        cartas_disponibles = [carta for j in self.jugadores for carta in j.cartas] + self.cartas_mesa
        print("Habilidades disponibles:")
        for idx, carta in enumerate(cartas_disponibles):
            print(f"{idx + 1}. {carta}")

        try:
            eleccion_habilidad = int(input("Seleccione un número para declarar la habilidad que quiere usar: ")) - 1
            if 0 <= eleccion_habilidad < len(cartas_disponibles):
                carta_seleccionada = cartas_disponibles[eleccion_habilidad]
                habilidad_declarada = carta_seleccionada.habilidad

                if carta_seleccionada.nombre == "El Campesino":
                    self.campesinos_revelados += 1
                    if self.campesinos_revelados >= 2:
                        print("¡Dos Campesinos han sido revelados!")
                        for j in self.jugadores:
                            if any(carta.nombre == "El Campesino" for carta in j.cartas):
                                j.oro += 2
                                print(f"{j.nombre} recibe 2 monedas de oro adicionales.")

                # Preguntar a otros jugadores si quieren refutar
                refutadores = []
                for otro_jugador in self.jugadores:
                    if otro_jugador != jugador and otro_jugador.esta_vivo():
                        refutar = input(
                            f"{otro_jugador.nombre}, ¿quieres refutar la habilidad de {carta_seleccionada}? (sí/no): "
                        ).strip().lower()
                        if refutar in ["si", "sí", "yes", "y"]:
                            refutadores.append(otro_jugador)
                            print(f"{otro_jugador.nombre} ha decidido refutar.")

                # Verificar si la habilidad declarada es válida
                habilidad_en_posesion = any(carta.habilidad == habilidad_declarada for carta in jugador.cartas)

                if refutadores:
                    if habilidad_en_posesion:
                        print(f"{jugador.nombre} estaba usando la habilidad correcta. Los que refutaron pierden 1 oro.")
                        for refutador in refutadores:
                            refutador.oro = max(0, refutador.oro - 1)
                            print(f"{refutador.nombre} pierde 1 oro. (Oro actual: {refutador.oro})")
                        carta_seleccionada.usar_habilidad(jugador, self.jugadores, self.corte)
                    else:
                        print(
                            f"{jugador.nombre} intentó usar una habilidad que no está en su poder. Debe pagar 1 oro a la corte."
                        )
                        jugador.oro -= 1
                        self.corte.depositar(1)
                else:
                    print(f"Nadie ha refutado. {jugador.nombre} usa la habilidad {carta_seleccionada}.")
                    carta_seleccionada.usar_habilidad(jugador, self.jugadores, self.corte)
            else:
                print("Selección no válida.")
        except (ValueError, IndexError):
            print("Entrada no válida o error al usar habilidad. Intenta de nuevo.")

    # Métodos estáticos para habilidades (sin cambios significativos)
    @staticmethod
    def habilidad_juez(jugador, jugadores, corte):
        cantidad = corte.retirar()
        jugador.oro += cantidad
        print(f"{jugador.nombre} recibe {cantidad} monedas de oro del Palacio de Justicia.")

    @staticmethod
    def habilidad_obispo(jugador, jugadores, corte):
        jugador_mas_rico = max(jugadores, key=lambda j: j.oro)
        cantidad = 2
        print(f"{jugador.nombre} toma {cantidad} monedas de {jugador_mas_rico.nombre}.")
        jugador_mas_rico.oro -= cantidad
        jugador.oro += cantidad

    @staticmethod
    def habilidad_rey(jugador, jugadores, corte):
        jugador.oro += 3
        print(f"{jugador.nombre} recibe 3 monedas del banco.")

    @staticmethod
    def habilidad_reina(jugador, jugadores, corte):
        jugador.oro += 2
        print(f"{jugador.nombre} recibe 2 monedas del banco.")

    @staticmethod
    def habilidad_ladron(jugador, jugadores, corte):
        jugadores_adyacentes = [j for j in jugadores if j != jugador and j.esta_vivo()]
        if len(jugadores_adyacentes) >= 2:
            objetivo1, objetivo2 = random.sample(jugadores_adyacentes, 2)
            print(f"{jugador.nombre} roba 1 moneda de {objetivo1.nombre} y de {objetivo2.nombre}.")
            objetivo1.oro -= 1
            objetivo2.oro -= 1
            jugador.oro += 2

    @staticmethod
    def habilidad_bufon(jugador, jugadores, corte):
        print(f"{jugador.nombre} usa la habilidad del Bufón.")
        jugador.oro += 1
        print(f"{jugador.nombre} recibe 1 moneda de oro.")
        intercambiar = input("¿Deseas intercambiar las cartas de dos jugadores? (sí/no): ").strip().lower()
        if intercambiar in ["si", "sí", "yes", "y"]:
            print("Selecciona dos jugadores para intercambiar sus cartas:")
            for idx, j in enumerate(jugadores):
                if j != jugador and j.esta_vivo():
                    print(f"{idx + 1}. {j.nombre}")
            idx_jugador1 = int(input("Selecciona el número del primer jugador: ")) - 1
            if 0 <= idx_jugador1 < len(jugadores) and jugadores[idx_jugador1] != jugador and jugadores[
                idx_jugador1].esta_vivo():
                jugador1 = jugadores[idx_jugador1]
            else:
                print("Selección no válida. No se realizará ningún intercambio.")
                return
            idx_jugador2 = int(input("Selecciona el número del segundo jugador: ")) - 1
            if 0 <= idx_jugador2 < len(jugadores) and jugadores[idx_jugador2] != jugador and jugadores[
                idx_jugador2].esta_vivo():
                jugador2 = jugadores[idx_jugador2]
            else:
                print("Selección no válida. No se realizará ningún intercambio.")
                return
            jugador1.cartas, jugador2.cartas = jugador2.cartas, jugador1.cartas
            print(f"Se han intercambiado las cartas de {jugador1.nombre} y {jugador2.nombre}.")
        else:
            print("No se intercambiaron cartas.")

    @staticmethod
    def habilidad_bruja(jugador, jugadores, corte):
        print(f"{jugador.nombre} usa la habilidad de la Bruja.")
        print("Selecciona un jugador para intercambiar fortunas:")
        for idx, j in enumerate(jugadores):
            if j != jugador and j.esta_vivo():
                print(f"{idx + 1}. {j.nombre} (Oro: {j.oro})")
        idx_objetivo = int(input("Selecciona el número del jugador: ")) - 1
        if 0 <= idx_objetivo < len(jugadores) and jugadores[idx_objetivo] != jugador and jugadores[
            idx_objetivo].esta_vivo():
            jugador_objetivo = jugadores[idx_objetivo]
            jugador.oro, jugador_objetivo.oro = jugador_objetivo.oro, jugador.oro
            print(f"{jugador.nombre} y {jugador_objetivo.nombre} han intercambiado sus fortunas.")
            print(f"{jugador.nombre} ahora tiene {jugador.oro} monedas de oro.")
            print(f"{jugador_objetivo.nombre} ahora tiene {jugador_objetivo.oro} monedas de oro.")
        else:
            print("Selección no válida. No se realizará ningún intercambio.")

    @staticmethod
    def habilidad_espia(jugador, jugadores, corte):
        print(f"{jugador.nombre} usa la habilidad del Espía.")
        print(f"Tu carta: {jugador.cartas[0]}")
        print("Selecciona un jugador para ver su carta:")
        for idx, j in enumerate(jugadores):
            if j != jugador and j.esta_vivo():
                print(f"{idx + 1}. {j.nombre}")
        idx_objetivo = int(input("Selecciona el número del jugador: ")) - 1
        if 0 <= idx_objetivo < len(jugadores) and jugadores[idx_objetivo] != jugador and jugadores[
            idx_objetivo].esta_vivo():
            jugador_objetivo = jugadores[idx_objetivo]
            carta_objetivo = jugador_objetivo.cartas[0]
            print(f"La carta de {jugador_objetivo.nombre} es: {carta_objetivo}")
            intercambiar = input("¿Deseas intercambiar las cartas? (sí/no): ").strip().lower()
            if intercambiar in ["si", "sí", "yes", "y"]:
                jugador.cartas[0], jugador_objetivo.cartas[0] = jugador_objetivo.cartas[0], jugador.cartas[0]
                print(f"Se han intercambiado las cartas de {jugador.nombre} y {jugador_objetivo.nombre}.")
            else:
                print("No se realizará ninguna acción.")
        else:
            print("Selección no válida. No se realizará ninguna acción.")

    @staticmethod
    def habilidad_inquisidor(jugador, jugadores, corte):
        print(f"{jugador.nombre} usa la habilidad del Inquisidor.")
        print("Selecciona un jugador para interrogarlo:")
        for idx, j in enumerate(jugadores):
            if j != jugador and j.esta_vivo():
                print(f"{idx + 1}. {j.nombre}")
        idx_objetivo = int(input("Selecciona el número del jugador: ")) - 1
        if 0 <= idx_objetivo < len(jugadores) and jugadores[idx_objetivo] != jugador and jugadores[
            idx_objetivo].esta_vivo():
            jugador_objetivo = jugadores[idx_objetivo]
            print(f"{jugador_objetivo.nombre}, adivina el personaje de tu carta.")
            print("Opciones disponibles:")
            opciones = [
                "El Juez", "El Obispo", "El Rey", "La Reina", "El Bufón",
                "El Ladrón", "La Bruja", "El Espía", "El Campesino",
                "El Tramposo", "El Inquisidor", "La Viuda"
            ]
            for i, opcion in enumerate(opciones, start=1):
                print(f"{i}. {opcion}")
            eleccion = int(input("Selecciona el número del personaje que crees que eres: ")) - 1
            if 0 <= eleccion < len(opciones):
                guess = opciones[eleccion]
                print(f"{jugador_objetivo.nombre} cree que es {guess}.")
                if any(carta.nombre == guess for carta in jugador_objetivo.cartas):
                    print(f"¡Correcto! {jugador_objetivo.nombre} ha adivinado correctamente su personaje.")
                else:
                    print(f"Incorrecto. {jugador_objetivo.nombre} debe pagar 4 monedas de oro a {jugador.nombre}.")
                    cantidad = 4
                    if jugador_objetivo.oro >= cantidad:
                        jugador_objetivo.oro -= cantidad
                        jugador.oro += cantidad
                        print(f"{jugador_objetivo.nombre} paga {cantidad} monedas a {jugador.nombre}.")
                    else:
                        print(f"{jugador_objetivo.nombre} no tiene suficiente oro para pagar.")
            else:
                print("Selección no válida. No se realizará ninguna acción.")
        else:
            print("Selección no válida. No se realizará ninguna acción.")

    @staticmethod
    def habilidad_campesino(jugador, jugadores, corte):
        print(f"{jugador.nombre} usa la habilidad del Campesino.")
        jugador.oro += 1
        print(f"{jugador.nombre} recibe 1 moneda de oro.")
        cartas_reveladas = [carta for j in jugadores for carta in j.cartas] + juego.cartas_mesa
        campesinos_revelados = [carta for carta in cartas_reveladas if carta.nombre == "El Campesino"]
        if len(campesinos_revelados) >= 2:
            print("¡Dos Campesinos han sido revelados!")
            for j in jugadores:
                if any(carta.nombre == "El Campesino" for carta in j.cartas):
                    j.oro += 2
                    print(f"{j.nombre} recibe 2 monedas de oro adicionales.")

    @staticmethod
    def habilidad_tramposo(jugador, jugadores, corte):
        if jugador.oro >= 10:
            print(f"{jugador.nombre} ha ganado el juego como tramposo!")
            return True
        else:
            print(f"{jugador.nombre} no puede ganar aún.")
            return False

    @staticmethod
    def habilidad_viuda(jugador, jugadores, corte):
        a_pagar = 10 - jugador.oro
        if a_pagar > 0:
            jugador.oro += a_pagar
            print(f"{jugador.nombre} recibe {a_pagar} monedas del banco, llevando su fortuna a 10 monedas en total.")
        else:
            print(f"{jugador.nombre} ya tiene suficiente oro.")


if __name__ == "__main__":
    juego = Juego()
    juego.agregar_jugadores()
    juego.iniciar_juego()
