from bs4 import BeautifulSoup
import dateutil.parser as dparser
import os
import tkinter as tk
from tkinter import filedialog
import string

file_path = "1437-14-LE22.html"
# root = tk.Tk()
# root.withdraw()
# file_path = filedialog.askopenfilename()


var = open(file_path, 'r+')

soup = BeautifulSoup(var, features="lxml")

lic = {}

lic["Nombre licitación"] = soup.find("span", {"id":"lblNombreLicitacion"}).string # Nombre licitación

lic["Licitación ID"] = soup.find("span", {"id":"lblNumLicitacion"}).string # Licitación ID
lic["Responsable"] = soup.find("span", {"id":"lblResponsable"}).string # Responsable
lic["Fecha publicación"] = soup.find("span", {"id":"lblFicha3Publicacion"}) # Fecha publicación
lic["Fecha cierre"] = soup.find("span", {"id":"lblFicha3Cierre"}) # Fecha cierre
lic["Fecha final de preguntas"] = soup.find("span", {"id":"lblFicha3Fin"}) # Fecha final de preguntas
lic["Fecha visita a terreno"] = soup.find("span", {"id":"grvFechasUsuario_ctl02_lblFicha3FechaUsuario"}) # Fecha visita a terreno

# Ubicación
lic["Dirección"] = soup.find("span", {"id":"lblFicha2Direccion"}) # Dirección
lic["Comuna"] = soup.find("span", {"id":"lblFicha2Comuna"}) # Comuna
lic["Región"] = soup.find("span", {"id":"lblFicha2Region"}) # Región

# Características del proyecto. Resumen tambien?
lic["Monto Total Estimado"] = soup.find("span", {"id": "lblFicha7MontoEstimado"}) # Monto Total Estimado
lic["Estimación en base a"] = soup.find("span", {"id":"lblFicha7Estimacion"}) #Estimación en base a
lic["Responsable"] = lic["Responsable"]
lic["Prohibición de subcontratación"] = soup.find("span", {"id":"lblFicha7Subcontratacion"}) # Prohibición de subcontratación

# Req. Generales: Visita a terreno, Criterios evaluación
lic["Condiciones visita terreno"] = soup.find("span", {"id":"grvFechasUsuario_ctl02_lblFicha3TituloFechaUsuario"})
lic["Fecha visita a terreno"] = lic["Fecha visita a terreno"]
gar1M = soup.find("span", {"id":"grvGarantias_ctl02_lblFicha8Monto"})
gar1U = soup.find("span", {"id":"grvGarantias_ctl02_lblFicha8TipoMoneda"})
lic["Garantia de seriedad de ofertas"] = [gar1M, gar1U]
gar2M = soup.find("span", {"id":"grvGarantias_ctl03_lblFicha8Monto"})
gar2U = soup.find("span", {"id":"grvGarantias_ctl03_lblFicha8TipoMoneda"})
lic["Garantía fiel de Cumplimiento de Contrato"] = [gar2M, gar2U]

# Fechas

# To CSV only
lic["Tipo de ID"] = lic["Licitación ID"].split("-")[-1]

print(lic["Fecha final de preguntas"])

lic["Hora de cierre"] = dparser.parse(soup.find("span", {"id":"lblFicha3Cierre"}).string,fuzzy=True).strftime("%H:%M")
lic["Fecha de inicio preguntas"] = soup.find("span", {"id":"lblFicha3Inicio"}).string
lic["Hora de inicio preguntas"] = dparser.parse(soup.find("span", {"id":"lblFicha3Inicio"}).string,fuzzy=True).strftime("%H:%M")
lic["Hora de cierre preguntas"] = dparser.parse(soup.find("span", {"id":"lblFicha3Fin"}).string,fuzzy=True).strftime("%H:%M")
lic["Fecha de respuestas"] = soup.find("span", {"id":"lblFicha3PublicacionRespuestas"}).string
lic["Fecha de adjudicación"] = soup.find("span", {"id":"lblFicha3Adjudicacion"}).string


listInOrder = ["Nombre licitación", "Licitación ID", "Responsable", "Fecha publicación",
               "Fecha cierre", "Fecha final de preguntas", "Fecha visita a terreno",
               "Dirección", "Comuna", "Región", "Monto Total Estimado", "Estimación en base a",
               "Responsable", "Prohibición de subcontratación", "Condiciones visita terreno",
               "Fecha visita a terreno", "Garantia de seriedad de ofertas",
               "Garantía fiel de Cumplimiento de Contrato"]


