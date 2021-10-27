from random import randint

class TurnoError(Exception):
    pass


class TablaPuntosError(Exception):
    pass


class Ganaste(Exception):
    pass


class ErrorInputs(Exception):
    pass


def calcular_repetidos(dados):
    repetidos = [0] * 6
    for dado in dados:
        index = dado - 1
        repetidos[index] += 1

    return repetidos



def buscar_repetido(dados, repetidos, cantidad_repetidos): #dados, cantidad de repetidos por numeros, cantidad que quiero
    encontre = False
    for repetido in repetidos:
        if repetido >= cantidad_repetidos:
            encontre = True
    return encontre


def calcular_puntos(numero_lanzamiento, dados, juego):
    puntos = 0
    if juego == "escalera":
        dados.sort()
        if dados == [1, 2, 3, 4, 5] or dados == [2, 3, 4, 5, 6]:
            puntos = 20
            if numero_lanzamiento == 1:
                puntos += 5


    elif juego == "full":
        encontre1 = False
        encontre2 = False
        for i in calcular_repetidos(dados):
            if i == 3:
                encontre1 = True
            if i == 2:
                encontre2 = True

        if encontre1 and encontre2:
            puntos = 30
            if numero_lanzamiento == 1:
                puntos += 5


    elif juego == "poker":
        repetidos = calcular_repetidos(dados)
        if buscar_repetido(dados, repetidos, 4):
            puntos = 40
            if numero_lanzamiento == 1:
                puntos += 5

    elif juego == "generala":
        repetidos = calcular_repetidos(dados)
        if buscar_repetido(dados, repetidos, 5):
            puntos = 50
            if numero_lanzamiento == 1:
                raise Ganaste(("\n\n+" + "-"*66 + "+\n|{:^66}|\n" + "+" + "-"*66 + "+\n").format("Ganaste con Generala servida!!!"))

    elif juego == "generala_doble":
        repetidos = calcular_repetidos(dados)
        if buscar_repetido(dados, repetidos, 5):
            puntos = 100
            if numero_lanzamiento == 1:
                raise Ganaste(("\n\n+" + "-"*66 + "+\n|{:^66}|\n" + "+" + "-"*66 + "+\n").format("Ganaste con Generala doble servida!!! Increible!!!"))

    elif juego == "1" or juego == "2" or juego == "3" or juego == "4" or juego == "5" or juego == "6":
        for dado in dados:
            if juego == str(dado):
                puntos += dado
    else:
        raise ErrorInputs(("\n\n+" + "-"*66 + "+\n|{:^66}|\n" + "+" + "-"*66 + "+\n").format("Jugada NO valida"))

    return puntos


def calcular_final(tabla):
    puntos=[]
    for i in tabla:
        puntos.append(sum(i.values()))
    return puntos


class Dados:
    def __init__(self, cantidad_dados):
        self._valores = [randint(1, 6) for _ in range(cantidad_dados)]

    @property
    def cantidad(self):
        return len(self._valores)

    @property
    def valores(self):
        return self._valores


class Turno:
    def __init__(self):
        self.numero_lanzamiento = 1
        self.dados_lanzados = Dados(5)
        self.dados_seguir = Dados(0)

    def guardar_dados(self, indices):
        todos_dados = self.dados_seguir.valores + self.dados_lanzados.valores
        self.dados_seguir = Dados(0)
        for i in indices:
            self.dados_seguir.valores.append(todos_dados[i])
        self.siguiente_turno()

    def siguiente_turno(self):
        if(self.numero_lanzamiento >= 3):
            raise TurnoError(("\n\n+" + "-"*66 + "+\n|{:^66}|\n" + "+" + "-"*66 + "+\n").format("Límite de lanzamientos alcanzado"))

        self.numero_lanzamiento += 1
        self.dados_lanzados = Dados(5 - self.dados_seguir.cantidad)

    @property
    def dados_finales(self):
        return self.dados_seguir.valores + self.dados_lanzados.valores


class TablaPuntos:
    def __init__(self, cantidad_jugadores):
        self.cantidad_jugadores = cantidad_jugadores
        self._tabla = [  # lista/jugador
            {  # diccionario/jugada
                "1": None,
                '2': None,
                '3': None,
                '4': None,
                '5': None,
                '6': None,
                'escalera': None,
                'full': None,
                'poker': None,
                'generala': None,
                'generala_doble': None,
            }
            for _ in range(cantidad_jugadores)
        ]

    @property
    def estado_tabla(self):
        for jugada in self._tabla[-1].values():
            if jugada is None:
                return False, 0
        return True, calcular_final(self._tabla) # Significa que la tabla del ultimo jugador esta llena

    def anotar(self, jugador, jugada, numero_lanzamiento, dados):
        jugadas_posibles = ["1",
                '2',
                '3',
                '4',
                '5',
                '6',
                'escalera',
                'full',
                'poker',
                'generala',
                'generala_doble',
            ]

        if not(jugada in jugadas_posibles):
            raise ErrorInputs(("\n\n+" + "-"*66 + "+\n|{:^66}|\n" + "+" + "-"*66 + "+\n").format("Jugada NO valida"))


        if jugada == "generala_doble" and self._tabla[jugador]["generala"] is None:     # para anotar la generala doble
            puntos = calcular_puntos(numero_lanzamiento, dados, "generala")

            if puntos == 0:    # Cuando quiero tachar
                self._tabla[jugador][jugada] = puntos

            else:        # Evitar anotar 100 en doble sin la simple 
                raise TablaPuntosError(("\n\n+" + "-"*66 + "+\n|{:^66}|\n" + "+" + "-"*66 + "+\n").format("No tenes la generala simple"))


        elif jugada == "generala" and self._tabla[jugador]["generala_doble"] is None:
            puntos = calcular_puntos(numero_lanzamiento, dados, "generala")

            if puntos == 0:      # No tachar la simple sin tener tachada la doble
                raise TablaPuntosError(("\n\n+" + "-"*66 + "+\n|{:^66}|\n" + "+" + "-"*66 + "+\n").format("No podes tachar la simple sin tachar la doble!!"))

            else:     # Anotar la simple
                self._tabla[jugador][jugada] = puntos

                
    
        elif self._tabla[jugador][jugada] is None:    # Anotar
            puntos = calcular_puntos(numero_lanzamiento, dados, jugada)
            self._tabla[jugador][jugada] = puntos
        else:
            raise TablaPuntosError(("\n\n+" + "-"*66 + "+\n|{:^66}|\n" + "+" + "-"*66 + "+\n").format('Jugada ya anotada!'))


