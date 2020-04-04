#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import date
import urllib.request
from urllib.parse import urlparse

"""
Funcionalidades para procesamiento de reportes de Google
"""

def google_movility_download_pdfs():
  """
  Descarga los reportes de movilidad en la carpeta /server/data/google_movility_pdf/[dia_actual]

  Return:
  void

  Todo:
    * Recibir parámetro de dónde guardar los archivos.
  """
  # Ruta de guardado
  today = date.today().strftime("%m-%d-%Y")
  file_path = str(Path(__file__).parents[2]) + os.sep + 'data' + os.sep + 'google_movility_pdf' + os.sep + today + os.sep

  if not os.path.exists(file_path):
    os.makedirs(file_path)

  links = google_mobility_get_pdf_links()
  for link in links:
    file_name = Path(urlparse(link).path).name
    urllib.request.urlretrieve(link, file_path + file_name)

def google_mobility_get_pdf_links():
  """
  Scraping de los links de reportes de movilidad

  Return:
  array
  """
  url = 'https://www.google.com/covid19/mobility/'

  page_response = requests.get(url, timeout=5)
  page_content = BeautifulSoup(page_response.content, 'html.parser')

  link_html = page_content.find_all('a', {'class': ['download-link']})

  links = []
  for item in link_html:
    links.append(item.get('href'))

  return links