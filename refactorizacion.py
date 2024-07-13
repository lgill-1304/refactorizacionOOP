import heapq
import random

class Mapa: #se usa para crear metodos y manipular el mapa
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.mapa = [[0 for _ in range(columnas)] for _ in range(filas)]

    def imprimir_mapa(self):
        for fila in self.mapa:
            print(fila)

    def agregar_obstaculos(self, obstaculos):
        for obstaculo in obstaculos:
            if 0 <= obstaculo[0] < self.filas and 0 <= obstaculo[1] < self.columnas:
                self.mapa[obstaculo[0]][obstaculo[1]] = 1

    def quitar_obstaculos(self, obstaculos):
        for obstaculo in obstaculos:
            if 0 <= obstaculo[0] < self.filas and 0 <= obstaculo[1] < self.columnas:
                self.mapa[obstaculo[0]][obstaculo[1]] = 0

    def generar_obstaculos_aleatorios(self, num_obstaculos):
        obstaculos = set()
        while len(obstaculos) < num_obstaculos:
            x = random.randint(0, self.filas - 1)
            y = random.randint(0, self.columnas - 1)
            if self.mapa[x][y] == 0:
                obstaculos.add((x, y))
        return list(obstaculos)
        
    def coordenadas_validas(self, coordenadas):
        return (0 <= coordenadas[0] < self.filas and 
                0 <= coordenadas[1] < self.columnas and 
                self.mapa[coordenadas[0]][coordenadas[1]] == 0)
    
    def mostrar_mapa_con_ruta(self, ruta=[]):
        print('   ', end=' ')
        for col in range(self.columnas):
            print(f'{col:2}', end=' ')
        print()

        for fila in range(self.filas):
            print(f'{fila:2} ', end=' ')

            for col in range(self.columnas):
                if self.mapa[fila][col] == 0:
                    if (fila, col) in ruta:
                        print('\033[1;32m* \033[0m', end=' ')
                    else:
                        print('. ', end=' ')
                else:
                    print('\033[1;31m# \033[0m', end=' ')
            print()  


class Ruta:
    def __init__(self, mapa):
        self.mapa = mapa
        self.direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
    def heuristica(self, pos_actual, pos_final):
        return abs(pos_actual[0] - pos_final[0]) + abs(pos_actual[1] - pos_final[1])

    def encontrar_ruta(self, inicio, fin):
        heap = [(0, inicio)]
        heapq.heapify(heap)
        padres = {inicio: None}
        costos = {inicio: 0}

        while heap:
            costo_actual, nodo_actual = heapq.heappop(heap)
            if nodo_actual == fin:
                break

            for direccion in self.direcciones:
                vecino = (nodo_actual[0] + direccion[0], nodo_actual[1] + direccion[1])
                if 0 <= vecino[0] < self.mapa.filas and 0 <= vecino[1] < self.mapa.columnas:
                    nuevo_costo = costo_actual + 1
                    if self.mapa.mapa[vecino[0]][vecino[1]] != 1 and (vecino not in costos or nuevo_costo < costos[vecino]):
                        costos[vecino] = nuevo_costo
                        prioridad = nuevo_costo + self.heuristica(vecino, fin)
                        heapq.heappush(heap, (prioridad, vecino))
                        padres[vecino] = nodo_actual

        ruta = []
        nodo = fin
        while nodo is not None:
            ruta.append(nodo)
            nodo = padres[nodo]
        ruta.reverse()

        return ruta

if __name__ == "__main__":
    num_filas, num_columnas = 12, 12
    mapa = Mapa(num_filas, num_columnas)

    print("\nMapa original")
    mapa.imprimir_mapa()

    obstaculos_quitar = []  # Inicializar lista para quitar obstáculos

    modo = input("Selecciona el modo de ingreso de obstáculos (1: Manual, 2: Aleatorio,): ")

    if modo == '1':
        obstaculos = []
        while True:
            entrada = input("Ingresa las coordenadas de un obstáculo (formato x,y) o 'fin' para terminar: ")
            if entrada.lower() == 'fin':
                break
            x, y = map(int, entrada.split(','))
            obstaculos.append((x, y))
    elif modo == '2':
        num_obstaculos = int(input("Ingresa el número de obstáculos aleatorios: "))
        obstaculos = mapa.generar_obstaculos_aleatorios(num_obstaculos)
    
        mapa.agregar_obstaculos(obstaculos)
    
    print("\nMapa con obstáculos: ")
    mapa.mostrar_mapa_con_ruta()

    # Bucle adicional para quitar obstáculos según lo solicite el usuario
    while True:
        quitar_mas = input("¿Quieres quitar algún obstáculo más? (s/n): ").lower()
        if quitar_mas == 's':
            obstaculos_quitar = []
            while True:
                entrada = input("Ingrese las coordenadas para quitar obstáculos (formato x,y) o 'fin' para terminar: ")
                if entrada.lower() == 'fin':
                    break
                x, y = map(int, entrada.split(','))
                obstaculos_quitar.append((x, y))
            mapa.quitar_obstaculos(obstaculos_quitar)
            print("\nMapa actualizado:")
            mapa.mostrar_mapa_con_ruta()
        else:
            break

    while True:
        inicio = tuple(map(int, input("Ingresa coordenadas de inicio (formato x,y): ").split(',')))
        if mapa.coordenadas_validas(inicio):
            break
        print("Coordenadas no son válidas o es un obstáculo. Intenta de nuevo.")

    while True:
        fin = tuple(map(int, input("Ingresa coordenadas de destino (formato x,y): ").split(',')))
        if mapa.coordenadas_validas(fin):
            break
        print("Coordenadas no válidas o es un obstáculo. Intenta de nuevo.")

    objetivo_ruta = Ruta(mapa)
    ruta_encontrada = objetivo_ruta.encontrar_ruta(inicio, fin)

    print("\nMapa con la ruta más corta")
    mapa.mostrar_mapa_con_ruta(ruta_encontrada)


