import unittest
from generala_poo import (
    Ganaste,
    Generala,
    TablaPuntosError,
    TurnoError,
    ErrorInputs,
    calcular_repetidos,
    calcular_puntos,
    Turno,
    TablaPuntos,
)


class TurnoTest(unittest.TestCase): #15

    def test_tirada_1(self):
        turno = Turno()
        self.assertEqual(turno.numero_lanzamiento, 1)

    def test_tirada_2(self):
        turno = Turno()
        turno.siguiente_turno()
        self.assertEqual(turno.numero_lanzamiento, 2)

    def test_tirada_3(self):
        turno = Turno()
        turno.siguiente_turno()
        turno.siguiente_turno()
        self.assertEqual(turno.numero_lanzamiento, 3)

    def test_tirada_4(self):
        turno = Turno()
        turno.siguiente_turno()
        turno.siguiente_turno()
        with self.assertRaises(TurnoError):
            turno.siguiente_turno()     # No puede haber un 4to turno
        self.assertEqual(turno.numero_lanzamiento, 3)   # Verifico que el numero de lanzamiento haya quedado en 3

    def test_cant_dados(self):
        turno = Turno()
        self.assertEqual(turno.dados_lanzados.cantidad, 5)
        self.assertEqual(turno.dados_seguir.cantidad, 0)
        self.assertEqual(len(turno.dados_finales), 5)

    def test_can_dados_turno2_1dado(self):
        turno = Turno()
        turno.guardar_dados([3])  # Los que NO vamos a tirar de nuevos (Guardamos uno)
        self.assertEqual(turno.dados_seguir.cantidad, 1)
        self.assertEqual(turno.dados_lanzados.cantidad, 4)
        self.assertEqual(len(turno.dados_finales), 5)

    def test_can_dados_turno2_2dado(self):
        turno = Turno()
        turno.guardar_dados([3, 1])  
        self.assertEqual(turno.dados_seguir.cantidad, 2)
        self.assertEqual(turno.dados_lanzados.cantidad, 3)
        self.assertEqual(len(turno.dados_finales), 5)

    def test_can_dados_turno2_3dado(self):
        turno = Turno()
        turno.guardar_dados([3, 1, 4])  
        self.assertEqual(turno.dados_seguir.cantidad, 3)
        self.assertEqual(turno.dados_lanzados.cantidad, 2)
        self.assertEqual(len(turno.dados_finales), 5)

    def test_can_dados_turno2_4dado(self):
        turno = Turno()
        turno.guardar_dados([0, 1, 2, 3])
        self.assertEqual(turno.dados_seguir.cantidad, 4)
        self.assertEqual(turno.dados_lanzados.cantidad, 1)
        self.assertEqual(len(turno.dados_finales), 5)

    def test_can_dados_turno2_5dado(self):
        turno = Turno()
        turno.guardar_dados([0, 1, 2, 3, 4])
        self.assertEqual(turno.dados_seguir.cantidad, 5)
        self.assertEqual(turno.dados_lanzados.cantidad, 0)
        self.assertEqual(len(turno.dados_finales), 5)

    def test_can_dados_turno3_2dados_en_distinto_turnos(self):
        turno = Turno()
        turno.guardar_dados([3]) 
        turno.guardar_dados([4, 2]) 
        self.assertEqual(turno.dados_seguir.cantidad, 2)
        self.assertEqual(turno.dados_lanzados.cantidad, 3)
        self.assertEqual(len(turno.dados_finales), 5)

    def test_can_dados_turno3_5dados_en_distinto_turnos(self):
        turno = Turno()
        turno.guardar_dados([3, 4]) 
        turno.guardar_dados([0, 1, 2, 3, 4]) 
        self.assertEqual(turno.dados_seguir.cantidad, 5)
        self.assertEqual(turno.dados_lanzados.cantidad, 0)
        self.assertEqual(len(turno.dados_finales), 5)

    # que no cambien los dados que se eligieron: 
    def test_valor_1dado_seguir(self):
        turno = Turno()
        turno.dados_lanzados._valores = [1, 3, 5, 2, 4]
        turno.guardar_dados([0]) 
        self.assertEqual(turno.dados_seguir.valores, [1])

    def test_valor_4dados_seguir(self):
        turno = Turno()
        turno.dados_lanzados._valores = [6, 6, 6, 6, 1]
        turno.guardar_dados([0, 1, 2, 3]) 
        self.assertEqual(turno.dados_seguir.valores, [6, 6, 6, 6])

    # no elegir dados a seguir
    def test_valor_0dados_seguir(self):
        turno = Turno()
        turno.dados_lanzados._valores = [6, 5, 6, 6, 1]
        turno.guardar_dados([]) 
        self.assertEqual(turno.dados_seguir.valores, [])


