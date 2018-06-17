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
import ConfigParser

def addPageNumber(canvas, doc):
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
def crea_report(fname, front_cover, back_cover, path, path2, path3, path4, medias, horas, pivot):
    """"""
    
    stylesheet = getSampleStyleSheet()
    
    
    filename = os.path.join(path, fname)
    doc = SimpleDocTemplate(filename, pagesize=portrait(A4))
    
    
    elements_medias = crearTablaMedias(path, medias)
    elements_horas = crearTablaHoras(path, horas)
    elements_pivot= crearTablaPivot(path, pivot)
    
    
    Story=[]
    
    width = 7*inch
    height = 9*inch    
    
    path_valores_par = path2
    path_valores_d = os.path.join(path3, 'D')
    path_valores_60 = os.path.join(path3, '60')
    path_valores_w = os.path.join(path3, 'W')
    path_valores_horas = path4
    
    
    os.chdir(path_valores_par)
    pictures = []
    for file in glob.glob("*.png"):
        pictures.append(os.path.join(path_valores_par,file))

    os.chdir(path_valores_w)
    pictures_w = []
    for file in glob.glob("*.png"):
        pictures_w.append(os.path.join(path_valores_w,file))
        
    os.chdir(path_valores_d)
    pictures_d = []
    for file in glob.glob("*.png"):
        pictures_d.append(os.path.join(path_valores_d,file))
    
            
    os.chdir(path_valores_60)
    pictures_60 = []
    for file in glob.glob("*.png"):
        pictures_60.append(os.path.join(path_valores_60,file))
    
    os.chdir(path_valores_horas)
    pictures_mh = []
    for file in glob.glob("*.png"):
        pictures_mh.append(os.path.join(path_valores_horas,file))
    
    
    Story.append(Image(front_cover, width, height))
    Story.append(PageBreak())
    
    for el in elements_medias:
        Story.append(el)
        
    Story.append(PageBreak())
    
    for el in elements_pivot:
        Story.append(el)
    
    Story.append(PageBreak())
    
    Story.append(Paragraph('Mejor horario Trading', stylesheet['Title']))
    for pic in pictures_mh:
        Story.append(Image(pic, width, height))
        Story.append(PageBreak())  
    
    Story.append(Paragraph('PARES', stylesheet['Title']))
    for pic in pictures:
        Story.append(Image(pic, width, height))
        Story.append(PageBreak())

    Story.append(Paragraph('VALORES EN GRAFICO SEMANAL', stylesheet['Title']))
    for pic in pictures_w:
        Story.append(Image(pic, width, height))
        Story.append(PageBreak())

    Story.append(Paragraph('VALORES EN GRAFICO DIARIO', stylesheet['Title']))
    for pic in pictures_d:
        Story.append(Image(pic, width, height))
        Story.append(PageBreak())

    Story.append(Paragraph('VALORES EN GRAFICO HORARIO', stylesheet['Title']))
    for pic in pictures_60:
        Story.append(Image(pic, width, height))
        Story.append(PageBreak())
                       
        
    # Story.append(Image(back_cover, width, height))
    # doc.build(Story, onFirstPage=addPageNumber, onLaterPages=addPageNumber)
    doc.build(Story, onLaterPages=addPageNumber)
    print ("creando {}".format(filename))
    

def leer_mejores_medias():
    data = []
    config = ConfigParser.ConfigParser()
    config.read('configuracion.cfg')
    directorio_base = config.get('data', 'directorio_base')
    
    filename = os.path.join(directorio_base, 'result', 'medias.csv')
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            data.append(row)
    
    return data[1:]


def leer_mejores_horas():
    data = []
    config = ConfigParser.ConfigParser()
    config.read('configuracion.cfg')
    directorio_base = config.get('data', 'directorio_base')
    
    filename = os.path.join(directorio_base, 'result', 'horas.csv')
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            data.append(row)
    
    return data[1:]

