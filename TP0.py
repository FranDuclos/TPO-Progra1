# biblioteca_genes.py
import CrearGenes
import os
import json
import re

def crear_base_datos(path, json_path):  
    """
    Nos permite crear una base de datos con una cantidad de genes X, a partir del .py CrearGenes que importamos
    """
    while True:
        try:
            opcion = input("¿Cuantos genes desea que tenga la base de datos? o escriba 'salir' para terminar: ").lower()

            if opcion == "salir":
                print("Operación cancelada")
                break
            
            cantidad = int(opcion)

            if cantidad <= 0:
                print("Por favor ingrese un número positivo: ")
                continue

            if os.path.exists(path):
                confirmacion = input(f"El archivo '{path}' ya existe. ¿Desea sobreescribirlo? (si/no): ").lower()
                if confirmacion != "si":
                    print("Operación cancelada.")
                    break
            
            with open(path, mode='w', encoding='utf-8') as archivo:
                for i in range(1, cantidad + 1):
                    archivo.write(CrearGenes.crearRegistro(i))
                    
            print(f"TXT creado exitosamente con {cantidad} genes en {path}")
            
            print("\nConvirtiendo a diccionario...")
            
            #Convertimos directamente a diccionario :)
            diccionario = convertir_txt_a_diccionario(path)

            if diccionario:
                print(f"✓ Diccionario creado con {len(diccionario)} genes")

            else:
                print("Error al crear el diccionario")

            print("\n Guardando diccionario en JSON...")
            if guardar_a_json(diccionario, json_path):
                print(f"Base de datos completada exitosamente")
                print(f"- TXT fuente: {path}")
                print(f"- JSON activo: {json_path}")

                ver = input("\n¿Desea visualizar el diccionario creado? (si/no): ").lower()
                if ver == "si":
                    mostrar_diccionario(diccionario)

                return diccionario
            else:
                print("Error al guardar el JSON")
                return None
        
        except ValueError:
            print("Error, por favor ingrese un número válido.")
        except(OSError, IOError) as detalle:
            print(f"Error al crear el archivo: {detalle}")
            break
    