class TablaPuntosTest(unittest.TestCase): #24

    # anotar 2 veces una misma jugada en el mismo jugador
    def test_anotar_2veces_lo_mismo(self):
        tabla = TablaPuntos(2)
        jugador = 0
        jugada = 'poker'
        numero_lanzamiento = 1
        dados = [1, 1, 1, 1, 1]
        tabla.anotar(jugador, jugada, numero_lanzamiento, dados)
        self.assertEqual(tabla._tabla[0]['poker'], 45)
        dados = [2, 1, 1, 1, 1]
        with self.assertRaises(TablaPuntosError):
            tabla.anotar(jugador, jugada, numero_lanzamiento, dados)
        self.assertEqual(tabla._tabla[0]['poker'], 45)

    # anotar cada tipo de jugada
    def test_jugada_1(self):
        tabla = TablaPuntos(2)  
        tabla.anotar(0, "1", 2, [1, 1, 2, 1, 5])
        self.assertEqual(tabla._tabla[0]["1"], 3)
 
    def test_jugada_2(self):
        tabla = TablaPuntos(2)  
        tabla.anotar(0, "2", 2, [1, 1, 2, 1, 5])
        self.assertEqual(tabla._tabla[0]["2"], 2)

    def test_jugada_3(self):
        tabla = TablaPuntos(2)  
        tabla.anotar(0, "3", 2, [1, 1, 2, 1, 5])
        self.assertEqual(tabla._tabla[0]["3"], 0)

    def test_jugada_4(self):
        tabla = TablaPuntos(2)  
        tabla.anotar(0, "4", 2, [1, 1, 2, 1, 5])
        self.assertEqual(tabla._tabla[0]["4"], 0)
 
    def test_jugada_5(self):
        tabla = TablaPuntos(2)  
        tabla.anotar(0, "5", 2, [1, 1, 2, 1, 5])
        self.assertEqual(tabla._tabla[0]["5"], 5)

    def test_jugada_6(self):
        tabla = TablaPuntos(2)  
        tabla.anotar(0, "6", 2, [1, 6, 6, 1, 5])
        self.assertEqual(tabla._tabla[0]["6"], 12)

    # escalera
    def test_jugada_escalera_mal(self):
        tabla = TablaPuntos(2)  
        tabla.anotar(0, "escalera", 2, [1, 2, 4, 3, 1])
        self.assertEqual(tabla._tabla[0]["escalera"], 0)

    def test_jugada_escalera_bien(self):
        tabla = TablaPuntos(2)  
        tabla.anotar(0, "escalera", 2, [1, 2, 4, 3, 5])
        self.assertEqual(tabla._tabla[0]["escalera"], 20)

    def test_jugada_escalera_servida(self):
        tabla = TablaPuntos(2)  
        tabla.anotar(0, "escalera", 1, [1, 2, 4, 3, 5])
        self.assertEqual(tabla._tabla[0]["escalera"], 25)

    # full
    def test_jugada_full_mal(self):
        tabla = TablaPuntos(2)  
        tabla.anotar(0, "full", 2, [1, 1, 2, 4, 5])
        self.assertEqual(tabla._tabla[0]["full"], 0)

    def test_jugada_full_bien(self):
        tabla = TablaPuntos(2)  
        tabla.anotar(0, "full", 2, [1, 1, 5, 1, 5])
        self.assertEqual(tabla._tabla[0]["full"], 30)
 
    def test_jugada_full_servida(self):
        tabla = TablaPuntos(2)  
        tabla.anotar(0, "full", 1, [1, 1, 5, 1, 5])
        self.assertEqual(tabla._tabla[0]["full"], 35)

    # pocker
    def test_jugada_poker_mal(self):
        tabla = TablaPuntos(2)  
        tabla.anotar(0, "poker", 2, [1, 1, 1, 5, 5])
        self.assertEqual(tabla._tabla[0]["poker"], 0)

    def test_jugada_poker_bien(self):
        tabla = TablaPuntos(2)  
        tabla.anotar(0, "poker", 2, [1, 1, 1, 1, 5])
        self.assertEqual(tabla._tabla[0]["poker"], 40)

    def test_jugada_poker_servida(self):
        tabla = TablaPuntos(2)  
        tabla.anotar(0, "poker", 1, [1, 1, 1, 1, 5])
        self.assertEqual(tabla._tabla[0]["poker"], 45)

    # generala
    def test_jugada_generala_mal(self):
        tabla = TablaPuntos(2)  
        with self.assertRaises(TablaPuntosError):
            tabla.anotar(0, "generala", 2, [1, 1, 2, 1, 1])
        self.assertEqual(tabla._tabla[0]["generala"], None)

    def test_jugada_generala_bien(self):
        tabla = TablaPuntos(2)  
        tabla.anotar(0, "generala", 2, [1, 1, 1, 1, 1])
        self.assertEqual(tabla._tabla[0]["generala"], 50)

    def test_jugada_generala_servida(self):
        tabla = TablaPuntos(2)  
        with self.assertRaises(Ganaste):
            tabla.anotar(0, "generala", 1, [1, 1, 1, 1, 1])
        self.assertEqual(tabla._tabla[0]["generala"], None) # ganar de una
    
    
    def test_tachar_general(self):
        tabla = TablaPuntos(2)
        tabla.anotar(0, "generala_doble", 1, [4, 1, 1, 5, 1]) 
        self.assertEqual(tabla._tabla[0]["generala_doble"], 0)
        tabla.anotar(0, "generala", 1, [4, 1, 1, 5, 1])
        self.assertEqual(tabla._tabla[0]["generala"], 0)


    # generala doble
    def test_jugada_generala_doble_mal(self):
        tabla = TablaPuntos(2)  
        tabla.anotar(0, "generala", 2, [1, 1, 1, 1, 1])
        tabla.anotar(0, "generala_doble", 2, [1, 4, 1, 1, 1]) 
        self.assertEqual(tabla._tabla[0]["generala_doble"], 0)

    def test_jugada_generala_doble_sin_simple(self): # no tenes la generala simple
        tabla = TablaPuntos(2)  
        with self.assertRaises(TablaPuntosError):
            tabla.anotar(0, "generala_doble", 2, [1, 1, 1, 1, 1]) 
        self.assertEqual(tabla._tabla[0]["generala_doble"], None)

    def test_jugada_generala_doble_bien(self):  # ahora si tenes la simple
        tabla = TablaPuntos(2)  
        tabla.anotar(0, "generala", 2, [1, 1, 1, 1, 1])
        tabla.anotar(0, "generala_doble", 2, [1, 1, 1, 1, 1])
        self.assertEqual(tabla._tabla[0]["generala_doble"], 100)

    def test_jugada_generala_doble_servida_sin_simple(self): # gana igual, pero por generala simple servida
        tabla = TablaPuntos(2) 
        with self.assertRaises(Ganaste):  
            tabla.anotar(0, "generala_doble", 1, [1, 1, 1, 1, 1])
        self.assertEqual(tabla._tabla[0]["generala_doble"], None) 

    def test_jugada_generala_doble_servida_bien(self): # ajá, vale soñar...
        tabla = TablaPuntos(2) 
        tabla.anotar(0, "generala", 2, [1, 1, 1, 1, 1])
        with self.assertRaises(Ganaste):  
            tabla.anotar(0, "generala_doble", 1, [1, 1, 1, 1, 1])
        self.assertEqual(tabla._tabla[0]["generala_doble"], None) # ganar de una

    def test_tachar_generala_doble(self):
        tabla = TablaPuntos(2) 
        tabla.anotar(0, "generala_doble", 2, [4, 1, 1, 5, 1])
        self.assertEqual(tabla._tabla[0]["generala_doble"], 0)