csvInOrder = ["Licitación ID", "Tipo de ID", "Palabras Clave", "Nombre licitación", "Responsable", "Responsable Resumido",
              "Comuna", "Región", "Categoria Minvu", "Categoria MOP", "Garantia de seriedad de ofertas",
              "Garantía fiel de Cumplimiento de Contrato", "Fecha visita a terreno", "Fecha publicación", "Fecha cierre",
              "Hora de cierre", "Fecha de inicio preguntas", "Fecha final de preguntas", "Hora de cierre preguntas",
              "Fecha de respuestas", "Fecha de adjudicación", "Fecha de revisión", "Monto Total Estimado", "Encargado",
              "Observaciones", "Observaciones resumidas"]

ignoreList = ["Palabras Clave", "Responsable Resumido", "Categoria Minvu", "Categoria MOP", "Fecha de revisión",
              "Encargado", "Observaciones", "Observaciones resumidas"]

excelPersonal = ["Nombre licitación", "Licitación ID", "Fecha publicación", "Fecha cierre", "Fecha final de preguntas",
                 "Fecha visita a terreno", "Región", "Monto Total Estimado"]


listErrors = []

licD = {}

for k, v in lic.items():
    try:
        if type(v) == str:
            printed = f'{k}: {v}'
            licD[k] = v
        else:
            printed = f'{k}: {v.string}'
            print(printed)
            licD[k] = v.string
    except:
        if k in ["Garantia de seriedad de ofertas","Garantía fiel de Cumplimiento de Contrato"]:
            try:
                newv = []
                for i in v:
                    newv.append(i.string)
                printed = f'{k}: {" ".join(newv)}'
                print (printed)
                licD[k] = " ".join(newv)
                continue
            except:
                listErrors.append(k)
                licD[k] = "Error"
                print("error")
        listErrors.append(k)
        licD[k] = "Error"

print ("Errors: ", listErrors)

print (licD)
print("")

for i in listInOrder:
    if i in ["Nombre licitación", 'Responsable', "Dirección"]:
        print (f'{i}: {string.capwords(licD[i])}')
    elif i in ["Fecha publicación", "Fecha cierre", "Fecha final de preguntas", "Fecha visita a terreno"]:
        try:
            date= dparser.parse(licD[i],fuzzy=True, dayfirst=True)
            print (f'{i}, {date.strftime("%d-%m-%Y")}')
        except:
            print (i, "Error")
    else:
        print (f'{i}: {licD[i]}')
print(licD)


print("")
csvList = []


for i in csvInOrder:
    if i in ignoreList:
        print (i, "-")
        csvList.append("-")
    elif i in ["Nombre licitación", 'Responsable', "Dirección"]:
        print (i, string.capwords(licD[i]))
        csvList.append(string.capwords(licD[i]))
    elif i in ["Fecha publicación", "Fecha cierre", "Fecha final de preguntas", "Fecha visita a terreno", "Fecha de inicio preguntas", "Fecha de respuestas", "Fecha de adjudicación"]:
        try:
            date= dparser.parse(licD[i],fuzzy=True, dayfirst=True)
            print (i, date.strftime("%d-%m-%Y"))
            csvList.append(date.strftime("%d-%m-%Y"))
        except:
            print (i, "Error")
            csvList.append("Error")
    else:
        print (i, licD[i])
        csvList.append(licD[i])

excelList = []
for i in excelPersonal:
    if i in ignoreList:
        print (i, "-")
        excelList.append("-")
    elif i in ["Nombre licitación", 'Responsable', "Dirección"]:
        print (i, string.capwords(licD[i]))
        excelList.append(string.capwords(licD[i]))
    elif i in ["Fecha publicación", "Fecha cierre", "Fecha final de preguntas", "Fecha visita a terreno", "Fecha de inicio preguntas", "Fecha de respuestas", "Fecha de adjudicación"]:
        try:
            date= dparser.parse(licD[i],fuzzy=True, dayfirst=True)
            print (i, date.strftime("%d-%m-%Y"))
            excelList.append(date.strftime("%d-%m-%Y"))
        except:
            print (i, "Error")
            excelList.append("Error")
    else:
        print (i, licD[i])
        excelList.append(licD[i])

# with open(f'{licD["Licitación ID"]}.html', 'w') as file:
#     file.write(var)

print(";".join(csvList))

print(";".join(excelList))

var.close()

extension = os.path.splitext(file_path)
os.rename(file_path, f'{lic["Licitación ID"]}{extension[1]}')
# print (lic)
# print(lic.Name)

# <span id="lblNombreLicitacion" class="texto04">