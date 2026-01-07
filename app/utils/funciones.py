from itertools import product, permutations
def capitalizacion(palabra):
    lista = []
    palabraUpper = palabra.upper()
    palabraLower = palabra.lower()
    palabraCap = palabra.capitalize()
    lista.append(palabraUpper)
    lista.append(palabraLower)
    lista.append(palabraCap)
    return lista

def acortar(fecha):
    lista = []
    if len(fecha) == 4:
        fecha_acortada = fecha[2:]
        lista.append(fecha)
        lista.append(fecha_acortada)
    elif len(fecha) == 10:
        fecha = fecha[6:]
        fecha_acortada = fecha[2:]
        lista.append(fecha)
        lista.append(fecha_acortada)
    return lista

def remplazo(nombre):
    dic = {
        "a": "@",
        "e": "€",
        "i": "1",
        "o": "0"
    }
    nombre_full = nombre
    listaFleek = []
    for letra, remplazo in dic.items():
        if letra in nombre_full:
            nombreFleek = nombre.replace(letra, remplazo)
            nombre_full = nombre_full.replace(letra, remplazo)
            listaFleek.append(nombreFleek)
    listaFleek.append(nombre_full)
    listaFleek = list(set(listaFleek))
    return listaFleek

def listaFinal(nombre, fechas, otros, caracteres):
    lista_final = []
    for n, f in product(nombre, fechas):
        password = n + f
        lista_final.append(password)
    
    for n, c, f in product(nombre, caracteres, fechas):
        password = n + c + f
        lista_final.append(password)

    for o, n in product(otros, nombre):
        password = o + n
        lista_final.append(password)

    for n, f, c in product(nombre, fechas, caracteres):
        password = n + f + c
        lista_final.append(password)

    for n, o, f in product(nombre, otros, fechas):
        password = n + o + f
        lista_final.append(password)

    if len(otros) > 1:
        for o1, o2 in permutations(otros, 2):
            for f in fechas:
                password = o1 + o2 + f
                lista_final.append(password)

    lista_final = list(set(lista_final))

    return lista_final

def variantes(lista_final):
    variantes = []
    for psswd in lista_final:
        psswd = remplazo(psswd)
        for pss in psswd:
            variantes.append(pss.lower())
            variantes.append(pss.upper())
            variantes.append(pss.capitalize())

    return list(set(variantes))