class CalcularPuntosTest(unittest.TestCase): #30

    # numeros
    def test_calcular_puntos_1_0_puntos(self):
        dados = [2, 2, 3, 4, 5]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "1")
        self.assertEqual(puntos, 0)

    def test_calcular_puntos_1_1_punto(self):
        dados = [2, 1, 3, 4, 5]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "1")
        self.assertEqual(puntos, 1)

    def test_calcular_dados_iguales_dobles(self):
        dados = [1, 2, 2, 3, 6]
        repetidos = calcular_repetidos(dados)
        self.assertEqual(
            repetidos, [
                1,  # 1
                2,  # 2
                1,  # 3
                0,  # 4
                0,  # 5
                1,  # 6
            ]
        )

    def test_calcular_dados_iguales_trios(self):
        dados = [1, 3, 2, 3, 3]
        repetidos = calcular_repetidos(dados)
        self.assertEqual(
            repetidos, [
                1,  # 1
                1,  # 2
                3,  # 3
                0,  # 4
                0,  # 5
                0,  # 6
            ]
        )

    def test_calcular_puntos_1_2_puntos(self):
        dados = [2, 1, 1, 4, 5]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "1")
        self.assertEqual(puntos, 2)

    def test_calcular_puntos_1_5_puntos(self):
        dados = [1, 1, 1, 1, 1]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "1")
        self.assertEqual(puntos, 5)

    def test_calcular_puntos_2_2_puntos(self):
        dados = [2, 1, 3, 4, 5]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "2")
        self.assertEqual(puntos, 2)

    def test_calcular_puntos_2_10_puntos(self):
        dados = [2, 2, 2, 2, 2]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "2")
        self.assertEqual(puntos, 10)

    def test_calcular_puntos_3_15_puntos(self):
        dados = [3, 3, 3, 3, 3]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "3")
        self.assertEqual(puntos, 15)

    def test_calcular_puntos_4_16_puntos(self):
        dados = [4, 4, 4, 6, 4]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "4")
        self.assertEqual(puntos, 16)

    def test_calcular_puntos_5_25_puntos(self):
        dados = [5, 5, 5, 5, 5]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "5")
        self.assertEqual(puntos, 25)

    def test_calcular_puntos_6_30_puntos(self):
        dados = [6, 6, 6, 6, 6]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "6")
        self.assertEqual(puntos, 30)

    # poker
    def test_calcular_puntos_poker_puntos_0(self):
        dados = [6, 3, 4, 6, 6]
        numero_lanzamiento = 2
        puntos = calcular_puntos(numero_lanzamiento, dados, "poker")
        self.assertEqual(puntos, 0)

    def test_calcular_puntos_poker_puntos_40_por_4(self):
        dados = [6, 6, 4, 6, 6]
        numero_lanzamiento = 2
        puntos = calcular_puntos(numero_lanzamiento, dados, "poker")
        self.assertEqual(puntos, 40)

    def test_calcular_puntos_poker_puntos_40_por_5(self):
        dados = [6, 6, 6, 6, 6]
        numero_lanzamiento = 2
        puntos = calcular_puntos(numero_lanzamiento, dados, "poker")
        self.assertEqual(puntos, 40)

    def test_calcular_puntos_poker_puntos_45_servido(self):
        dados = [6, 6, 4, 6, 6]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "poker")
        self.assertEqual(puntos, 45)

    # full
    def test_calcular_puntos_full_puntos_0(self):
        dados = [3, 3, 4, 2, 6]
        numero_lanzamiento = 2
        puntos = calcular_puntos(numero_lanzamiento, dados, "full")
        self.assertEqual(puntos, 0)

    def test_calcular_puntos_full_puntos_0_2(self):
        dados = [3, 3, 3, 2, 6]
        numero_lanzamiento = 2
        puntos = calcular_puntos(numero_lanzamiento, dados, "full")
        self.assertEqual(puntos, 0)


    def test_calcular_puntos_full_puntos_30(self):
        dados = [3, 3, 6, 6, 6]
        numero_lanzamiento = 2
        puntos = calcular_puntos(numero_lanzamiento, dados, "full")
        self.assertEqual(puntos, 30)

    def test_calcular_puntos_full_puntos_35(self):
        dados = [3, 3, 6, 6, 6]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "full")
        self.assertEqual(puntos, 35)

    # escalera
    def test_calcular_puntos_escalera_puntos_0(self):
        dados = [1, 2, 5, 4, 5]
        numero_lanzamiento = 2
        puntos = calcular_puntos(numero_lanzamiento, dados, "escalera")
        self.assertEqual(puntos, 0)

    def test_calcular_puntos_escalera_menor_puntos_20(self):
        dados = [4, 1, 2, 3, 5]
        numero_lanzamiento = 2
        puntos = calcular_puntos(numero_lanzamiento, dados, "escalera")
        self.assertEqual(puntos, 20)

    def test_calcular_puntos_escalera_mayor_puntos_20(self):
        dados = [2, 3, 4, 5, 6]
        numero_lanzamiento = 2
        puntos = calcular_puntos(numero_lanzamiento, dados, "escalera")
        self.assertEqual(puntos, 20)

    def test_calcular_puntos_escalera_menor_puntos_25(self):
        dados = [2, 3, 4, 5, 1]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "escalera")
        self.assertEqual(puntos, 25)

    def test_calcular_puntos_escalera_mayor_puntos_25(self):
        dados = [2, 3, 4, 5, 6]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "escalera")
        self.assertEqual(puntos, 25)

    # generala
    def test_calcular_puntos_generala_puntos_0(self):
        puntos = calcular_puntos(1, [2, 3, 4, 5, 6], "generala")
        self.assertEqual(puntos, 0)

    def test_calcular_puntos_generala_puntos_50(self):
        puntos = calcular_puntos(2, [2, 2, 2, 2, 2], "generala")
        self.assertEqual(puntos, 50)

    def test_calcular_puntos_generala_servida_ganaste(self):
        with self.assertRaises(Ganaste):
            calcular_puntos(1, [2, 2, 2, 2, 2], "generala")

    # generala doble
    def test_calcular_puntos_generala_doble_puntos_100(self):
        puntos = calcular_puntos(2, [2, 2, 2, 2, 2], "generala_doble")
        self.assertEqual(puntos, 100)

    def test_calcular_puntos_generala_doble_puntos_0(self):
        puntos = calcular_puntos(2, [2, 2, 2, 2, 3], "generala_doble")
        self.assertEqual(puntos, 0)

    def test_calcular_puntos_generala_doble_servida_ganaste(self):
        with self.assertRaises(Ganaste):
            calcular_puntos(1, [2, 2, 2, 2, 2], "generala_doble")


