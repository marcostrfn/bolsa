#! /usr/bin/env/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import glob
import os
import re
import sys
import shutil
import csv

from reportlab.lib.pagesizes import letter, landscape, A4, portrait
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak, Table, TableStyle, Spacer
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

from pyPdf import PdfFileWriter, PdfFileReader
import StringIO
import datetime
# import ConfigParser



def crear_directorio(directorio_destino):
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))   
        
        
        
def add_page_number(canvas, doc):
    """
    Add the page number
    """  
    # a4 = 210 x 197
    page_num = canvas.getPageNumber()
    text = "Page %s" % page_num
    canvas.drawRightString(200*mm, 20*mm, text)
    
    text = "Report by %s" % "Trampal Sotolutions (C) Sede en Carranque"
    canvas.drawString(10*mm, 20*mm, text)
    
    
#----------------------------------------------------------------------


def leer_mejores_medias(config):
    data = []
    directorio_base = config.get('data', 'directorio_base')
    
    filename = os.path.join(directorio_base, 'result', 'medias.csv')
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            data.append(row)
    
    return data[1:]


def leer_mejores_horas(config):
    data = []
    directorio_base = config.get('data', 'directorio_base')
    
    filename = os.path.join(directorio_base, 'result', 'horas.csv')
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            data.append(row)
    
    return data[1:]

def leer_pivot_point(config):
    data = []
    directorio_base = config.get('data', 'directorio_base')
    
    x=0
    filename = os.path.join(directorio_base, 'result', 'pivot.csv')
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            valor,s3,s2,s1,pp,r1,r2,r3=row
            if x>0:
                s3 = "{0:.5f}".format(float(s3))
                s2 = "{0:.5f}".format(float(s2))
                s1 = "{0:.5f}".format(float(s1))
                pp = "{0:.5f}".format(float(pp))
                r1 = "{0:.5f}".format(float(r1))
                r2 = "{0:.5f}".format(float(r2))
                r3 = "{0:.5f}".format(float(r3))
    
            data.append([valor,s3,s2,s1,pp,r1,r2,r3])
            x += 1
            
    return data[1:]


def crear_tabla_medias(medias):
    
    stylesheet = getSampleStyleSheet()

    elements = []
    new_medias = []
    new_medias.append(['VALOR','TIEMPO','FUNCION','PERIODO','NUM.OP'])
    for m in medias:
        new_medias.append(m[0:5])
    
    medias = new_medias
    
    numero_columnas = len(medias[0])
    numero_filas = len(medias)
    
    data=medias
    t=Table(data,numero_columnas*[1*inch], numero_filas*[0.4*inch])

    t.setStyle(TableStyle([('TEXTCOLOR',(0,1),(-1,-1),colors.blue),
                           ('ALIGN',(0,0),(-1,-1),'CENTER'),
                           ('TEXTCOLOR',(3,0),(3,-1),colors.red),
                           ('BACKGROUND',(0,1),(0,-1),colors.aliceblue),
                           ('BACKGROUND',(0,0),(-1,0),colors.aliceblue),
                           
                           # caja
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                           ]))
    
    
    ahora = datetime.datetime.now().strftime("%Y %m %d")
    elements.append(Paragraph(ahora, stylesheet['Title']))
    elements.append(Spacer(1,12))
    
    elements.append(Paragraph('MEJORES MEDIAS TRADING', stylesheet['Title']))
    elements.append(Spacer(1,12))
    
    elements.append(t)
    return elements


def crear_tabla_horas(horas):
    
    stylesheet = getSampleStyleSheet()

    elements = []
    
    new_horas = []
    new_horas.append(['VALOR','TIPO','PERIODO','HORA'])
    for m in horas:
        new_horas.append(m[0:4])
    
    horas = new_horas
    
    numero_columnas = len(horas[0])
    numero_filas = len(horas)
    
    data= horas
    t=Table(data,numero_columnas*[1*inch], numero_filas*[0.4*inch])

    t.setStyle(TableStyle([('TEXTCOLOR',(0,1),(-1,-1),colors.blue),
                           ('ALIGN',(0,0),(-1,-1),'CENTER'),
                           # caja
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                           ]))
    
    elements.append(Paragraph('MEJORES HORAS TRADING', stylesheet['Title']))
    elements.append(Spacer(1,12))
    
    elements.append(t)

    return elements