def convertir_txt_a_diccionario(path):
    """
    Lee el TXT y lo convierte a diccionario
    """
    try:
        diccionario_genes = {}

        with open(path, mode="r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split(";")

                if len(datos) >= 8:
                    gen_id = datos[0]
                    diccionario_genes[gen_id] = {
                        "nombre": datos[1],
                        "secuencia": datos[2],
                        "organismo": datos[3],
                        "longitud": int(datos[4]),
                        "funcion": datos[5],
                        "es_mutante": datos[6].lower == "true",
                        "secuencia_mutante": datos[7] if datos[7] != "N/A" else None
                    }
        return diccionario_genes
    
    except FileNotFoundError:
        print(f"✘ Error: El archivo '{path}' no existe.")
        return {}
    except (OSError, IOError) as detalle:
        print(f"✘ Error al leer el archivo: {detalle}")
        return {}

def cargar_json(json_path):
    """
    Carga el diccionario desde JSON
    """
    if not os.path.exists(json_path):
        print(f"✘ El archio '{json_path}' no existe")
        print(" Debe crear la basde de datos primero (Opción 1)")
        return None
    
    try:
        with open(json_path, "r", encoding="utf-8") as archivo:
            diccionario = json.load(archivo)
            return diccionario
    except json.JSONDecodeError:
        print(f"✘ Error: El archivo '{json_path}' está corrupto o vacío.")
        return None
    except Exception as e:
        print(f"✘ Error al cargar JSON: {e}")
        return None
    

def guardar_a_json(diccionario, json_path):
    """
    Guarda el diccionario en JSON.
    Se llama post cada modificación
    """
    try:
        with open(json_path, "w", encoding="utf-8") as archivo:
            json.dump(diccionario, archivo, indent=4, ensure_ascii=False)
        print(f"✔ Diccionario guardado como '{json_path}'")
        return True
    except Exception as e:
        print(f"✘ Error al guardar el JSON {e}")    
        return False
        
def mostrar_diccionario(diccionario):
    """
    Muestra el contenido del diccionario de genes
    """
    if not diccionario:
        print("El diccionario está vacío.")
        return
    
    print(f"\n{'='*50}")
    print(f"DICCIONARIO DE GENES ({len(diccionario)} genes)")
    print(f"{'='*50}")
    
    for gen_id, datos in diccionario.items():
        print(f"\n{gen_id}:")
        for clave, valor in datos.items():
            print(f"  {clave}: {valor}")

def visualizar_genes(diccionario):
    """
    Permite visualizar genes individuales o todos a la vez en formato matriz
    """
    try:
        if not diccionario:
            print("El diccionario está vacío.")
            return 
        
        print(f"\n{'='*50}")
        print("GENES DISPONIBLES:")
        print(f"{'='*50}")
        
        ids = list(diccionario.keys())
        for gen_id in ids:
            print(f"- {gen_id}")
        
        encabezados = ["gen_id", "nombre", "secuencia", "organismo", "longitud", "funcion", "es_mutante", "secuencia_mutante"]
        
        while True:
            opcion = input("\nIngresa el ID del gen que quieres visualizar/TODOS (o escribe 'SALIR' para terminar): ").upper()
            
            if opcion == "SALIR":
                print("Visualización finalizada.")
                break
            
            if opcion == "TODOS":
                matriz = []
                for gen_id, datos in diccionario.items():
                    fila = [
                        gen_id,
                        datos["nombre"],
                        datos["secuencia"][:20] + "...",
                        datos["organismo"],
                        datos["longitud"],
                        datos["funcion"],
                        datos["es_mutante"],
                        datos["secuencia_mutante"][:20] + "..." if datos["secuencia_mutante"] else None
                    ]
                    matriz.append(fila)
                print(f"\n✔ Matriz creada con {len(matriz)} genes\n")
                print(" | ".join(encabezados))
                print("-" * 130)
                for fila in matriz:  # Imprimir cada fila
                    print(" | ".join(str(item) for item in fila))
            
            elif opcion in ids:
                datos = diccionario[opcion]
                matriz = [
                    encabezados,
                    [
                        opcion,
                        datos["nombre"],
                        datos["secuencia"][:20] + "...",
                        datos["organismo"],
                        datos["longitud"],
                        datos["funcion"],
                        datos["es_mutante"],
                        datos["secuencia_mutante"][:20] + "..." if datos["secuencia_mutante"] else None
                    ]
                ]
                print(f"\n✔ Matriz creada para el gen {opcion}\n")
                print(" | ".join(encabezados))
                print("-" * 130)
                print(" | ".join(str(item) for item in matriz[1]))
            else:
                print("❌ ID no encontrado. Intenta nuevamente.")
                
    except Exception as e:
        print(f"Error al visualizar genes: {e}")
        return None

    
def agregar_genes(diccionario, organismos_vaidos, caracteres_validos, json_path):
    """
    Agregar genes al diccionario
    Guardado en JSON automatico. 
    """
    try:
        ids = list(diccionario.keys())

        if ids:
            print("IDs existentes:",",".join(ids))
        
        else:
            print("El diciconario está vacío")

        while True:
            if ids:
                ultimo_id = ids[-1] #Esto no los explico el chat
                try:
                    prefijo = ''.join([c for c in ultimo_id if not c.isdigit()]) #Extraer la palabra GEN de lo que escribimos
                    numero = int(''.join([c for c in ultimo_id if c.isdigit()])) #Extraer el número del GEN que escribimos
                    nuevo_numero = numero + 1
                    gen_id = f"{prefijo}{nuevo_numero:03d}"
                    
                except ValueError:
                    gen_id = "GEN001" #Si hay error empieza con esta ID

            else:
                gen_id = "GEN001" #De útima que haga el primer gen

            print(f"\ ID automático: {gen_id}")
            confirmar = input("¿Desesa usar este ID? (si/no) o escribe 'salir' para terminar: ").lower()
            
            if confirmar == "salir":
                break
                
            if confirmar != "si":
                gen_id = input("Ingresa el ID personalizado: ").upper()

            #Verificar si existe    
            if gen_id in ids:
                resp = input(f"✘ {gen_id} ya existe. ¿Sobrescribir? (si/no): ").strip().lower()
                if resp != "si":
                    print("No sobrescrito, ingrese otro ID: ")
                    continue
            
            
            #Recopilar datos
                
            nombre = input("Nombre del gen: ")

            while True:     
                organismo = input("Organismo: ")
                if organismo not in organismos_vaidos:
                    print(f"✘ Organismo no valido ingrese uno valido {organismos_vaidos}: )")
                else:
                    break

            while True:
                    secuencia = input("Secuencia: ").upper()
                    if not re.match(r'^[ATCG]{3,}$', secuencia):
                        print("✘ Secuencia no validos, ingrese de nuevo: ")
                    else:
                        break

            longitud = len(secuencia)

            funcion = input("Función: ")

            es_mutante = input("¿Es mutante? (si/no): ").lower() == "si"
            
            if es_mutante == "si":
                secuencia_mutante = secuencia
                secuencia_original = input("Ingrese la secuencia original: ")    
                secuencia = secuencia_original
            else:
                secuencia_mutante = None

            diccionario[gen_id] = {
                "nombre": nombre,
                "secuencia": secuencia,
                "organismo": organismo,
                "longitud": longitud,
                "funcion": funcion,
                "es_mutante": es_mutante,
                "secuencia_mutante": secuencia_mutante
            }

            ids.append(gen_id)
            print(f"Gen {gen_id} agregado exitosamente al diccionario.\n")  # Confirmación

            guardar_a_json(diccionario, json_path)

            continuar = input("¿Desea agregar otro gen? (si/no): ").lower()
            if continuar != "si":
                break
        
        return diccionario
        
    except KeyError as e:
        print(f"Error de clave en el diccionario: {e}")
        return diccionario
    except Exception as e:
        print(f"Error inesperado: {e}")
        return diccionario

def modificar_genes(diccionario, organismos_vaidos, json_path):
    """
    Eliminar/Modificar gen/es
    Guardado automático en JSON
    """
    try:
        ids = list(diccionario.keys())

        if ids:
            print("IDs existentes:",",".join(ids))
        
        else:
            print("El diccionario está vacío")

    
        while True:
            gen_id_input = input("\nIngresa el ID del gen que quieres visualizar/todos (o escribe 'salir' para terminar): ").upper()
            
            if gen_id_input == "SALIR":
                break
        
            if gen_id_input not in diccionario:
                print(f"✘ Error: el gen {gen_id_input} no existe.")
                continue
        
            datos = diccionario[gen_id_input]
            print(f"DATOS ACTUALES DEL GEN {gen_id_input}")
            print(f"Nombre: {datos['nombre']}")
            print(f"Secuencia: {datos['secuencia']}")
            print(f"Organismo: {datos['organismo']}")
            print(f"Longitud: {datos['longitud']}")
            print(f"Función: {datos['funcion']}")
            print(f"Es mutante: {'Si' if datos['es_mutante'] else 'No'}")
            if datos['secuencia_mutante']:
                print(f"Secuencia mutante: {datos['secuencia_mutante']}")
           
            resp = input(f"\n¿Qué deseas hacer con el gen {gen_id_input}? (modificar/borrar/cancelar)").lower()

            if resp == "cancelar":
                print("Operación cancelada.")
                continue

            elif resp == "borrar":
                confirmacion = input(f"¿Estás seguro de borrar el gen: {gen_id_input}?").lower()

                if confirmacion == "si":
                    del diccionario[gen_id_input]
                    print(f"✓ Gen {gen_id_input} borrado exitosamente.\n")

                    #Guardado en JSON
                    guardar_a_json(diccionario, json_path)


                else:
                    print("Borrado cancelado.")
                continue
            
            elif resp == "modificar":
                print("\n--- Ingrese los nuevos datos ---")
                nombre = input("Nombre del gen: ")

                while True:
                    organismo = input("Organismo: ")
                    if organismo not in organismos_vaidos:
                        print(f"✘ Organismo no valido ingrese uno valido {organismos_vaidos}: )")
                    else:
                        break

                while True:
                    secuencia = input("Secuencia: ").upper()
                    if not re.match(r'^[ATCG]{3,}$', secuencia):
                        print("✘ Secuencia no validos, ingrese de nuevo: ")
                    else:
                        break
                    
                longitud = len(secuencia)

                funcion = input("Función: ")

                es_mutante = input("¿Es mutante? (si/no): ").lower() == "si"
                
                if es_mutante == "si":
                    secuencia_mutante = secuencia
                    secuencia_original = input("Ingrese la secuencia original: ")    
                    secuencia = secuencia_original
                else:
                    secuencia_mutante = None

                diccionario[gen_id_input] = {
                    "nombre": nombre,
                    "secuencia": secuencia,
                    "organismo": organismo,
                    "longitud": longitud,
                    "funcion": funcion,
                    "es_mutante": es_mutante,
                    "secuencia_mutante": secuencia_mutante
                }
                print(f"✓ Gen {gen_id_input} modificado exitosamente.\n")

                guardar_a_json(diccionario, json_path)

            else:
                print("✘ Opción no valida. Usar: modificar/borrar/cancelar")
        
        return diccionario

    except KeyError as e:
        print(f"Error: clave no encontrada en el diccionario: {e}")
        return diccionario
    except Exception as e:
        print(f"Error inesperado: {e}")
        return diccionario
    

def analizar_genes(diccionario):
    """
    Analiza genes: CG%, SNPs, Traducción
    NO modifica el diccionario, por lo tanto NO guarda en JSON
    """
    try:
        ids = list(diccionario.keys())

        if ids:
            print("IDs existentes:",",".join(ids))
        
        else:
            print("El diciconario está vacío")

    
        while True:
            gen_id_input = input("\nIngresa el ID del gen que quieres visualizar/todos (o escribe 'salir' para terminar): ").upper()
            
            if gen_id_input == "SALIR":
                break
        
            if gen_id_input not in diccionario:
                print(f"✘ Error: el gen {gen_id_input} no existe.")
                continue
            
            
            datos = diccionario[gen_id_input]

            secuencia = datos['secuencia']
            
            secuencia_mutante = datos["secuencia_mutante"]

            while True:
                respuesta = input("Que desesa analizar: CG%, SNPs, Traducir (o escribe 'salir' para terminar)").lower()

                if respuesta == "salir":
                    break

                if respuesta.upper() == "CG%":
                    porcentaje_gc, porcentaje_at = calcular_contenido_nucleotido(secuencia)
                    print(f"\n📊 Contenido de nucleótidos:")
                    print(f"Contenido de GC: {porcentaje_gc:.2f}%") #el .2f lo corta en 2 decimales.
                    print((f"Contenido de AT: {porcentaje_at:.2f}%"))

                elif respuesta == "snps":
                    if secuencia_mutante != None:
                        resultado = encontrar_snp(secuencia, secuencia_mutante)
                        if resultado:
                            (f"\n🧬 SNPs encontrados: {len(resultado)}")
                            for snp in resultado:
                                print(f"Posición {snp['posicion']}: {snp['original']} → {snp['mutante']}")
                        else:
                            print("\n No se encontrarón SNPs entre las secuencias")
                    else: 
                        print("No existen poliformismos")

                elif respuesta == "traducir":
                    secuencia_traducida = traducir_secuencia(secuencia)
                    print(f"\n🔬 Traducción ADN → ARN:")
                    print(f"    ADN:  {secuencia}")
                    print(f"    ARN: {secuencia_traducida}")
                else:
                    print("✘ Opción no válida. Use: CG / SNPs / Traducir / salir")
            
        
    except KeyError as e:
        print(f"✘ Error: clave no encontrada en el diccionario: {e}")
        return diccionario
    except Exception as e:
        print(f"✘ Error inesperado: {e}")
        return diccionario         

def traducir_secuencia(secuencia): #No se si podmos usar replace, pero estaria bueno.
    return ''.join(['U' if base == 'T' else base for base in secuencia])
    
    # return secuencia.replace("T", "U")



def encontrar_snp(secuencia, secuencia_mutante):
    """
    Encuentra la posición donde se generó el SNP entre la secuencia original y la mutante.
    Retorna la ubicación y que nucleotido ha cambiado.
    """
    snps = []
    longitud_minima = min(len(secuencia), len(secuencia_mutante))
    for i in range(longitud_minima):
        if secuencia[i] != secuencia_mutante[i]:
            snp = {
                'posicion': i,
                'original': secuencia[i],
                'mutante': secuencia_mutante[i],
                'cambio': f"{secuencia[i]}>{secuencia_mutante[i]}"
            }
            snps.append(snp)
    
    return snps

def calcular_contenido_nucleotido(secuencia):
    """
    Calcula el procentaje de GC de la secuencia, es un dato clave
    a la hora de por ejemplo preparar una PCR.
    """
    gc = secuencia.count('G') + secuencia.count('C')
    at = secuencia.count('A') + secuencia.count('T')
    return (gc / len(secuencia)) * 100, (at / len(secuencia)) * 100

def main():
    path = "registros.txt"
    json_path = "genes.json"
    organismos_vaidos = ( "Escherichia coli",
    "Salmonella enterica",
    "Staphylococcus aureus",
    "Bacillus subtilis",
    "Pseudomonas aeruginosa",
    "Mycobacterium tuberculosis",
    "Lactobacillus acidophilus",
    "Clostridium botulinum",
    "Streptococcus pneumoniae",
    "Neisseria meningitidis",
    "Saccharomyces cerevisiae",
    "Aspergillus niger",
    "Candida albicans",
    "Penicillium chrysogenum",
    "Neurospora crassa",
    "Arabidopsis thaliana",
    "Oryza sativa",
    "Zea mays",
    "Triticum aestivum",
    "Glycine max",
    "Solanum lycopersicum",
    "Nicotiana tabacum",
    "Pisum sativum",
    "Drosophila melanogaster",
    "Caenorhabditis elegans",
    "Mus musculus",
    "Rattus norvegicus",
    "Homo sapiens",
    "Danio rerio",
    "Gallus gallus",
    "Bos taurus",
    "Sus scrofa",
    "Canis lupus familiaris",
    "Felis catus",
    "Equus caballus",
    "Pan troglodytes",
    "Macaca mulatta",
    "Anopheles gambiae",
    "Apis mellifera",
    "Aedes aegypti",
    "Xenopus laevis",
    "Strongylocentrotus purpuratus",
    "Toxoplasma gondii",
    "Plasmodium falciparum",
    "Trypanosoma cruzi",
    "Leishmania donovani",
    "Chlamydomonas reinhardtii",
    "Synechocystis sp. PCC 6803",
    "Methanococcus jannaschii",
    "Halobacterium salinarum")
    caracteres_validos = ("A", "C", "G", "T")

    while True:
            if os.path.exists(json_path):
                diccionario = cargar_json(json_path)
            print()
            print("---------------------------")
            print("MENÚ ...         ")
            print("---------------------------")
            print("[1] Opción 1: Crear base de datos")
            print("[2] Opción 2: Visualizar genes")
            print("[3] Opción 3: Agregar gen/es")
            print("[4] Opción 4: Eliminar/Modificar gen/genes")
            print("[5] Opción 5: Analizar gen")
            print("[6] Opción 6: Guardar en Json")
            print("[0] Salir del programa")
            print("---------------------------")
            print()
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "0": 
                break 
            
            elif opcion == "1":
                crear_base_datos(path, json_path)

            elif opcion in ["2", "3", "4", "5"]:
            # Para cualquier otra operación, cargar desde JSON
                if diccionario is None:
                    diccionario = cargar_json(json_path)
                
                if diccionario is None:
                    print("\n No hay datos disponibles.")
                    print("   Primero cree la base de datos (Opción 1)")
                    continue
                
                if opcion == "2":
                    visualizar_genes(diccionario)
                
                elif opcion == "3":
                    diccionario = agregar_genes(diccionario, organismos_vaidos, caracteres_validos, json_path)
                
                elif opcion == "4":
                    diccionario = modificar_genes(diccionario, organismos_vaidos, json_path)
                
                elif opcion == "5":
                    analizar_genes(diccionario)
                
                elif opcion == "6":
                    guardar_a_json(diccionario, json_path)
        
            else:
                print("Opción no válida. Intente nuevamente.")
            
main()