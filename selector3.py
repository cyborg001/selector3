###########################################################################
###########################################################################
##                                                                       ##
##        selector3                                                      ##
##        version 3.0                                                    ##
##        creado por: Carlos Ramirez                                     ##
##                                                                       ##
###########################################################################
###########################################################################
import re
import os
def formatear_hyp(lineas):#path_file):
    # cambiaremos linea por lineas y linea sera = lineas[0] o a lineas[0][-1] como funcione
    lineas = lineas.split('\n')
    # print(lineas[2])
    analista = ''
  
    data_estaciones = ''
    index = -1
    for l in lineas:
        if 'STAT SP IPHASW' in l:
            index = lineas.index(l)+1
            data_estaciones=lineas[index:]
            # print(type(index))
        # if index >=0 and lineas.index(l) >= index:
        #     data_estaciones += l
    linea = lineas[0]
    # print(linea)
    
    anio = linea[1:5]
    mes = linea[6:8]
    dia = linea[8:10]
    if mes[0]==' ':
        mes=str(0)+mes[1]
    if dia[0]== ' ':
        dia = str(0)+dia[1]
    h = linea[11:13]
    if h[0]==' ':
        h =  str(0)+h[1]
    m = linea[13:15]
    if m[0]==' ':
        m = str(0)+m[1]
    s = linea[16:18]
    if s[0]==' ':
        s = str(0)+s[1]
    lat = linea[24:30]
    lon = linea[31:38]
    fecha = anio+'-'+mes+'-'+dia
    hora = h+':'+m+':'+s
    i_d = anio+mes+dia+h+m
    deph = linea[38:43]
    rms= linea[52:55]
    l = linea[56:-1]
    ml = '0.0'
    mc = '0.0'
    mw = '0.0'
    mag = '0.0'
    if 'L' in l:
        ml = (l[l.index('L')-3:l.index('L')])
    if 'C' in l:
        mc = l[l.index('C')-3:l.index('C')]
    if 'W' in l:
        mw = l[l.index('W')-3:l.index('W')]
    
    
    # sal=i_d+ '  '+fecha+'  '+hora+'  '+lat+'  '+lon+'  '+deph+'  '+mag+'  '
    sal = f'{i_d}  {fecha}  {hora}  {lat}  {lon}  {deph}  {mc}  {ml}  {mw}  {rms}'
    # json = "{'i_d':'"+i_d+"','fecha':'"+fecha+"','hora':'"+hora+"','lat':'"+lat+"','lon':'"+lon+"','deph':'"+deph+"','mag':'"+mag+"','comentario':'"+comentario+"}"

    obj = {'id':i_d,
    'analista':analista,
    "fecha":fecha,
    "hora":hora,
    "lat":lat,
    "lon":lon,
    "depth":deph,
    "mag":mag,
    "magC":mc,
    "rms":rms,
    "magL":ml,
    "magW":mw,
    "salida":sal,
    'data_estaciones':data_estaciones,

    }
    # obj = ''
    #print (json.dumps(obj))
    # print(obj)
    return obj




def filtrarEst(l, filtro):
    
    dis = f'{l[71:75]}'
    if dis != '    ' and float(dis) <= float(filtro):
        stat = l[1:5]
        ch = l[6:8]
        amp = l[33:40]
        # print(stat, ch, amp, dis)
        return stat, ch, amp, dis
    
def getData(entrada, filtro):
    datos = ''
    est = ""
    out = []
    data = formatear_hyp(entrada)
    # print(data)
    datos = data['salida']
    estaciones = data['data_estaciones']
    est_con_IAML = [n for n in estaciones if 'IAML' in n]
    # print(est_con_IAML)
    for n in est_con_IAML:
        salida = filtrarEst(n,filtro)
        # print(salida,'salida')
        if salida:
            out.append(f'{datos}  {salida[0]}  {salida[1]}  {salida[2]}  {salida[3]}')
    # print(out)
    return out
    
def getSelects(entrada,regexx):
    s = ''
    selects = []
    regexx2 = re.compile(r'\n')
    with open(entrada,'r') as f:
        f = f.readlines()
        for i in f:
            if regexx.search(i):
                selects.append(s)
                s = ''
            else:
                s+=i

    return selects

'''esta solucion se basa mas en string para y no en stream'''
def solucion(select,salida, dist):
    """select es el archivo de entrada que son muchos selects separados por lineas en blanco,
    dist es un parametro para filtrar por distancia los archivos de salida"""
    regexx = regexx =  re.compile(r'\s{79}\n')
    selects = getSelects(select,regexx)
    # print(selects)
    with open(salida,'w') as f:
        """abre el archivo de salida como f para copiar en el los datos parecidos al dummy"""
        f.write("id            fecha       hora      lat     lon      depth  mgC  mgL  mgW  rms  stat  ch  amplit   dis\n")
        for n in selects:
            # print(n)
            datos = getData(n,dist)
            # print(datos)
            if datos:
                for l in datos:
                    f.write(l+'\n')
            # break

# '''Para casos puntuales: un solo select'''         
filtro_distancias = 300
nombreArchivo = '2018 SDD Dominican data.out'
carpeta = 'entradas'
select = os.path.join(carpeta,nombreArchivo) #genera el path carpeta//nombreArchivo
# dist = 300
salida = f'dis-menor-{filtro_distancias}-{nombreArchivo[:-4]}.txt'
solucion(select,salida,filtro_distancias)

'''Para transformar un listado de archivos en una carpeta'''
# def filtrarLista(dist):
#     lista = os.listdir('entradas')
#     for n in lista:
#         if '.out' in n:
#             nombre = f'entradas/{n}'
#             salida = f'salidas/eugenio/dis-menor-{dist}-{n[:-4]}.txt'
#             solucion(nombre,salida,dist)
# dist = 200
# filtrarLista(dist)