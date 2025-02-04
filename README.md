![image](https://github.com/user-attachments/assets/77cb59e1-a55f-41ec-8252-b7d3e3e8e37c)

# 🎴 Mascarade (Estructura de Datos)

**Mascarade** es un emocionante juego de engaño y deducción para 2 a 13 jugadores, diseñado por Bruno Faidutti. En este proyecto, se implementa el juego utilizando estructuras de datos en Python para manejar jugadores, cartas y las reglas del juego.


## 📋 Estructura de Datos Utilizada

### Listas
- **`self.jugadores`**:  
  - Guarda a los jugadores como objetos de la clase `Jugador`.  
  - Permite acceder a los jugadores por índice, agregar o eliminar jugadores fácilmente.  
  - Se usa para gestionar los turnos recorriendo la lista uno por uno.

- **`self.mazo`**:  
  - Representa el mazo de cartas con objetos de la clase `Carta`.  
  - Usa `pop()` para simular el robo de cartas, siguiendo una estructura de pila (LIFO).  
  - Se puede mezclar con `random.shuffle()` para añadir aleatoriedad.

- **`self.cartas_mesa`**:  
  - Contiene las cartas disponibles en la mesa.  
  - Permite agregar o quitar cartas según las reglas del juego.

- **`jugador.cartas`**:  
  - Cada jugador tiene sus propias cartas, que pueden intercambiarse o usarse dependiendo de las habilidades de los personajes.

### Clases y Objetos
- **`Carta`**:  
  - Representa una carta con nombre y habilidad.  
  - Encapsula sus datos y funciones, como `usar_habilidad()`.  
  - Facilita la creación de muchas cartas distintas gracias a su reutilización.

- **`Jugador`**:  
  - Gestiona los datos del jugador (nombre, oro, cartas).  
  - Encapsula comportamientos como `esta_vivo()` para verificar si un jugador sigue en la partida.

- **`Corte`**:  
  - Representa el banco del juego, donde se acumula oro.  
  - Incluye métodos como `depositar()` y `retirar()` para manejar transacciones.

- **`Juego`**:  
  - Es el cerebro del juego, manejando jugadores, mazo y reglas.  
  - Centraliza toda la lógica del juego en una sola clase.

### Estructuras Implícitas
- **Colas Implícitas (Turnos)**:  
  - Ejemplo: `for jugador in self.jugadores`.  
  - Procesan jugadores en orden, funcionando como una cola sin necesidad de implementarla explícitamente.

- **Pila Implícita (Mazo de Cartas)**:  
  - Ejemplo: `self.mazo.pop()`.  
  - Simula el comportamiento de una pila (LIFO), eliminando el último elemento rápidamente.

- **Tuplas**:  
  - Ejemplo: `zip(nombres, habilidades)`.  
  - Son inmutables y útiles para emparejar datos de manera segura.

- **Diccionarios Implícitos (No usados, pero podrían ser útiles)**:  
  - Permiten búsquedas rápidas si fuera necesario buscar jugadores por nombre.

- **Árboles o Grafos**:  
  - No se usan porque serían demasiado complejos. Las listas y objetos cumplen bien su función.

## 📜 Reglas del Juego

### Objetivo
- Obtener **13 monedas de oro** para ganar.
- Si un jugador pierde todas sus monedas (**quiebra**), la partida termina y gana el jugador más rico.

### Preparación
1. Cada jugador comienza con **6 monedas de oro**.
2. Se reparten **cartas de personaje boca abajo** (una por jugador).
3. Las cartas restantes se colocan en el centro de la mesa, boca arriba, para luego voltearlas boca abajo.
4. El **Palacio de Justicia** y el **Banco** se colocan en el centro.

### Secuencia de Juego
1. **Intercambio de cartas**: Durante los primeros cuatro turnos, los jugadores pueden intercambiar (o no) su carta con otra, sin mirarlas.
2. **Acciones principales**:
   - **Intercambiar tu carta** con otro jugador (o no).
   - **Mirar tu carta** en secreto.
   - **Anunciar tu personaje**: Si nadie protesta, puedes usar el poder del personaje anunciado. Si alguien protesta, todos los involucrados revelan sus cartas:
     - Si aciertas, usas el poder del personaje.
     - Si fallas, pagas una multa al Palacio de Justicia.

### Poderes de los Personajes
Cada personaje tiene un poder único:
- **Juez**: Recoge todas las monedas del Palacio de Justicia.
- **Rey**: Obtiene 3 monedas del Banco.
- **Reina**: Obtiene 2 monedas del Banco.
- **Bruja**: Intercambia toda su fortuna con otro jugador.
- **Ladrón**: Roba una moneda al jugador de su izquierda y derecha.
- **Campesino**: Obtiene 1 moneda del Banco (2 si ambos Campesinos se revelan).

### Fin del Juego
- La partida termina cuando:
  - Un jugador alcanza **13 monedas de oro**.
  - Un jugador queda en **bancarrota** (0 monedas), y gana el jugador más rico.

## 🙏 Créditos

- **Autor del Juego**: Bruno Faidutti  

## 📜 Licencia

Este proyecto está bajo la licencia [MIT](LICENSE). ¡Úsalo como quieras! 🚀
