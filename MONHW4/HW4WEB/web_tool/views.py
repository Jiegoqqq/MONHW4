#"D:/Program Files/Anaconda3/Scripts/activate"
from django.shortcuts import render
from django.db import connection
#from web_tool.models import User
from django.http import JsonResponse
import pandas as pd
import numpy as np
import os 
import sys
import yfinance as yf 
from django.views.decorators.csrf import csrf_exempt
from . import models
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
import json
import mplfinance as mpf
import sqlite3
import base64


def total_list(request):
    return render(request, 'total_list.html', locals())

def total_list__data(request):
    strategy =request.POST['strategy']

    url = ''
    if (strategy == 'HW4'):
        url = 'http://127.0.0.1:8000/web_tool/hw4/'   
    response = {
        'url':url,
    }
    return JsonResponse(response)

@csrf_exempt
def hw4(request):
    return render(request, 'hw4.html', locals())

@csrf_exempt
def hw4_data(request):

    #own_S08
    with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM own_S08_11_RNAfold;")

            result = cursor.fetchall()

            columns = [col[0] for col in cursor.description]
            own_S08_df = pd.DataFrame(result, columns=columns)


    own_S08_dict = own_S08_df.to_dict('records')

    #own_S09
    with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM own_S09_09_WT_RNAfold;")

            result = cursor.fetchall()

            columns = [col[0] for col in cursor.description]
            own_S09_df = pd.DataFrame(result, columns=columns)


    own_S09_dict = own_S09_df.to_dict('records')

    response = {
        'own_S08_dict':own_S08_dict,
        'own_S09_dict':own_S09_dict,
    }
    return JsonResponse(response)

@csrf_exempt
def hw4_S08_plot(request):

    index = request.POST.get('index')
    search_index = 'own_S08_'+ index + '_ss.png'
   

    current_working_directory = os.getcwd()

    current_folder = os.path.dirname(__file__)

    # 定義相對路徑
    target_folder = '../static/images/own_S08_RNAfold_PNG'

    # 建構絕對路徑
    absolute_path = os.path.normpath(os.path.join(current_folder, target_folder))

    # 改變工作資料夾
    os.chdir(absolute_path)

    with open(search_index, "rb") as f:
        
        data = f.read()

    # 对文件内容进行Base64编码
    img_str = base64.b64encode(data).decode("utf-8")
    
    os.chdir(current_working_directory)

    response = {
        'img_str':img_str ,
    }
    return JsonResponse(response)

@csrf_exempt
def hw4_S09_plot(request):

    index = request.POST.get('index')
    search_index = 'own_S09_'+ index + '_ss.png'
   

    current_working_directory = os.getcwd()
    
    current_working_directory = os.getcwd()

    current_folder = os.path.dirname(__file__)

    # 定義相對路徑
    target_folder = '../static/images/own_S09_RNAfold_PNG'

    # 建構絕對路徑
    absolute_path = os.path.normpath(os.path.join(current_folder, target_folder))

    # 改變工作資料夾
    os.chdir(absolute_path)

    with open(search_index, "rb") as f:
        
        data = f.read()

    # 对文件内容进行Base64编码
    img_str = base64.b64encode(data).decode("utf-8")

    os.chdir(current_working_directory)

    response = {
        'img_str':img_str ,
    }
    return JsonResponse(response)







