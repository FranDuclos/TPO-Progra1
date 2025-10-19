

# biblioteca_genes.py
def agregar_genes(path, organismos_vaidos, caracteres_validos):
    try:
        try:
            with open(path, mode="r", encoding="utf-8") as archivo:
                genes = archivo.readlines()  
        
        except FileNotFoundError:
            genes = []
        
        ids = []    
        for linea in genes:
            lista = linea.replace('\n','').split(';')
            gen_id = lista[0]
            ids.append(gen_id)  
        
        if ids:
            print("IDs existentes:",",".join(ids))
        else:
            print("No hay genes registrados aún")
            
            
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
                
            if gen_id in ids:
                resp = input(f"{gen_id} ya existe. ¿Sobrescribir? (si/no): ").strip().lower()
                if resp != "si":
                    print("No sobrescrito ingrese otro ID: ")
                    continue
                else:
                    genes = [linea for linea in genes if not linea.startswith(gen_id + ";")]
                    ids.remove(gen_id) #Elimiar un gen existente antes de sobrescribirlo
         
            nombre = input("Nombre: ")

            while True:     
                organismo = input("Organismo: ").lower()
                if organismo not in organismos_vaidos:
                    print(f"Organismo no valido ingrese uno valido {organismos_vaidos}: )")
                else:
                    break
            while True:
                secuencia = input("Secuencia: ").upper()
                if not all (c in caracteres_validos for c in secuencia) or len(secuencia) < 3:
                    print("Secuencia no validos, ingrese de nuevo: ")
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
                secuencia_mutante = "N/A"

            nueva_linea = f"{gen_id};{nombre};{secuencia};{organismo};{longitud};{funcion};{es_mutante}{secuencia_mutante}\n"
            genes.append(nueva_linea)
            ids.append(gen_id)
            print(f"Gen {gen_id} agregado exitosamente.\n")  # Confirmación

            with open(path, mode="w", encoding="utf-8") as archivo:
                archivo.writelines(genes)
            print("✓ Cambios guardados en el archivo.")
            return True
        
    except (OSError, IOError) as detalle:
        print("Error al intentar trabajar con el archivo:", detalle)
        return False

    
    return genes

def modificar_genes(path, organismos_vaidos, caracteres_validos):
    try:
        try:
            with open(path, mode="r", encoding="utf-8") as archivo:
                genes = archivo.readlines()  
        
        except FileNotFoundError:
            genes = []
        
        ids = []    
        for linea in genes:
            lista = linea.replace('\n','').split(';')
            gen_id = lista[0]
            ids.append(gen_id)  
        
        if ids:
            print("IDs existentes:",",".join(ids))
        else:
            print("No hay genes registrados aún")
    
        while True:
            gen_id_input = input("Ingresa el ID del gen que quieres visualizar/todos (o escribe 'salir' para terminar): ").upper()
            
            if gen_id_input.lower() == "salir":
                break
        
            if gen_id_input not in ids:
                print(f"Error: el gen {gen_id_input} no existe.")
                continue
        
            for linea in genes:
                lista = linea.replace('\n','').split(';')
                if lista[0] == gen_id_input:
                    print(f"\n{'='*40}")
                    print(f"DATOS ACTUALES DEL GEN {lista[0]}")
                    print(f"{'='*40}")
                    print(f"Nombre: {lista[1]}")
                    print(f"Secuencia: {lista[2]}")
                    print(f"Organismo: {lista[3]}")
                    print(f"Longitud: {lista[4]}")
                    print(f"Función: {lista[5]}")
                    es_mutante_actual = "Si" if lista[6].strip().lower() == "true" else "No"
                    print(f"Es mutante: {es_mutante_actual}")
                    break
            resp = input(f"\n¿Qué deseas hacer con el gen {gen_id_input}? (modificar/borrar/cancelar)").lower()

            if resp == "cancerar":
                print("Cancelado.")
                continue
            elif resp == "borrar":
                confirmacion = input(f"¿Estás seguro de borrar el gen: {gen_id_input}?").lower()

                if confirmacion == "si":
                    genes = [linea for linea in genes if not linea.startswith(gen_id_input + ";")]
                    ids.remove(gen_id_input)  
                    with open(path, mode="w", encoding="utf-8") as archivo:
                        archivo.writelines(genes)
                    
                    print(f"✓ Gen {gen_id_input} borrado exitosamente.\n")
                else:
                    print("Borrado cancelado.")
                continue
            
            elif resp == "modificar":
                genes = [linea for linea in genes if not linea.startswith(gen_id_input + ";")]
                ids.remove(gen_id_input)

                print("\nIngresa los nuevos datos:")
                nombre = input("Nombre: ")
                while True:
                    organismo = input("Organismo: ")
                    if organismo not in organismos_vaidos:
                        print(f"Organismo no valido ingrese uno valido {organismos_vaidos}: )")
                    else:
                        break
                while True:
                    secuencia = input("Secuencia: ")
                    if not all (c in caracteres_validos for c in secuencia) or len(secuencia) < 3:
                        print("Secuencia no validos, ingrese de nuevo: ")
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
                    secuencia_mutante = "N/A"

                nueva_linea = f"{gen_id_input};{nombre};{secuencia};{organismo};{longitud};{funcion};{es_mutante}{secuencia_mutante}\n"
                genes.append(nueva_linea)
                ids.append(gen_id_input)
                print(f"Gen {gen_id} agregado exitosamente.\n")  # Confirmación

                with open(path, mode="w", encoding="utf-8") as archivo:
                    archivo.writelines(genes)
                print("✓ Cambios guardados en el archivo.")
            else:
                print("Opción no valida. Usar: modificar/borrar/cancelar")
        return True

    except (OSError, IOError) as detalle:
        print("Error al intentar trabajar con el archivo:", detalle)
    return False 
    

