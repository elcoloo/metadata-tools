__author__ = 'Ariel Anthieni'

#Definicion de Librerias
import os
import json
import csv
import codecs

import geojson
import shapely.wkt



"""
Es necesario que se instalen las librerias geojson y shapely para poder convertir los formatos
pip3 install geojson
pip3 install shapely
"""




#Establecimiento de variables
dir_origen = '/opt/repositorio/metadata-tools/convert-tools/data/in/'
dir_destino = '/opt/repositorio/metadata-tools/convert-tools/data/out/'
geocampo = 'WKT'


#Listo los archivos en el directorio
ficheros = os.listdir(dir_origen)


"""
El script analiza el contenido del encabezado del csv y genera el array luego produciendo un geojson
"""

for archivo in ficheros:

    ext = os.path.splitext(archivo)

    #verifico si es un producto
    if (( ext[0] == '20161212calles_gba')):

        #abro el csv
        filecsv = open(dir_origen+archivo)
        objcsv = csv.reader(filecsv)

        #Paso a un array la estructura
        arreglo = []
        geoarreglo = []
        propiedades = {}
        multigeo = {}
        multiwkt = ''

        for elemento in objcsv:
            arreglo.append(elemento)

        filecsv.close()

        encabezado = arreglo[0]

        idgeo = encabezado.index(geocampo)

        i = 0
        for elemento in arreglo:
            #Recorro el encabezado

            if i == 0 :
                i=i+1
            else:
                j = 0
                propiedades = {}
                for col in encabezado:

                    if (j != idgeo):
                        propiedades[col] = elemento[j]
                    else:
                        multiwkt = elemento[j]

                    j=j+1

                #convierto el wkt a geojson
                g1 = shapely.wkt.loads(multiwkt)

                #Almaceno las propiedades
                multigeo = geojson.Feature(geometry=g1, properties=propiedades)

                geoarreglo.append(multigeo)


        georesultado = { "type": "FeatureCollection", "features": [] }

        for value in geoarreglo:
            georesultado['features'].append(value)

        resultado = codecs.open(dir_destino+ext[0]+'.geojson', 'w','utf-8')
        jsongeo = json.dumps(georesultado, ensure_ascii=False).encode('utf8')

        resultado.write(jsongeo.decode('utf-8'))



        resultado.close()