class Generala:
    def __init__(self, cantidad_jugadores):
        self.cantidad_jugadores = cantidad_jugadores
        self.esta_jugado = True
        self.jugador_esta_jugando = True
        self.jugador_actual = 0  
        self.turno_actual = Turno()
        self.tabla_puntos = TablaPuntos(cantidad_jugadores)
        self.puntos = 0

    def siguiente_jugador(self):
        self.jugador_actual += 1
        self.jugador_actual = self.jugador_actual % self.cantidad_jugadores
        self.turno_actual = Turno()
        self.jugador_esta_jugando = True


    def anotar(self, jugada):
        try:
            jugada = jugada.lower()
            self.tabla_puntos.anotar(
                self.jugador_actual,
                jugada,
                self.turno_actual.numero_lanzamiento,
                self.turno_actual.dados_finales,
            )

            estado, self.puntos = self.tabla_puntos.estado_tabla
            
            if estado: # Aca recibe los puntos
                self.esta_jugado = False
                maximo = max(self.puntos)

                while maximo in self.puntos:
                    self.puntos[self.puntos.index(maximo)] = str(self.puntos[self.puntos.index(maximo)]) + " --Ganador--"

            else:
                self.siguiente_jugador()
            return None

        except TablaPuntosError as e:
            return str(e)

        except Ganaste as e:
            self.esta_jugado = False
            return str(e)

        except ErrorInputs as e:
            return str(e)

    def dados_finales(self, dados_seguir):
        dados_seguir = dados_seguir.lower()
        try:
            dados_seguir
            if dados_seguir == "anotar" :
                self.jugador_esta_jugando = False
            else:
                if dados_seguir == "":
                    list_int_dados_seguir = []
                else:
                    list_dados_seguir = dados_seguir.split(sep=',')
                    list_int_dados_seguir = [(int(dado)-1) for dado in list_dados_seguir]
                self.turno_actual.guardar_dados(list_int_dados_seguir)
                if self.turno_actual.numero_lanzamiento == 3:
                    self.jugador_esta_jugando = False
        except:
            return("|+++++++{:^24}+++++++|".format('Indices no validos'))


def imprimir_tabla(tabla, jugador=None): # juego.tabla_puntos._tabla; False=imprimir a todos los jugadores
    tabla_limpia = [""] * 11
    jugadores = ""
    n = 0

    if jugador is None: # Todos los jugadores
        
        for i in range(len(tabla)): #cada jugador
            jugadores += str("|{:^24}| ".format("Jugador " + str(i+1)))

            for k in tabla[i]: # Cada jugada
                m = n % 11
                tabla_limpia[m] += "|{:<15}:{:>8}| ".format(str(k), str(tabla[i][k]))
                n += 1
    
    else: # Jugador actual
        jugadores += str("|{:^24}| ".format("Jugador " + str(jugador+1)))
        for k in tabla[jugador]:
            m = n % 11
            tabla_limpia[m] += "|{:<15}:{:>8}| ".format(str(k), str(tabla[jugador][k]))
            n += 1

    puntos = ""  
    for f in tabla_limpia:
        puntos += str(f) + "\n"
    return(jugadores + "\n" + puntos)


def imprimir_dados(lista_dados):
    dados=""
    for i in lista_dados:
        dados += str(i) + " "
    return dados


def imprimir_puntos(lista_puntos):
    a=""
    for i in lista_puntos:
        a += "|{:^24}| ".format(i)
    return a


def main():
    while True:
        try:
            cantidad_jugadores = int(input('\nCantidad jugadores: '))
            juego = Generala(cantidad_jugadores)
            print(imprimir_tabla(juego.tabla_puntos._tabla))
            while juego.esta_jugado:

                while juego.jugador_esta_jugando:
                    print('Jugador actual: {}'.format(juego.jugador_actual+1))
                    print("Tiro: {}".format(juego.turno_actual.numero_lanzamiento))
                    print("Indices:     1 2 3 4 5")
                    print("Valores:    ", imprimir_dados(juego.turno_actual.dados_finales))
                    print(juego.dados_finales(input('\nElija los indices (1 al 5) de los dados con los que quiere seguir o escriba "anotar": ')))


                print('Jugador actual: {}'.format(juego.jugador_actual+1))
                print("Tiro: {}".format(juego.turno_actual.numero_lanzamiento))
                print("Indices:     1 2 3 4 5")
                print("Valores:    ", imprimir_dados(juego.turno_actual.dados_finales))
                print(juego.anotar(input("¿Que jugada quiere anotar? ")))
                print(imprimir_tabla(juego.tabla_puntos._tabla))

            print(imprimir_puntos(juego.puntos))
            exit()


        except ValueError:
            print("|+++++++{:^24}+++++++|".format("Valor NO valido"))
    
if __name__ == '__main__':
    main()

