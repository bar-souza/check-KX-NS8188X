#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import sys
import argparse

# Importa e traduz lib de encryption da panasonic para usarmos na autenticação do
import js2py
from temp import *  
js2py.translate_file("panasonic_encryption.js", "temp.py")

#Códigos de status possíveis
# //SYSTEM STATUS
# var CONST_SYSTEM_STATUS_INS = 0;
# var CONST_SYSTEM_STATUS_OUS = 1;
# var CONST_SYSTEM_STATUS_FLT = 2;
# var CONST_SYSTEM_STATUS_UNDEF = 4;
# //LINE STATUS ID
# var CONST_LINE_STATUS_ID_NON = 0;   //INS以外(エラーなし)
# var CONST_LINE_STATUS_ID_INS = 1;   //INS
# var CONST_LINE_STATUS_ID_LOS = 132; //LOS（同期外れ）                 0x84
# var CONST_LINE_STATUS_ID_AIS = 133; //AIS（Alarm Indication Signal）  0x85
# var CONST_LINE_STATUS_ID_RAI = 134; //RAI（Remote Alarm Indication）  0x86
# var CONST_LINE_STATUS_ID_SNC = 135; //マルチフレーム同期外れ          0x87
# var CONST_LINE_STATUS_ID_FRA = 136; //フレーマエラー                  0x88

# //LINE STATUS NAME
# var CONST_LINE_STATUS_NAME_NON = '';    //エラーなし
# var CONST_LINE_STATUS_NAME_INS = 'INS';
# var CONST_LINE_STATUS_NAME_LOS = 'Digital trunk out of Synchronization';
# var CONST_LINE_STATUS_NAME_AIS = 'Digital trunk AIS Reception';
# var CONST_LINE_STATUS_NAME_RAI = 'Digital trunk RAI Reception';
# var CONST_LINE_STATUS_NAME_SNC = 'Multiframe out of Synchronization';
# var CONST_LINE_STATUS_NAME_FRA = 'Framer error';
# var CONST_LINE_STATUS_NAME_UNDEF = 'Undefined';

# Função que trata os erros. Habilita o debug quando o parametro --debug é passado no script
def exception_handler(exception_type, exception, traceback, debug_hook=sys.excepthook):
    if parametros.debug:
        debug_hook(exception_type, exception, traceback)
    else:
        print('%s: %s' % (exception_type.__name__, exception))
sys.excepthook = exception_handler

# Recebe parametros
parser_parametros = argparse.ArgumentParser(description='Verificação de Link Status nos equipamentos KX-NS8188X')
parser_parametros.add_argument('-H','--host', action='store',dest='pHost',required=True,help='Endereço do equipamento KX-NS8188X a ser monitorado')
parser_parametros.add_argument('-U','--user', action='store',dest='pUser',required=True,help='Usuário do equipamento KX-NS8188X a ser monitorado')
parser_parametros.add_argument('-P','--password', action='store',dest='pPassword',required=True,help='Password do equipamento KX-NS8188X a ser monitorado')
parser_parametros.add_argument('--debug',action='store_true',required=False,help='Habilida o traceback do Python para debugar erros.')
parametros = parser_parametros.parse_args()

# Atribui parametros de entrada nas variaveis
url = 'http://'+parametros.pHost
user = temp.EncryptPassword(parametros.pUser)
password = temp.EncryptPassword(parametros.pPassword)

# Parametro que retorna o status do equipamento
params = (
    ('api', 'HOME_Home.ReadSiteList'),
)

# Parametros de autenticação do equipamento
data = {
  '_method': 'POST',
  'data[User][forcedLogin]': '1',
  'data[User][readOnly]': '1',
  'data[User][username]': user,
  'data[User][password]': password
}

s = requests.Session()
# Autentica na interface web do equipamento
s.post(url+'/WebMC/users/login', data=data, verify=False)
# Obtem status do equipamento
response = s.get(url+'/WebMC/gridForm/CommandCall/', params=params, verify=False)
# Faz o logout
s.get(url+'/WebMC/users/logout', verify=False)

r1 = json.loads(response.text)

if parametros.debug:
    print('Parametro -H --host: '+parametros.pHost)
    print('Parametro -U --user: '+parametros.pUser)
    print('Parametro -P --password: '+parametros.pPassword)
    print('Usuário codificado: '+user)
    print('Password codificado: '+password)
    print('IP do Equipamento: '+r1[0]['mc_unitconninfo_ip_adrs'])
    print('Número do tronco: '+r1[0]['mc_siteinfo_site_name'])
    print('Status do serviço: '+str(r1[0]['linestatus_insous']))
else:
    print(str(r1[0]['linestatus_insous']))

