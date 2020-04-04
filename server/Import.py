#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lib.helpers.Helper import *
from lib.helpers.ECDC_Helper import *
from lib.MongoDBClient import MongoDBClient

# 1. Obtengo la data del ECDC
data = ecdc_get_data()

# 2. Guardo en json
if(data):
  ecdc_save_data_to_json(data['rows'])

# 3. Guardo en Mongo
# Conexión a MongoDB
mc = MongoDBClient()
if(mc.isConnected()):  
  if(data and data['update']):
    for index, row in data['rows'].iterrows():
      #Convierto a diccionario
      data_row = row.to_dict()

      # Upsert
      condition = {
        'date_report': data_row['date_report'],
        'country_code': data_row['country_code']
      }
      mc.update('cases', data_row, condition)
  else:
    print('No hay data por actualizar')
else:
  print('Error de conexión a la DB')