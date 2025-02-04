# 🎴 Mascarade (Estructura de Datos)

Este proyecto es una implementación de un juego de cartas (Mascarade) en Python. Se usan listas, clases y objetos para manejar jugadores, cartas y las reglas del juego. Además, se aprovechan estructuras como pilas y colas de manera implícita para hacer todo más dinámico.

## 📋 Listas en el Juego

### `self.jugadores`
- **Guarda a los jugadores** como objetos de la clase `Jugador`.
- **Puedes acceder a ellos por índice**, como en una lista normal.
- **Fácil de modificar**: puedes agregar, eliminar o cambiar jugadores sin problema.
- **Se usa para los turnos**, recorriendo la lista uno por uno.

### `self.mazo`
- **Es el mazo de cartas**, con objetos de la clase `Carta`.
- **Puedes sacar cartas con `pop()`**, como si las estuvieras robando.
- **Puedes mezclarlo con `random.shuffle()`**, para que no siempre sea lo mismo.

### `self.cartas_mesa`
- **Son las cartas en juego**, disponibles en la mesa.
- **Puedes agregar o quitar cartas**, dependiendo de las reglas del juego.

### `jugador.cartas`
- **Cada jugador tiene sus propias cartas**.
- **Pueden intercambiarse o usarse** dependiendo de las habilidades que tengan.

## 🏗️ Clases y Objetos

### `Carta`
- **Representa una carta** con nombre y habilidad.
- **Encapsula sus datos y funciones**, como `usar_habilidad()`.
- **Puedes crear muchas cartas distintas**, gracias a su reutilización.

### `Jugador`
- **Cada jugador tiene un nombre, oro y cartas**.
- **Encapsula sus datos y comportamientos**, como `esta_vivo()`.
- **Abstracción**: facilita la lógica del juego sin meterse en detalles.

### `Corte`
- **Es el banco del juego**, donde se acumula oro.
- **Tiene métodos como `depositar()` y `retirar()`** para manejar el oro.

### `Juego`
- **Es el cerebro del juego**, manejando jugadores, mazo y reglas.
- **Encapsula toda la lógica del juego**, haciendo que todo esté centralizado.

## 🔄 Estructuras Implícitas

### 🏆 Colas Implícitas (Turnos)
- **Ejemplo:** `for jugador in self.jugadores`.
- **Funcionan como una cola**, procesando jugadores en orden.
- **Más simple** que implementar una cola explícita.

### 🎴 Pila Implícita (Mazo de cartas)
- **Ejemplo:** `self.mazo.pop()`.
- **Último en entrar, primero en salir (LIFO)**: como en un juego real de cartas.
- **Rápido y eficiente**, porque `pop()` elimina el último elemento sin problema.

### 🎭 Tuplas
- **Ejemplo:** `zip(nombres, habilidades)`.
- **No se pueden cambiar (inmutables)**, lo que las hace seguras.
- **Sencillas y útiles** para emparejar datos.

### 🔍 Diccionarios Implícitos (No usados, pero podrían ser útiles)
- **Hacen búsquedas más rápidas**, si fuera necesario buscar jugadores por nombre.
- **Perfectos para mapear jugadores con sus datos**.

### 🌳 Árboles o Grafos
- **No se usan porque serían demasiado complejos**.
- **Las listas y objetos hacen bien el trabajo**, sin necesidad de estructuras más avanzadas.

---

## 📜 Licencia
Este proyecto está bajo la licencia [MIT](LICENSE). ¡Úsalo como quieras! 🚀
