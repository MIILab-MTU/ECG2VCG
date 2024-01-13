# -*- coding: utf-8 -*-"
"""
Created on 04/25/2021  4:50 PM


@author: Zhuo
"""
import base64
import numpy as np

def find_EquName(file):
    tree = ET.parse(file)
    root = tree.getroot()
    children = root.getchildren()
def decode64base_ECG(code):
    code = code.replace(" ", "")
    code = code.replace("\n", "")
    code = code.replace("\r", "")

    data = base64.b64decode(code)
    ecg = np.frombuffer(data, dtype=np.int16)
    return ecg

def to_array(code):
    code = code.replace("\n", "")
    code = code.replace("\r", "")

    codearr = code.split(" ")
    codearr = [x.strip() for x in codearr if x.strip() != '']
    finalarr = []

    for i in codearr:
        finalarr.append(float(i))
    print(len(finalarr))
    return finalarr

def calculateVCG(trans_arr):
    """Calculate VCG from 8 leads transfer array.
    8 leads included in transLead_list"""

    Kors_trans = [
        [-0.13, 0.06, -0.43],
        [0.05, -0.02, -0.06],
        [-0.01, -0.05, -0.14],
        [0.14, 0.06, -0.2],
        [0.06, -0.17, -0.11],
        [0.54, 0.13, 0.31],
        [0.38, -0.07, 0.11],
        [-0.07, 0.93, -0.23],
    ]

    vcg_arr = np.dot(trans_arr.T, Kors_trans).T

    return vcg_arr