class GanadorTest(unittest.TestCase): #6
    def test_suma_puntos_y_fin_juego(self):
        tabla = TablaPuntos(1)
        tabla._tabla = [  # lista/jugador
            {  # diccionario/jugada
                '1': 1,
                '2': 1,
                '3': 1,
                '4': 1,
                '5': 1,
                '6': 1,
                'escalera': 1,
                'full': 1,
                'poker': 1,
                'generala': 1,
                'generala_doble': 1,
            }
        ]
        a, b = tabla.estado_tabla
        self.assertEqual(a, True)
        self.assertEqual(b, [11])

    def test_suma_puntos_y_fin_juego_mal(self):
        tabla = TablaPuntos(1)
        tabla._tabla = [  # lista/jugador
            {  # diccionario/jugada
                '1': 1,
                '2': 1,
                '3': 1,
                '4': 1,
                '5': None,
                '6': 1,
                'escalera': 1,
                'full': 1,
                'poker': 1,
                'generala': 1,
                'generala_doble': 1,
            }
        ]
        a, b = tabla.estado_tabla
        self.assertEqual(a, False)
        self.assertEqual(b, 0)

    def test_comparar_mayor_puntaje_2jugador_mal(self):
        # la generala tiene que ver si la condicion de "está jugando" es falsa y comparar cual es el puntaje mayor 
        juego = Generala(2)
        juego.tabla_puntos._tabla = [  # lista/jugador
            {  # diccionario/jugada
                '1': 1,
                '2': 1,
                '3': 1,
                '4': 1,
                '5': 1,
                '6': None,
                'escalera': 1,
                'full': 1,
                'poker': 1,
                'generala': 1,
                'generala_doble': 1,
            },
            {  
                '1': 1,
                '2': 1,
                '3': 1,
                '4': 1,
                '5': 1,
                '6': None,
                'escalera': 1,
                'full': 1,
                'poker': 40,
                'generala': 1,
                'generala_doble': 1,
            }
        ]     

        juego.turno_actual.dados_lanzados._valores = [1, 2, 3, 4, 6]
        juego.anotar("6")
        juego.turno_actual.dados_lanzados._valores = [1, 2, 3, 4, 6]
        a, b = juego.tabla_puntos.estado_tabla
        self.assertEqual(a, False)
        self.assertEqual(b, 0)  

    def test_comparar_mayor_puntaje_2jugador_bien(self):
        # la generala tiene que ver si la condicion de "está jugando" es falsa y comparar cual es el puntaje mayor 
        juego = Generala(2)
        juego.tabla_puntos._tabla = [  # lista/jugador
            {  # diccionario/jugada
                '1': 1,
                '2': 1,
                '3': 1,
                '4': 1,
                '5': 1,
                '6': None,
                'escalera': 1,
                'full': 1,
                'poker': 1,
                'generala': 1,
                'generala_doble': 1,
            },
            {  
                '1': 1,
                '2': 1,
                '3': 1,
                '4': 1,
                '5': 1,
                '6': None,
                'escalera': 1,
                'full': 1,
                'poker': 1,
                'generala': 1,
                'generala_doble': 1,
            }
        ]     

        juego.turno_actual.dados_lanzados._valores = [1, 2, 3, 4, 6]
        juego.anotar("6")
        juego.turno_actual.dados_lanzados._valores = [1, 2, 6, 4, 6]
        juego.anotar("6")
        a, b = juego.tabla_puntos.estado_tabla
        self.assertEqual(a, True)
        self.assertEqual(b, [16, 22]) 

    def test_comparar_mayor_puntaje_1jugador(self):
        # la generala tiene que ver si la condicion de "está jugando" es falsa y comparar cual es el puntaje mayor 
        juego = Generala(2)
        juego.tabla_puntos._tabla = [  # lista/jugador
            {  # diccionario/jugada
                '1': 1,
                '2': 1,
                '3': 1,
                '4': 1,
                '5': 1,
                '6': None,
                'escalera': 1,
                'full': 1,
                'poker': 1,
                'generala': 1,
                'generala_doble': 1,
            }
        ]     

        juego.turno_actual.dados_lanzados._valores = [1, 2, 3, 4, 6]
        juego.anotar("6")
        a, b = juego.tabla_puntos.estado_tabla
        self.assertEqual(a, True)
        self.assertEqual(b, [16])  

    def test_comparar_mayor_puntaje_2jugador(self):
        # la generala tiene que ver si la condicion de "está jugando" es falsa y comparar cual es el puntaje mayor 
        juego = Generala(2)
        juego.tabla_puntos._tabla = [  # lista/jugador
            {  # diccionario/jugada
                '1': 1,
                '2': 1,
                '3': 1,
                '4': 1,
                '5': 1,
                '6': None,
                'escalera': 1,
                'full': 1,
                'poker': 1,
                'generala': 1,
                'generala_doble': 1,
            },
            {  
                '1': 1,
                '2': 1,
                '3': 1,
                '4': 1,
                '5': 1,
                '6': None,
                'escalera': 1,
                'full': 1,
                'poker': 40,
                'generala': 1,
                'generala_doble': 1,
            }
        ]     

        juego.turno_actual.dados_lanzados._valores = [1, 2, 3, 4, 6]
        juego.anotar("6")
        juego.turno_actual.dados_lanzados._valores = [1, 2, 3, 4, 6]
        juego.anotar("6")
        a, b = juego.tabla_puntos.estado_tabla
        self.assertEqual(a, True)
        self.assertEqual(b, [16, 55])  