def crear_tabla_pivot( data):
    
    stylesheet = getSampleStyleSheet()
    normal = stylesheet["Normal"]
    normal.alignment = TA_CENTER
    
    elements = []
    new_data = []
    new_data.append(['VALOR','S3','S2','S1','PP','R1','R2','R3'])
    
    for m in data:
        new_data.append(m)
    
    data = new_data
    
    numero_columnas = len(data[0])
    numero_filas = len(data)    
                   
    t=Table(data,numero_columnas*[20*mm], numero_filas*[10*mm])

    t.setStyle(TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.blue),
                           ('ALIGN',(0,0),(-1,-1),'CENTER'),
                           ('TEXTCOLOR',(4,0),(4,-1),colors.red),
                           ('TEXTCOLOR',(5,0),(5,-1),colors.orange),
                           ('TEXTCOLOR',(3,0),(3,-1),colors.orange),
                           ('TEXTCOLOR',(6,0),(6,-1),colors.green),
                           ('TEXTCOLOR',(2,0),(2,-1),colors.green),
                           ('FONTSIZE', (0, 0), (-1, -1), 8), 
                           ('BACKGROUND',(0,1),(0,-1),colors.aliceblue),
                           ('BACKGROUND',(0,0),(-1,0),colors.aliceblue),
                           # caja
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                           ]))
    
    elements.append(Paragraph('PIVOT POINT FIBO', stylesheet['Title']))
    elements.append(Spacer(1,12))
    
    
    texto = '''Los pivot point han sido calculados en periodos diarios y en formato fibonacci.'''
    elements.append(Paragraph(texto, normal))
    elements.append(Spacer(1,12))
    
    elements.append(t)

    return elements



def crea_report(obj_config, medias, horas, pivot):
    
    directorio_base = obj_config.get('data', 'directorio_base')
    
    directorio_destino = os.path.join(directorio_base, 'result', 'reporte')
    crear_directorio(directorio_destino)
                
    
    ahora = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    filename = os.path.join(directorio_base, 'result', 'reporte', "report_{}.pdf".format(ahora))
    
    stylesheet = getSampleStyleSheet()
    
    doc = SimpleDocTemplate(filename, pagesize=portrait(A4))
    
    elements_medias = crear_tabla_medias(medias)
    elements_pivot= crear_tabla_pivot(pivot)
    
    story=[]
    
    width = 7*inch
    height = 9*inch    
    
    path_valores_par = os.path.join(directorio_base, 'graficos', 'pares', 'D')
    path_valores_horas = os.path.join(directorio_base, 'graficos', 'horas')
    
    pictures = []
    try:
        os.chdir(path_valores_par)
        for file in glob.glob("*.png"):
            pictures.append(os.path.join(path_valores_par,file))
    except:
        pass
    
    os.chdir(path_valores_horas)
    pictures_mh = []
    for file in glob.glob("*.png"):
        pictures_mh.append(os.path.join(path_valores_horas,file))
        
    
    for el in elements_medias:
        story.append(el)        
    story.append(PageBreak())
    
    for el in elements_pivot:
        story.append(el)
    story.append(PageBreak())
    
    story.append(Paragraph('Mejor horario Trading', stylesheet['Title']))
    for pic in pictures_mh:
        story.append(Image(pic, width, height))
        story.append(PageBreak())  
    
    if len(pictures) > 0:
        story.append(Paragraph('PARES', stylesheet['Title']))
        for pic in pictures:
            story.append(Image(pic, width, height))
            story.append(PageBreak())

    doc.build(story, onLaterPages=add_page_number)
    print ("creando {}".format(filename))
    
    
def crear_reporte(obj_config):
    ''' crea un reporte con los graficos de pares, valores
    pivot y mejores horas de trading.
    resultado en pdf en /graficos/valores/reporte'''
    
    medias = leer_mejores_medias(obj_config)
    horas = leer_mejores_horas(obj_config)
    pivot = leer_pivot_point(obj_config)
    crea_report(obj_config,medias,horas,pivot)
    
    