def leer_pivot_point():
    data = []
    config = ConfigParser.ConfigParser()
    config.read('configuracion.cfg')
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


def crearTablaMedias(path, medias):
    
    stylesheet = getSampleStyleSheet()
    
    # filename = os.path.join(path, 'tabla-medias.pdf')
    # doc = SimpleDocTemplate(filename,  pagesize=portrait(A4))
    # container for the 'Flowable' objects
    elements = []
    
    new_medias = []
    
    new_medias.append(['VALOR','TIEMPO','FUNCION','PERIODO','NUM.OP'])
    
    for m in medias:
        new_medias.append(m[0:5])
    
    medias = new_medias
    
    numero_columnas = len(medias[0])
    numero_filas = len(medias)
    
    data= medias
    t=Table(data,numero_columnas*[1*inch], numero_filas*[0.4*inch])
    
    ''''t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                           ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                           ('VALIGN',(0,0),(0,-1),'TOP'),
                           ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                           ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                           ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                           ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                           ]))'''

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
    # write the document to disk
    # doc.build(elements)
    return elements


def crearTablaHoras(path, horas):
    
    stylesheet = getSampleStyleSheet()
    
    # filename = os.path.join(path, 'tabla-horas.pdf')
    # doc = SimpleDocTemplate(filename,  pagesize=portrait(A4))
    # container for the 'Flowable' objects
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
    
    ''''t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                           ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                           ('VALIGN',(0,0),(0,-1),'TOP'),
                           ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                           ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                           ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                           ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                           ]))'''

    t.setStyle(TableStyle([('TEXTCOLOR',(0,1),(-1,-1),colors.blue),
                           ('ALIGN',(0,0),(-1,-1),'CENTER'),
                           # caja
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                           ]))
    
    elements.append(Paragraph('MEJORES HORAS TRADING', stylesheet['Title']))
    elements.append(Spacer(1,12))
    
    elements.append(t)
    
    # write the document to disk
    # doc.build(elements)

    return elements


def crearTablaPivot(path, data):
    
    stylesheet = getSampleStyleSheet()
    normal = stylesheet["Normal"]
    normal.alignment = TA_CENTER
    
    
    # filename = os.path.join(path, 'tabla-horas.pdf')
    # doc = SimpleDocTemplate(filename,  pagesize=portrait(A4))
    # container for the 'Flowable' objects
    elements = []
    
    new_data = []
    
    new_data.append(['VALOR','S3','S2','S1','PP','R1','R2','R3'])
    
    for m in data:
        new_data.append(m)
    
    data = new_data
    
    numero_columnas = len(data[0])
    numero_filas = len(data)
    
    
    '''p = ParagraphStyle('parrafos', 
        fontSize = 8,
        fontName="Times-Roman")
    
    data_result = []
    for d in data:
        data_v = []
        for v in d:
            data_v.append(Paragraph(v,p))
        data_result.append(data_v)
     
    data = data_result'''     
                   
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
    
    
    # write the document to disk
    # doc.build(elements)

    return elements



def crearDocumento(medias,horas,pivot):
    
    path1 = r"C:\tmp\bolsa\graficos\reporte"
    path2 = r"C:\tmp\bolsa\graficos\pares\D"
    path3 = r"C:\tmp\bolsa\graficos\valores"
    path4 = r"C:\tmp\bolsa\graficos\horas"

    front_cover = os.path.join(path1, 'img', "FrontCover.jpg")
    back_cover = os.path.join(path1, 'img', "BackCover2.jpg")
    
    ahora = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    filename = "report_{}.pdf".format(ahora)
    
    crea_report(filename, front_cover, back_cover, path1, path2, path3, path4, medias, horas, pivot)


def crearReporte():
    medias = leer_mejores_medias()
    horas = leer_mejores_horas()
    pivot = leer_pivot_point()
    crearDocumento(medias,horas,pivot)
    
    