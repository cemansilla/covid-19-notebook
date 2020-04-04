#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Funcionalidades para extracción de datos del European Centre for Disease Prevention and Control
https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases
"""

import requests
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import pandas as pd
from lib.helpers.Helper import *

def ecdc_get_data():
  """
  Extrae la data del Excel descargado de la web del ECDC

  Returns:
  False: Si no se encontró data.
  dict: Si se encontró data y pudo procesarse. El diccionario de retorno contiene en la key `rows` las filas y en la `key` update un boolean que indica si se trata de data nueva o no.
  """
  # Descarga el Excel y obtiene la data
  file_data = ecdc_download_xlsx()

  data = False

  if(file_data):
    data = dict()
    data['rows'] = ecdc_read_xlsx(file_data)
    data['update'] = file_data['update']
  
  return data

def ecdc_save_data_to_json(data):
  """
  Parameters:
  data (dict):

  Return:
  void

  Todo:
    * Recibir parámetro de dónde guardar los archivos.
    * Optimizar proceso de almacenamiento de los sucesivos json.
      * Especificar nombre y ubicación.
  """
  file_path = str(Path(__file__).parents[2]) + os.sep + 'data' + os.sep
  file_name = 'global.json'

  cant_rows = data.count()['date_report'] - 1
  with open(file_path + file_name, 'w') as f:
    f.write('[')

    c = 0
    a_iso2 = []
    a_iso3 = []
    a_countries = []
    for index, row in data.iterrows():
      data_row = row.to_dict()

      """
      Procesamiento para json principal
      """
      # Parseo de fecha
      date_report = pd.to_datetime(data_row['date_report']).date()
      data_row['date_report'] = str(date_report)

      # Paseo de GeoID NaN
      if isNaN(data_row['geoid']):
        data_row['geoid'] = ''

      # Paseo de population data NaN
      if isNaN(data_row['country_code']):
        data_row['country_code'] = ''

      # Paseo de population data NaN
      if isNaN(data_row['pop_data_2018']):
        data_row['pop_data_2018'] = ''

      # Escribo valores
      f.write(json.dumps(data_row, indent=4, default=json_util.default))

      # Escribo coma
      if(c < cant_rows):
        f.write(',')
        pass
      """
      ./Procesamiento para json principal
      """

      """
      Procesamiento para json auxiliares
      """
      if not data_row['geoid'] in a_iso2 and data_row['geoid']:
          a_iso2.append(data_row['geoid'])

      a_iso2.sort()      

      if not data_row['country_code'] in a_iso3 and data_row['country_code']:
        a_iso3.append(data_row['country_code'])

      a_iso3.sort()      

      if not data_row['countries_territories'] in a_countries and data_row['countries_territories']:
        a_countries.append(data_row['countries_territories'])

      a_countries.sort()      
      """
      ./Procesamiento para json auxiliares
      """

      c += 1
    
    f.write(']')

    write_to_json(a_iso2, 'iso2.json')
    write_to_json(a_iso3, 'iso3.json')
    write_to_json(a_countries, 'countries.json')
  

def ecdc_read_xlsx(file_data):
  """
  Parameters:
  file_data (dict): diccionario que contiene el path y nombre de archivo Excel a leer

  Return:
  Pandas DataFrame
  """
  return pd.read_excel(file_data['file_path'] + file_data['file_name'], names=['date_report', 'day', 'month',	'year',	'cases', 'deaths', 'countries_territories', 'geoid', 'country_code', 'pop_data_2018'])

def ecdc_get_xlxs_link():
  """
  Obtiene el link de descarga del Excel del día de la web del ECDC.

  Returns:
  False: Si no se encontró el link.
  string: Si se encontró la URL con el link en el HTML
  """
  url = 'https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide'

  page_response = requests.get(url, timeout=5)
  page_content = BeautifulSoup(page_response.content, 'html.parser')

  regex = re.compile('application/vnd.openxmlformats')
  link_html = page_content.find('a', {'type': regex})

  return link_html.get('href') if link_html else False

def ecdc_download_xlsx():
  """
  Descarga el Excel del día de la web del ECDC.

  Returns:
  False: Si no hay archivo por descargar.
  dict: Contiene el path, nombre de archivo y un flag que indica si se trata de data actualizada (ya procesada previamente) o no.
  """
  file_path = str(Path(__file__).parents[2]) + os.sep + 'data' + os.sep + 'xlsx' + os.sep
  link = ecdc_get_xlxs_link()

  file_data = False

  if(link):
    resp = requests.get(link)

    # Ruta de guardado
    if not os.path.exists(file_path):
      os.makedirs(file_path)

    # Escribo el archivo
    file_name = Path(urlparse(link).path).name

    update = False
    if not os.path.exists(file_path + file_name):    
      with open(file_path + file_name, 'wb') as output:
        output.write(resp.content)

      update = True

    file_data = dict({
      'file_name': file_name,
      'file_path': file_path,
      'update': update
    })

  return file_data