def visualizar_genes(path):
    try:
        with open(path, mode="r", encoding="utf-8") as archivo:
            genes = archivo.readlines()  
        
        print("Genes disponibles:")
        ids = []  
        
        for linea in genes:
            lista = linea.replace('\n','').split(';')
            gen_id = lista[0]
            ids.append(gen_id)  
            print(f"- {gen_id}")
    
        while True:
            gen_id_input = input("Ingresa el ID del gen que quieres visualizar/todos (o escribe 'salir' para terminar): ").upper()
            
            if gen_id_input.lower() == "salir":
                break
            
            if gen_id_input.lower() == "todos":
                for linea in genes:
                    lista = linea.replace('\n','').split(';')
                    print(f"\n{'='*40}")
                    print(f"DATOS DEL GEN {lista[0]}")
                    print(f"{'='*40}")
                    print(f"Nombre: {lista[1]}")
                    print(f"Secuencia: {lista[2]}")
                    print(f"Organismo: {lista[3]}")
                    print(f"Longitud: {lista[4]}")
                    print(f"Funcion: {lista[5]}")
                    es_mutante = "Si" if lista[6].strip().lower() == "true" else "No"
                    print(f"Es mutante: {es_mutante}")
                    if es_mutante == "Si":
                        print(f"Secuencia mutante: {lista[7]}")
                    
                continue
            
            if gen_id_input in ids: 
                for linea in genes:
                    lista = linea.replace('\n','').split(';')
                    if lista[0] == gen_id_input:
                        print(f"\n{'='*40}")
                        print(f"DATOS DEL GEN {lista[0]}")
                        print(f"{'='*40}")
                        print(f"Nombre: {lista[1]}")
                        print(f"Secuencia: {lista[2]}")
                        print(f"Organismo: {lista[3]}")
                        print(f"Longitud: {lista[4]}")
                        print(f"Funcion: {lista[5]}")
                        es_mutante = "Si" if lista[6].strip().lower() == "true" else "No"
                        print(f"Es mutante: {es_mutante}")
                        if es_mutante == "Si":
                            print(f"Secuencia mutante: {lista[7]}")
                        break
            else:
                print("ID de gen no encontrado. Intenta de nuevo.")
                
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)

    return

def analizar_genes(path):
    try:
        with open(path, mode="r", encoding="utf-8") as archivo:
            genes = archivo.readlines()  
        
        print("Genes disponibles:")
        ids = []  
        
        for linea in genes:
            lista = linea.replace('\n','').split(';')
            gen_id = lista[0]
            ids.append(gen_id)  
            print(f"- {gen_id}")
    
        while True:
            gen_id_input = input("Ingresa el ID del gen que quieres analizar (o escribe 'salir' para terminar): ").upper()
            
            if gen_id_input.lower() == "salir":
                break
        
            if gen_id_input in ids:
                secuencia = ""
                for linea in genes:
                    lista = linea.replace('\n','').split(';')
                    if lista[0] == gen_id_input:
                        secuencia = lista[2]
                        secuencia_mutante = lista[7]
                        break
            
                while True:
                    respuesta = input("Que desesa analizar: %CG, SNPs, Traducir (o escribe 'salir' para terminar)").lower()

                    if respuesta == "salir":
                        break

                    if respuesta.upper() == "%GC":
                        porcentaje_gc, porcentaje_at = calcular_contenido_nucleotido(secuencia)
                        print(f"Contenido de GC: {porcentaje_gc:.2f}%") #el .2f lo corta en 2 decimales.
                        print((f"Contenido de AT: {porcentaje_at:.2f}%"))

                    elif respuesta == "snps":
                        if secuencia_mutante != "N/A":
                            resultado = encontrar_snp(secuencia, secuencia_mutante)
                            for snp in resultado:
                                print(f"Posición {snp['posicion']}: {snp['original']} → {snp['mutante']}")
                        else: 
                            secuencia_mutante == "N/A"
                            print("No existen poliformismos")

                    elif respuesta == "traducir":
                        secuencia_traducida = traducir_secuencia(secuencia)
                        print(f"La secuencia {secuencia} traducida es: {secuencia_traducida}")
                    else:
                        print("Entrada no valida, intente de nuevo:")
            else:
                print(f"El gen {gen_id_input} no existe en la lista")
        
    except (OSError, IOError) as detalle:
        print("Error al intentar trabajar con el archivo:", detalle)         

def traducir_secuencia(secuencia): #No se si podmos usar replace, pero estaria bueno.
    return ''.join(['U' if base == 'T' else base for base in secuencia])
    
    # return secuencia.replace("T", "U")
        
    

def encontrar_snp(secuencia, secuencia_mutante):
    """
    Encuentra la posición donde se generó el SNP entre la secuencia original y la mutante.
    Retorna la ubicación y que nucleotido ha cambiado.
    """
    snps = []
    for i in range(len(secuencia)):
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
            opciones = 4
            print()
            print("---------------------------")
            print("MENÚ ...         ")
            print("---------------------------")
            print("[1] Opción 1: agregar gen")
            print("[2] Opción 2: eliminar/modificar gen")
            print("[3] Opción 3: visualizar")
            print("[4] Opción 4: Analizar genes")
            print("[0] Salir del programa")
            print("---------------------------")
            print()
            
            opcion = input("Seleccione una opción: ")
            

            if opcion == "0": 
                break 
        
            elif opcion == "1":
                agregar_genes(path, organismos_vaidos, caracteres_validos)


            elif opcion == "2":
                modificar_genes(path, organismos_vaidos, caracteres_validos)
            
            elif opcion == "3":
                visualizar_genes(path)
            
            elif opcion == "4":
                analizar_genes(path)
main()