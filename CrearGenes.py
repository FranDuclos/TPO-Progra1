#Crear base de genes
import random
import os
def darIdIncremental(id):
    if id < 10:
        return "00" + str(id)
    elif id < 100:
        return "0" + str(id)
    else:
        return str(id)
    
def darLetra(letras):
    return random.choice(letras)

def darNucleotidos(nucleotidos):
    return random.choice(nucleotidos)

def darOrganismo(organismos_validos):
    return random.choice(organismos_validos)

def darFuncion(funciones):
    return random.choice(funciones)

def crear_mutacion(secuencia_original, nucleotidos):
    """
    Crea una mutación (SNP) en la secuencia original
    """
    #Converitmos la secuencia en lsita para poder mod
    secuencia_lista = list(secuencia_original)
    #Elegimos la posicion alazar para que ocurra el SNP
    posicion_mutante = random.randint(0, len(secuencia_lista)-1)

    nucleotido_original = secuencia_lista[posicion_mutante]
    #Elegir un nucleotido diferente
    nucleotidos_disponibles = [n for n in nucleotidos if n != nucleotido_original]
    nucleotido_mutante = random.choice(nucleotidos_disponibles)

    #Realizar la mutacion
    secuencia_lista[posicion_mutante] = nucleotido_mutante

    return "".join(secuencia_lista)

def crearRegistro(id):
    letras = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    nucleotidos = ["A", "C", "G", "T"]
    organismos_validos = [ "Escherichia coli",
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
    "Halobacterium salinarum"]
    funciones = [
        "Síntesis de proteínas", "Reparación del ADN", "Replicación del ADN", 
        "Transcripción de ARN", "Traducción de proteínas", "Metabolismo de glucosa",
        "Metabolismo de lípidos", "Metabolismo de aminoácidos", "Fotosíntesis",
        "Respiración celular", "Transporte de electrones", "Señalización celular",
        "Apoptosis", "Ciclo celular", "Síntesis de ribosomas", "Síntesis de hemoglobina",
        "Formación de microtúbulos", "Movimiento flagelar", "Síntesis de ATP",
        "Degradación de proteínas", "Transporte de iones", "Detoxificación celular",
        "Regulación hormonal", "Síntesis de colágeno", "Adhesión celular",
        "Respuesta al estrés", "Respuesta inmune", "Resistencia a antibióticos",
        "Síntesis de clorofila", "Síntesis de pigmentos", "Desarrollo embrionario",
        "Regulación epigenética", "Síntesis de lípidos de membrana",
        "Síntesis de ADN mitocondrial", "Reparación de mutaciones",
        "Regulación de la presión osmótica", "Transporte de oxígeno",
        "Secreción de enzimas", "Transporte de nutrientes", "Formación de pared celular",
        "Producción de insulina", "Degradación de glucógeno", "Síntesis de glucógeno",
        "Activación de receptores", "Comunicación intercelular",
        "Síntesis de ARN ribosomal", "Procesamiento de ARN", "Empaquetamiento del ADN",
        "Síntesis de histonas", "Síntesis de enzimas digestivas", "Degradación de grasas",
        "Síntesis de ácidos grasos", "Fotosíntesis anoxigénica", "Síntesis de carotenoides",
        "Formación de cloroplastos", "Desarrollo floral", "Formación de semillas",
        "Germinación", "Síntesis de hormonas vegetales", "Crecimiento celular",
        "Regulación del pH intracelular", "Síntesis de metabolitos secundarios",
        "Producción de toxinas", "Producción de antibióticos",
        "Mantenimiento del citoesqueleto", "Movimiento celular", "Migración celular",
        "Regeneración tisular", "Activación de linfocitos", "Producción de anticuerpos",
        "Síntesis de neurotransmisores", "Degradación de neurotransmisores",
        "Transmisión sináptica", "Desarrollo neuronal", "Síntesis de colina",
        "Formación de mielina", "Síntesis de ácido fólico", "Síntesis de vitaminas",
        "Metabolismo del nitrógeno", "Fijación de nitrógeno",
        "Degradación de compuestos tóxicos", "Homeostasis del calcio",
        "Regulación del sueño", "Síntesis de melatonina",
        "Regulación de temperatura corporal", "Producción de energía",
        "Síntesis de ADN polimerasa", "Síntesis de ARN polimerasa",
        "Síntesis de proteínas de choque térmico", "Formación de biofilm",
        "Regulación de la permeabilidad de membrana", "Degradación de almidón",
        "Síntesis de ácido láctico", "Síntesis de proteínas estructurales",
        "Reparación de doble cadena de ADN", "Metabolismo del azufre",
        "Síntesis de ferredoxina", "Formación de lisosomas",
        "Regulación del metabolismo oxidativo", "Síntesis de ferrocitocromo"
    ]
    gen = 'GEN'
    gen = gen + darIdIncremental(id)
    
    nombre = "".join(darLetra(letras) for _ in range(5))

    longitud_secuencia = random.randint(12, 200)
    secuencia = ''.join(darNucleotidos(nucleotidos) for _ in range(longitud_secuencia))
    
    organismo = darOrganismo(organismos_validos)

    longitud = len(secuencia)

    funcion = darFuncion(funciones)

    es_mutante = random.random() < 0.25

    if es_mutante:
        secuencia_mutante = crear_mutacion(secuencia,nucleotidos)
    else:
        secuencia_mutante = "N/A"
    
    registro = f'{gen};{nombre};{secuencia};{organismo};{longitud};{funcion};{es_mutante};{secuencia_mutante}\n'
    return registro
#La ruta no me daba, chat ayudo
'''
ruta = os.path.join("C:\\Users\\fran\\Desktop\\facu\\2º 2025\\Progra 1\\TP0\\TPO-Progra1", "registros.txt")
archivo = open(ruta, mode='w', encoding ='utf-8')

for i in range(1, 11):
    archivo.write(crearRegistro(i))

archivo.close()

print('Terminé')
'''
