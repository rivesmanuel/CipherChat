from app.utils.funciones import *
import os
def  generar(nombre, fechas, otros, caracteres):

    nombreCap = capitalizacion(nombre)
    nombreFleek = remplazo(nombre)

    listaNombre = nombreCap + nombreFleek

    fechas = acortar(fechas)

    datos = {
        "nombre": listaNombre,
        "fechas": fechas,
        "otros": otros,
        "caracteres_especiales": caracteres
    }

    lista_final = listaFinal(nombre=datos['nombre'], fechas=datos['fechas'], otros=datos['otros'], caracteres=datos['caracteres_especiales'])

    var = variantes(lista_final)
    
    filename = f"wordlist_{nombre}.txt"
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.dirname(current_file_dir)
    wordlists_dir = os.path.join(app_dir, 'static', 'wordlists')
    filepath = os.path.join(wordlists_dir, filename)
    
    print(f"DEBUG: Intentando crear archivo en: {filepath}")  # Para debug
    
    os.makedirs(wordlists_dir, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        for pss in var:
            f.write(pss + '\n')
    
    return {
        'passwords': var,
        'filename': filename,
        'total': len(var)
    }
    #with open(f"{nombre.lower()}.txt", "w", encoding="utf-8") as f:
    #    f.write("\n".join(var))

    #return var

