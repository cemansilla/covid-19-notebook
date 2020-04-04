#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lib.helpers.Helper import *
from lib.helpers.Google_Helper import *
from lib.MongoDBClient import MongoDBClient

# Descarga de PDFs de movilidad de Google ( https://www.google.com/covid19/mobility/ )
#google_movility_download_pdfs()

# Test de consultas a la data almacenada en MongoDB para ser enviada al sitio en GH Pages
mc = MongoDBClient()
if(mc.isConnected()):
  match = {
    '$match': {
      'country_code': 'ARG',
    }
  }
  #match = {}
  pipe = [    
    {
      '$group': {
        '_id': {
          'country_code': '$country_code',
          'date_report' : '$date_report'
        },
        'total': {
          '$sum': '$cases'
        }
      }
    },
    {
      '$sort': {
        '_id': 1
      }
    }
  ]

  if(match):
    pipe.insert(0, match)

  cases = mc.db.cases.aggregate(pipe)

  store = []
  for case in cases:
    print(case)
    store.append(case)

  #print('store', store)
  #j = json.dumps(store)
else:
  print('Error de conexión a la DB')