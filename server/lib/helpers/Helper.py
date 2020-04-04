#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import json
from bson import json_util
import configparser

def write_to_json(data, file_name):
  """
  Escribe 

  Parameters:
  data (array): Array con la data.
  file_name (string): Nombre del archivo.

  Return:
  void
  """
  file_path = str(Path(__file__).parents[2]) + os.sep + 'data' + os.sep

  cant_rows = len(data) - 1
  c = 0
  with open(file_path + file_name, 'w') as f:
    f.write('[')

    for row in data:
      f.write(json.dumps(row, indent=4, default=json_util.default))
      
      if(c < cant_rows):
        f.write(',')

      c += 1

    f.write(']')

def get_global_config_by_section(key):
  """
  Obtiene data de configuración de una sección dada en el archivo config/config.ini

  Parameters:
  key (string): Nombre de la sección dentro del archivo

  Returns:
  dict: data
  """
  data = dict()
  
  
  try:
    file_path = str(Path(__file__).parents[2]) + os.sep + 'config' + os.sep
    config = configparser.ConfigParser()
    config.read(file_path + 'config.ini')

    if(config.has_section(key)):
      for name, value in config.items(key):
        data.update({name:value})
  except:
    pass

  return data

def d(data):
  """
  Impresión de dump formateado

  Parameters:
  data (object|array): Elemento a imprimir

  Returns:
  void
  """
  print(json.dumps(data, indent=2))

def isNaN(string):
  """
  Return:
  boolean
  """
  return string != string