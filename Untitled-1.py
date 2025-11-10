import json
from datetime import datetime

def leer_propietarios(ARCHIVO_JSON):
    try:
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
            propietarios = json.load(f)
            print("Archivo JSON leído correctamente.\n")
    except:
        print("Error: No se encontró el archivo JSON o está dañado.")
        propietarios = {}
    
    finally:
        return propietarios

def mostrar_propietarios(propietarios):
    if len(propietarios) == 0:
        print("No hay propietarios registrados.\n")
    else:
        print("=== Lista de Propietarios Registrados ===")
        for dni, info in propietarios.items():
            print(f"\nDNI: {dni}")
            for clave, valor in info.items():
                print(f"  {clave.capitalize()}: {valor}")
    return
    
def guardar_propietarios(propietarios):
    try:
        with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
            json.dump(propietarios, f, indent=4, ensure_ascii=False)
            print("Datos guardados correctamente.\n")
    except:
        print(f"Error al guardar los datos")
    
    finally:
        return

def crear_propietario(propietarios, TIPOS_VALIDOS, ESTADOS_VALIDOS):
    dni = input("Ingrese DNI (8 dígitos): ")
    if len(dni) != 8 or not dni.isdigit():
        print("DNI inválido. Debe tener 8 dígitos numéricos.")
    
    elif dni in propietarios:
        print("El propietario ya existe.")
    
    else:
        nombre = input("Ingrese nombre completo: ")
        while len(nombre) == 0:
            print("El nombre no puede estar vacío.")
            nombre = input("Ingrese nombre completo: ")

        tipo = input("Ingrese tipo de estructura (teja, cemento, chapa): ")
        while tipo not in TIPOS_VALIDOS:
            print(f"Tipo inválido. Tipos válidos: {TIPOS_VALIDOS}")
            tipo = input("Ingrese tipo de estructura (teja, cemento, chapa): ")

        while True:
            try:
                coord_x = float(input("Ingrese coordenada X (float): "))
                if not (-90.0 <= coord_x <= 90.0):
                    raise ValueError("Coordenada X fuera de rango permitido (-90 a 90).")
                
                coord_y = float(input("Ingrese coordenada Y (float): "))
                if not (-180.0 <= coord_y <= 180.0):
                    raise ValueError("Coordenada Y fuera de rango permitido (-180 a 180).")
                break
            except ValueError as e:
                print(f" Error: {e}")

        estado = input("Ingrese estado (al dia, mora, plan de pago): ").lower()
        while estado not in ESTADOS_VALIDOS:
            print(f"Estado inválido. Estados válidos: {ESTADOS_VALIDOS}")
            estado = input("Ingrese estado (al dia, mora, plan de pago): ").lower()
            

        # Crear el registro
        propietarios[dni] = {
            "nombre": nombre,
            "tipo": tipo,
            "coordenadaX": coord_x,
            "coordenadaY": coord_y,
            "estado": estado
        }

        guardar_propietarios(propietarios)
        print("Propietario agregado correctamente.\n")
    return

def modificar(propietarios, ESTADOS_VALIDOS): 
   dni = input(...)
   if len(dni) != 8 or not dni.isdigit():
      print(...)
   elif dni not in propietarios:
      print(...)
   else:
      estado = input(...)
      while estado not in ESTADOS_VALIDOS:
        print(...)
        estado = input(...)
   propietarios[dni]['estado'] = estado 
   guardar_propietarios(propietarios)
   return 

def registrar_pago(propietarios, ARCHIVO_PAGOS):

    if len(propietarios) == 0:
        print("No hay propietarios registrados en el sistema.")
    else:
        dni = input("Ingrese DNI del propietario: ")
        if dni not in propietarios:
            print("DNI no encontrado en el sistema.")
        else:
            while True:
                try:
                    importe = int(input("Ingrese importe del pago (entre 1000 y 100000): "))
                    if not (1000 <= importe <= 100000):
                        raise ValueError("Importe fuera de rango permitido (1000 a 100000).")
                    else:
                        break
                except ValueError as e:
                    print(f"Error: {e}")
                
            fecha_hora = datetime.now()
            fecha = fecha_hora.strftime("%Y-%m-%d")
            hora = fecha_hora.strftime("%H:%M:%S")
            try:
                with open(ARCHIVO_PAGOS, "a", encoding="utf-8") as f:
                    f.write(f"{dni},{importe},{fecha},{hora}\n")
                print("Pago registrado correctamente.\n")
            except:
                print(f"Error al escribir en el archivo de pagos:")
    return


def leer_pagos(ARCHIVO_PAGOS):
    try:
        f = open(ARCHIVO_PAGOS, "r", encoding="utf-8")
        for fila in f:
            dni, importe, fecha, hora = fila.strip().split(",")
            print(f"DNI: {dni} | Importe: ${importe} | Fecha: {fecha} | Hora: {hora}")
        f.close

    except:
        print("Error: No se encontró el archivo de pagos.")
    
    finally:
        print()
        return

# =====================================================
# MENÚ PRINCIPAL
# =====================================================
def main():
    ARCHIVO_JSON = "propietarios.json"
    ARCHIVO_PAGOS = "pagos.txt"
    TIPOS_VALIDOS = ("teja", "cemento", "chapa")
    ESTADOS_VALIDOS = ("al dia", "mora", "plan de pago")
    
    propietarios = leer_propietarios(ARCHIVO_JSON)

    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Mostrar propietarios")
        print("2. Agregar propietario")
        print("3. Registrar pago")
        print("4. Mostrar pagos")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            mostrar_propietarios(propietarios)
        elif opcion == "2":
            crear_propietario(propietarios, TIPOS_VALIDOS, ESTADOS_VALIDOS)
        elif opcion == "3":
            registrar_pago(propietarios, ARCHIVO_PAGOS)
        elif opcion == "4":
            leer_pagos(ARCHIVO_PAGOS)
        elif opcion == "6":
            modificar(propietarios, ESTADOS_VALIDOS)
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida. Intente nuevamente.\n")
main()