class ErroresInputs(unittest.TestCase): #5
    # Mal escrito las jugadas
    def test_mal_escrito_anotar_jugada(self):
        tabla = TablaPuntos(2)  
        with self.assertRaises(ErrorInputs):
            tabla.anotar(0, "40", 2, [1, 1, 2, 1, 5])
        self.assertEqual(tabla._tabla[0]["4"], None)

    def test_mal_escrito_anotar_jugada_2(self):
        tabla = TablaPuntos(2)  
        with self.assertRaises(ErrorInputs):
            tabla.anotar(0, "", 2, [1, 1, 2, 1, 5])
        self.assertEqual(tabla._tabla[0]["4"], None)

    def test_jugada_escalera_mayusculas(self):
        juego = Generala(2)
        juego.turno_actual.dados_lanzados._valores = [1, 2, 3, 4, 5]
        juego.anotar("EscalEra")
        self.assertEqual(juego.tabla_puntos._tabla[0]["escalera"], 25)

    def test_jugada_poker_mayusculas(self):
        juego = Generala(2)
        juego.turno_actual.dados_lanzados._valores = [1, 2, 3, 4, 5]
        juego.anotar("Poker")
        self.assertEqual(juego.tabla_puntos._tabla[0]["poker"], 0)

    def test_jugada_escalera_error_ortografico(self):
        tabla = TablaPuntos(2)  
        with self.assertRaises(ErrorInputs):
            tabla.anotar(0, "EscalEras", 2, [1, 2, 4, 3, 5])
        self.assertEqual(tabla._tabla[0]["escalera"], None)



if __name__ == '__main__':
    unittest.main()

