# Proyecto de Intro a Programacion #2 
import os 
import os.path 
import easygui
import pygame as pg

def analizar(carpeta, archivos, carpetas):
    """
    Función que se encarga de abrir el área designada y procede a analizarla
    Entradas y salidas:
    - carpeta: dirección donde debe buscar los archivos y carpetas
    - archivos y carpetas: son los archivos que se encuentran en esa dirección, al igual que las carpetas
    Salidas:
    - Una lista
    """
    try:
        elementos = os.listdir(carpeta)
    except PermissionError:
        print("Acceso denegado, ignorando carpeta: " + carpeta)
        return []
    else:
        total = 0
        subcarpetas = []
        cantidadArchivos = 0

        for e in elementos:
            ruta = os.path.join(carpeta, e)
            if os.path.isfile(ruta):
                tam = os.path.getsize(ruta)
                total += tam
                archivos.append((ruta, tam))
                cantidadArchivos += 1
            elif os.path.isdir(ruta):
                datos = analizar(ruta, archivos, carpetas)
                total += datos[1]
                subcarpetas.append(datos) 
        carpetas.append((carpeta, cantidadArchivos))

        return [carpeta, total, subcarpetas]

def dibujar(datos, tamP, x, y, window, cantidad, color):
    """
    Se enacarga de dibujar un gráfico con lo que se encuentra en la dirección
    """

    font = pg.font.Font(pg.font.match_font("calibri", bold = True), 14)

    tam = datos[1]
    w = tam / tamP * window.get_width()
    h = 40
    pg.draw.rect(window, color, (x, y, w, h), 0, 3)
    
    if w > 5: 
        pg.draw.rect(window, (255, 255, 255), (x, y, w, h), 1, 3)

    text = font.render(os.path.basename(datos[0]), True, (0,0,0))
    dim = pg.font.Font.size(font, os.path.basename(datos[0]))

    tamArchivo = tamArc(tam)
    text2 = font.render(tamArchivo, True, (0,0,0))
    dim2 = pg.font.Font.size(font, tamArchivo)

    if w >= dim[0] and w >= dim2[0]:
        window.blit(text, (x + 5, y + 5))
        window.blit(text2, (x + 5, y + dim[1] + 8))

    for subcarpetas in datos[2]: 
        color = changeColor(cantidad + 1)
        if cantidad < 6: 
            dibujar(subcarpetas, tamP, x, y + h, window, cantidad + 1, color)
            x += subcarpetas[1]/tamP * window.get_width()

def changeColor(i): 
    #Elige los colores dependiendo del caso
    if i == 1: 
        return (240, 73, 18)
    if i == 2: 
        return (247, 104, 0)
    if i == 3: 
        return (253, 132, 0)
    if i == 4: 
        return (255, 159, 0)
    if i == 5: 
        return (255, 185, 0)
    if i == 6: 
        return (255, 210, 0)

def tamArc(tam):
    #Define el tamaño de los atchivos
    # 1024 bytes = KB 
    # 1024 KB = MB
    # 1024 MB = GB
    # 1024 GB = TB
    x = 1024
    if tam in range(x, x**2):
        return str(round(tam / x,2)) + " KB"  
    if tam in range(x**2, x**3): 
        return str(round(tam / x**2,2)) + " MB"
    if tam in range(x**3, x**4): 
        return str(round(tam / x**3,2)) + " GB"
    if tam in range(x**4, x**5):
        return str(round(tam / x**5,2)) + " TB"
    return str(round(tam,2)) + " bytes"

def dibujarTop(window, L, x, y, titulo): 
    pg.draw.rect(window, (255, 255, 255), (0, 40 * 7 + 15, window.get_width(), window.get_height()), 1, 3)
    pg.draw.rect(window, (255, 255, 255), (0, 40 * 7 + 15, window.get_width() // 2, window.get_height()), 1, 3)

    font = pg.font.Font(pg.font.match_font("calibri", bold = True), 18)
    text = font.render(titulo, True, (255,255,255))
    dim = pg.font.Font.size(font, titulo)
    window.blit(text, (x + window.get_width() * 0.05, y))
    y += dim[1] * 2

    font = pg.font.Font(pg.font.match_font("calibri", bold = True), 14)
    print(titulo)
    print()
    for top in L: 
        print(top)
        text = font.render(top, True, (255,255,255))
        dim = pg.font.Font.size(font, top)

        if dim[0] > window.get_width() // 2:
            text = font.render(top[:106] + "        ->", True, (255,255,255))
            window.blit(text, (x, y))
            y += dim[1] 
            text = font.render(top[106::], True, (255,255,255))

        window.blit(text, (x, y))
        y += dim[1] * 1.9
    print()

def main():
    global ARCHIVOS, CARPETAS
    pg.init()
    window = pg.display.set_mode((1500, 750))
    pg.display.set_caption("Proyecto #2")
    loop = True
    print("\n" * 40)
    # Solicitar la ruta
    ruta = easygui.diropenbox("Escoja una carpeta", default="C:/")

    # Analisis de datos
# Lista con los nombres de archivos y sus tamanos
    archivos = []

# Lista con los nombres de las carpetas y la cantidad de archivos
# locales que contiene. 
    carpetas = []
    # window.fill((255, 255, 255))
    datos = analizar(ruta, archivos, carpetas)

    archivos.sort(key = lambda x: x[1], reverse = True)
    topArc = [nombre + "   " + str(tamArc(tam)) for nombre, tam in archivos][:10]

    carpetas.sort(key = lambda x: x[1], reverse = True)
    topCarp = [nombre + "   " + str(tam) + " archivos" for nombre, tam in carpetas][:10]

    # h = 40

    dibujar(datos, datos[1], 0, 5, window, 0, (230, 31, 31))
    dibujarTop(window, topArc, 5, 40 * 7 + 20, "Top 10 archivos más grandes")
    dibujarTop(window, topCarp, window.get_width() // 2 + 5, 40 * 7 + 20, "Top 10 directorios con mayor cantidad de archivos ")
    while loop: 
        pg.time.delay(16)
        for event in pg.event.get(): 
            if event.type == pg.QUIT:
                loop = False
        # funcion que dibuja los datos
        pg.display.update()
    pg.quit()

# Programa
main()