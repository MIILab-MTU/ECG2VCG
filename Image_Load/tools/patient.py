# -*- coding: utf-8 -*-"
"""
Created on 05/03/2021  11:04 AM
Patient class

@author: Zhuo
"""
import os
import numpy as np
from scipy import integrate
from xml.etree import ElementTree as ET
from xml.dom import minidom as md
from Image_Load.tools.ecg_helpFunc import decode64base_ECG, calculateVCG, to_array
from Image_Load.tools.plot import plot_12ecgs, plot_vcg_XYZandVM, plot_vcg_blue, paint_color
import json
from djangoProject import settings
from pathlib import Path



names = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']


def align_ecg_signal(signal, lenght):
    zero_idx = np.where(signal == 0)[0][0]
    align_signal = signal[zero_idx:lenght]
    return align_signal


# class with patient information
class patient_data:
    """Philips ECG"""
    def __init__(self, args):
        self.path = args.file_dir
        self.save_dir = args.save_dir

        tree = ET.parse(self.path)
        children = list(tree.getroot())
        # patient information
        for i in range(0, 7):
            if len(children[5][0][i]) == 0:
                if '}patientid' in children[5][0][i].tag:
                    self.pid = children[5][0][i].text
                elif 'sex' in children[5][0][i].tag:
                    self.sex = children[5][0][i].text
                else:
                    pass
            else:
                if 'name' in children[5][0][i][0].tag:
                    self.name = children[5][0][i][0].text
                elif 'dateofbirth' in children[5][0][i][0].tag:
                    self.dob = children[5][0][i][0].text
                else:
                    pass

                # date information
                self.date = children[4].attrib['date']

                # sampling rate
                self.sampling_rate = children[4][2][0].text

                # meanQRSdur
                self.meanqrsdur = children[6][0][29].text

                self.i = decode64base_ECG(children[8][1][0][6].text)
                self.ii = decode64base_ECG(children[8][1][1][6].text)
                self.iii = decode64base_ECG(children[8][1][2][6].text)
                self.aVR = decode64base_ECG(children[8][1][3][6].text)
                self.aVL = decode64base_ECG(children[8][1][4][6].text)
                self.aVF = decode64base_ECG(children[8][1][5][6].text)
                self.v1 = decode64base_ECG(children[8][1][6][6].text)
                self.v2 = decode64base_ECG(children[8][1][7][6].text)
                self.v3 = decode64base_ECG(children[8][1][8][6].text)
                self.v4 = decode64base_ECG(children[8][1][9][6].text)
                self.v5 = decode64base_ECG(children[8][1][10][6].text)
                self.v6 = decode64base_ECG(children[8][1][11][6].text)

                # self.longECG = decode64base_ECG(children[8][0].text)

                self.ecg = np.concatenate((self.i, self.ii, self.iii, self.aVR, self.aVL, self.aVF,
                                           self.v1, self.v2, self.v3, self.v4, self.v5, self.v6), axis=0).reshape(
                    (12, 1200))

                self.trans = np.concatenate((self.v1, self.v2, self.v3, self.v4, self.v5, self.v6,
                                             self.i, self.ii), axis=0).reshape((8, 1200))

                self.vcg = calculateVCG(self.trans)
                _x_vcg = self.vcg[0]
                _y_vcg = self.vcg[1]
                _z_vcg = self.vcg[2]

                # save ecg images
                plot_12ecgs(self.ecg, show_fig=False,
                            fig_dir=os.path.join(self.save_dir, 'Standard_12_ECG.png'))
                # fig_dir=os.path.join(args.save_dir, '{}_{}_ecg.png'.format(self.pid, self.date)))

                # save vcg images (X, Y, Z)
                plot_vcg_XYZandVM(self.vcg, fig_dir=os.path.join(self.save_dir, 'VCG_'), show_fig=False)

    def show_vcg(self):
        plot_vcg_blue(self.vcg, show_fig=False, fig_dir=os.path.join(self.save_dir, 'VCG_'))


class patient_data_2:
    """Philips ECG FDA Template"""
    def __init__(self, args):
        self.path = args.file_dir
        self.save_dir = args.save_dir
        self.name = "unknown"
        self.pid = "unknown"
        self.sex = "unknown"
        tree = ET.parse(self.path)
        children = list(tree.getroot())

        # short ecg data:

        self.i = to_array(children[16][0][10][0][4][0][1][0][1][2].text)
        self.ii = to_array(children[16][0][10][0][4][0][2][0][1][2].text)
        self.iii = to_array(children[16][0][10][0][4][0][3][0][1][2].text)
        self.aVR = to_array(children[16][0][10][0][4][0][4][0][1][2].text)
        self.aVL = to_array(children[16][0][10][0][4][0][5][0][1][2].text)
        self.aVF = to_array(children[16][0][10][0][4][0][6][0][1][2].text)
        self.v1 = to_array(children[16][0][10][0][4][0][7][0][1][2].text)
        self.v2 = to_array(children[16][0][10][0][4][0][8][0][1][2].text)
        self.v3 = to_array(children[16][0][10][0][4][0][9][0][1][2].text)
        self.v4 = to_array(children[16][0][10][0][4][0][10][0][1][2].text)
        self.v5 = to_array(children[16][0][10][0][4][0][11][0][1][2].text)
        self.v6 = to_array(children[16][0][10][0][4][0][12][0][1][2].text)

        self.ecg = np.concatenate((self.i, self.ii, self.iii, self.aVR, self.aVL, self.aVF,
                                   self.v1, self.v2, self.v3, self.v4, self.v5, self.v6), axis=0).reshape((12, -1))

        self.trans = np.concatenate((self.v1, self.v2, self.v3, self.v4, self.v5, self.v6,
                                     self.i, self.ii), axis=0).reshape((8, -1))
        self.vcg = calculateVCG(self.trans)
        _x_vcg = self.vcg[0]
        _y_vcg = self.vcg[1]
        _z_vcg = self.vcg[2]

        # save ecg images
        plot_12ecgs(self.ecg, show_fig=False,
                    fig_dir=os.path.join(self.save_dir, 'Standard_12_ECG.png'))
        # fig_dir=os.path.join(args.save_dir, '{}_{}_ecg.png'.format(self.pid, self.date)))

        # save vcg images (X, Y, Z)
        plot_vcg_XYZandVM(self.vcg, fig_dir=os.path.join(self.save_dir, 'VCG_'), show_fig=False)

    def show_vcg(self):
        plot_vcg_blue(self.vcg, show_fig=False, fig_dir=os.path.join(self.save_dir, 'VCG_'))


class patient_data_3:
    """Philips ECG FDA Template SPECIAL"""
    def __init__(self, args):
        self.path = args.file_dir
        self.save_dir = args.save_dir
        self.name = "unknown"
        self.pid = "unknown"
        self.sex = "unknown"
        tree = ET.parse(self.path)
        children = list(tree.getroot())

        # short ecg data:

        self.i = to_array(children[15][0][10][0][4][0][1][0][1][2].text)
        self.ii = to_array(children[15][0][10][0][4][0][2][0][1][2].text)
        self.iii = to_array(children[15][0][10][0][4][0][3][0][1][2].text)
        self.aVR = to_array(children[15][0][10][0][4][0][4][0][1][2].text)
        self.aVL = to_array(children[15][0][10][0][4][0][5][0][1][2].text)
        self.aVF = to_array(children[15][0][10][0][4][0][6][0][1][2].text)
        self.v1 = to_array(children[15][0][10][0][4][0][7][0][1][2].text)
        self.v2 = to_array(children[15][0][10][0][4][0][8][0][1][2].text)
        self.v3 = to_array(children[15][0][10][0][4][0][9][0][1][2].text)
        self.v4 = to_array(children[15][0][10][0][4][0][10][0][1][2].text)
        self.v5 = to_array(children[15][0][10][0][4][0][11][0][1][2].text)
        self.v6 = to_array(children[15][0][10][0][4][0][12][0][1][2].text)

        self.ecg = np.concatenate((self.i, self.ii, self.iii, self.aVR, self.aVL, self.aVF,
                                   self.v1, self.v2, self.v3, self.v4, self.v5, self.v6), axis=0).reshape((12, -1))

        self.trans = np.concatenate((self.v1, self.v2, self.v3, self.v4, self.v5, self.v6,
                                     self.i, self.ii), axis=0).reshape((8, -1))
        self.vcg = calculateVCG(self.trans)
        _x_vcg = self.vcg[0]
        _y_vcg = self.vcg[1]
        _z_vcg = self.vcg[2]

        # save ecg images
        plot_12ecgs(self.ecg, show_fig=False,
                    fig_dir=os.path.join(self.save_dir, 'Standard_12_ECG.png'))
        # fig_dir=os.path.join(args.save_dir, '{}_{}_ecg.png'.format(self.pid, self.date)))

        # save vcg images (X, Y, Z)
        plot_vcg_XYZandVM(self.vcg, fig_dir=os.path.join(self.save_dir, 'VCG_'), show_fig=False)

    def show_vcg(self):
        plot_vcg_blue(self.vcg, show_fig=False, fig_dir=os.path.join(self.save_dir, 'VCG_'))


class patient_data_NJ:
    """NL ECGToolkit"""
    def __init__(self, args):
        self.path = args.file_dir
        self.save_dir = args.save_dir
        print("===========", self.path)
        print("===========", args.save_dir)
        self.name = "unknown"
        self.pid = "unknown"
        self.sex = "unknown"
        tree = ET.parse(self.path)
        print("=========== Done with loading file")
        children = list(tree.getroot())

        self.i = to_array(children[6][0][11][0][4][0][1][0][1][2].text)
        self.ii = to_array(children[6][0][11][0][4][0][2][0][1][2].text)
        self.iii = to_array(children[6][0][11][0][4][0][3][0][1][2].text)
        self.aVR = to_array(children[6][0][11][0][4][0][4][0][1][2].text)
        self.aVL = to_array(children[6][0][11][0][4][0][5][0][1][2].text)
        self.aVF = to_array(children[6][0][11][0][4][0][6][0][1][2].text)
        self.v1 = to_array(children[6][0][11][0][4][0][7][0][1][2].text)
        self.v2 = to_array(children[6][0][11][0][4][0][8][0][1][2].text)
        self.v3 = to_array(children[6][0][11][0][4][0][9][0][1][2].text)
        self.v4 = to_array(children[6][0][11][0][4][0][10][0][1][2].text)
        self.v5 = to_array(children[6][0][11][0][4][0][11][0][1][2].text)
        self.v6 = to_array(children[6][0][11][0][4][0][12][0][1][2].text)

        self.ecg = np.concatenate((self.i, self.ii, self.iii, self.aVR, self.aVL, self.aVF,
                                   self.v1, self.v2, self.v3, self.v4, self.v5, self.v6), axis=0).reshape((12, -1))

        self.trans = np.concatenate((self.v1, self.v2, self.v3, self.v4, self.v5, self.v6,
                                     self.i, self.ii), axis=0).reshape((8, -1))
        self.vcg = calculateVCG(self.trans)
        _x_vcg = self.vcg[0]
        _y_vcg = self.vcg[1]
        _z_vcg = self.vcg[2]

        # save ecg images
        plot_12ecgs(self.ecg, show_fig=False,
                    fig_dir=os.path.join(self.save_dir, 'Standard_12_ECG.png'))
        # fig_dir=os.path.join(args.save_dir, '{}_{}_ecg.png'.format(self.pid, self.date)))

        # save vcg images (X, Y, Z)
        plot_vcg_XYZandVM(self.vcg, fig_dir=os.path.join(self.save_dir, 'VCG_'), show_fig=False)

    def show_vcg(self):
        plot_vcg_blue(self.vcg, show_fig=False, fig_dir=os.path.join(self.save_dir, 'VCG_'))


class PatientDataJson():
    def __init__(self, args):

        self.path = str(args.file_dir)
        self.save_dir = args.save_dir
        self.name = "unknown"
        self.pid = "unknown"
        self.sex = "unknown"


        # print("===========", self.path)
        # print("===========", args.save_dir)


        # file = open(self.path, "r")
        # print("=========== Done with open file")
        # data = json.load(file)
        # file.close()
        with open(os.path.join(settings.BASE_DIR, "data", self.path)) as json_file:
            data = json.load(json_file)

        print("=========== Done with loading data")
        png_name = list(data)[0]

        self.i = np.array(data[png_name][0]['v_array'])
        self.ii = np.array(data[png_name][1]['v_array'])
        self.iii = np.array(data[png_name][2]['v_array'])
        self.aVR = np.array(data[png_name][3]['v_array'])
        self.aVL = np.array(data[png_name][4]['v_array'])
        self.aVF = np.array(data[png_name][5]['v_array'])
        self.v1 = np.array(data[png_name][6]['v_array'])
        self.v2 = np.array(data[png_name][7]['v_array'])
        self.v3 = np.array(data[png_name][8]['v_array'])
        self.v4 = np.array(data[png_name][9]['v_array'])
        self.v5 = np.array(data[png_name][10]['v_array'])
        self.v6 = np.array(data[png_name][11]['v_array'])

        min_len = min(len(self.i), len(self.ii), len(self.iii), len(self.aVR), len(self.aVL), len(self.aVF),
                      len(self.v1), len(self.v2), len(self.v3), len(self.v4), len(self.v5), len(self.v6))

        self.i = align_ecg_signal(self.i, min_len)
        self.ii = align_ecg_signal(self.ii, min_len)
        self.iii = align_ecg_signal(self.iii, min_len)
        self.aVR = align_ecg_signal(self.aVR, min_len)
        self.aVL = align_ecg_signal(self.aVL, min_len)
        self.aVF = align_ecg_signal(self.aVF, min_len)
        self.v1 = align_ecg_signal(self.v1, min_len)
        self.v2 = align_ecg_signal(self.v2, min_len)
        self.v3 = align_ecg_signal(self.v3, min_len)
        self.v4 = align_ecg_signal(self.v4, min_len)
        self.v5 = align_ecg_signal(self.v5, min_len)
        self.v6 = align_ecg_signal(self.v6, min_len)
        print("JSON format")

        self.ecg = np.concatenate((self.i, self.ii, self.iii, self.aVR, self.aVL, self.aVF,
                                   self.v1, self.v2, self.v3, self.v4, self.v5, self.v6), axis=0).reshape(
            (12, -1))

        self.trans = np.concatenate((self.v1, self.v2, self.v3, self.v4, self.v5, self.v6,
                                     self.i, self.ii), axis=0).reshape((8, -1))

        # Calculate ECG
        self.vcg = calculateVCG(self.trans)
        _x_vcg = self.vcg[0]
        _y_vcg = self.vcg[1]
        _z_vcg = self.vcg[2]

        print("=========== Done with calculate VCG")

        # save ecg images
        plot_12ecgs(self.ecg, show_fig=False,
                    fig_dir=os.path.join(self.save_dir, 'Standard_12_ECG.png'))
        # fig_dir=os.path.join(args.save_dir, '{}_{}_ecg.png'.format(self.pid, self.date)))

        # save vcg images (X, Y, Z)
        plot_vcg_XYZandVM(self.vcg, fig_dir=os.path.join(self.save_dir, 'VCG_'), show_fig=False)

    def show_vcg(self):
        plot_vcg_blue(self.vcg, show_fig=False, fig_dir=os.path.join(self.save_dir, 'VCG_'))


# class PatientData():
#     def __init__(self, args, json=True):
#         self.path = str(args.file_dir)
#         self.save_dir = args.save_dir
#         self.name = "unknown"
#         self.pid = "unknown"
#         self.sex = "unknown"
#
#         if json:
#             print("===========", self.name)
#             print("===========", self.path)
#             print("===========", args.file_dir)
#             assert self.path.endswith('.json')
#             self._json_format()
#         else:
#             assert self.path.endswith('.xml')
#             try:
#                 self._xml_format_1()
#             except:
#                 try:
#                     self._xml_format_2()
#                 except:
#                     try:
#                         self._xml_format_3()
#                     except:
#                         try:
#                             self._xml_format_4()
#                         except ValueError:
#                             print("Unsupported XML file.")
#
#         self.ecg = np.concatenate((self.i, self.ii, self.iii, self.aVR, self.aVL, self.aVF,
#                                    self.v1, self.v2, self.v3, self.v4, self.v5, self.v6), axis=0).reshape(
#             (12, -1))
#
#         self.trans = np.concatenate((self.v1, self.v2, self.v3, self.v4, self.v5, self.v6,
#                                      self.i, self.ii), axis=0).reshape((8, -1))
#
#         # Calculate ECG
#         self.vcg = calculateVCG(self.trans)
#         _x_vcg = self.vcg[0]
#         _y_vcg = self.vcg[1]
#         _z_vcg = self.vcg[2]
#
#         # save ecg images
#         plot_12ecgs(self.ecg, show_fig=False,
#                     fig_dir=os.path.join(self.save_dir, 'Standard_12_ECG.png'))
#         # fig_dir=os.path.join(args.save_dir, '{}_{}_ecg.png'.format(self.pid, self.date)))
#
#         # save vcg images (X, Y, Z)
#         plot_vcg_XYZandVM(self.vcg, fig_dir=os.path.join(self.save_dir, 'VCG_'), show_fig=False)
#
#     def show_vcg(self):
#         plot_vcg_blue(self.vcg, show_fig=False, fig_dir=os.path.join(self.save_dir, 'VCG_'))
#
#     def _json_format(self):
#         file = open(self.path)
#         data = json.load(file)
#
#         png_name = list(data)[0]
#
#         self.i = np.array(data[png_name][0]['v_array'])
#         self.ii = np.array(data[png_name][1]['v_array'])
#         self.iii = np.array(data[png_name][2]['v_array'])
#         self.aVR = np.array(data[png_name][3]['v_array'])
#         self.aVL = np.array(data[png_name][4]['v_array'])
#         self.aVF = np.array(data[png_name][5]['v_array'])
#         self.v1 = np.array(data[png_name][6]['v_array'])
#         self.v2 = np.array(data[png_name][7]['v_array'])
#         self.v3 = np.array(data[png_name][8]['v_array'])
#         self.v4 = np.array(data[png_name][9]['v_array'])
#         self.v5 = np.array(data[png_name][10]['v_array'])
#         self.v6 = np.array(data[png_name][11]['v_array'])
#
#         min_len = min(len(self.i), len(self.ii), len(self.iii), len(self.aVR), len(self.aVL), len(self.aVF),
#                       len(self.v1), len(self.v2), len(self.v3), len(self.v4), len(self.v5), len(self.v6))
#
#         self.i = align_ecg_signal(self.i, min_len)
#         self.ii = align_ecg_signal(self.ii, min_len)
#         self.iii = align_ecg_signal(self.iii, min_len)
#         self.aVR = align_ecg_signal(self.aVR, min_len)
#         self.aVL = align_ecg_signal(self.aVL, min_len)
#         self.aVF = align_ecg_signal(self.aVF, min_len)
#         self.v1 = align_ecg_signal(self.v1, min_len)
#         self.v2 = align_ecg_signal(self.v2, min_len)
#         self.v3 = align_ecg_signal(self.v3, min_len)
#         self.v4 = align_ecg_signal(self.v4, min_len)
#         self.v5 = align_ecg_signal(self.v5, min_len)
#         self.v6 = align_ecg_signal(self.v6, min_len)
#         print("JSON format")
#
#     def _xml_format_1(self):
#         tree = ET.parse(self.path)
#         children = list(tree.getroot())
#         # patient information
#         for i in range(0, 7):
#             if len(children[5][0][i]) == 0:
#                 if '}patientid' in children[5][0][i].tag:
#                     self.pid = children[5][0][i].text
#                 elif 'sex' in children[5][0][i].tag:
#                     self.sex = children[5][0][i].text
#                 else:
#                     pass
#             else:
#                 if 'name' in children[5][0][i][0].tag:
#                     self.name = children[5][0][i][0].text
#                 elif 'dateofbirth' in children[5][0][i][0].tag:
#                     self.dob = children[5][0][i][0].text
#                 else:
#                     pass
#
#             # date information
#             self.date = children[4].attrib['date']
#
#             # sampling rate
#             self.sampling_rate = children[4][2][0].text
#
#             # meanQRSdur
#             self.meanqrsdur = children[6][0][29].text
#
#             self.i = decode64base_ECG(children[8][1][0][6].text)
#             self.ii = decode64base_ECG(children[8][1][1][6].text)
#             self.iii = decode64base_ECG(children[8][1][2][6].text)
#             self.aVR = decode64base_ECG(children[8][1][3][6].text)
#             self.aVL = decode64base_ECG(children[8][1][4][6].text)
#             self.aVF = decode64base_ECG(children[8][1][5][6].text)
#             self.v1 = decode64base_ECG(children[8][1][6][6].text)
#             self.v2 = decode64base_ECG(children[8][1][7][6].text)
#             self.v3 = decode64base_ECG(children[8][1][8][6].text)
#             self.v4 = decode64base_ECG(children[8][1][9][6].text)
#             self.v5 = decode64base_ECG(children[8][1][10][6].text)
#             self.v6 = decode64base_ECG(children[8][1][11][6].text)
#             print("XML format 1")
#
#     def _xml_format_2(self):
#         tree = ET.parse(self.path)
#         children = list(tree.getroot())
#
#         # short ecg data:
#
#         self.i = to_array(children[16][0][10][0][4][0][1][0][1][2].text)
#         self.ii = to_array(children[16][0][10][0][4][0][2][0][1][2].text)
#         self.iii = to_array(children[16][0][10][0][4][0][3][0][1][2].text)
#         self.aVR = to_array(children[16][0][10][0][4][0][4][0][1][2].text)
#         self.aVL = to_array(children[16][0][10][0][4][0][5][0][1][2].text)
#         self.aVF = to_array(children[16][0][10][0][4][0][6][0][1][2].text)
#         self.v1 = to_array(children[16][0][10][0][4][0][7][0][1][2].text)
#         self.v2 = to_array(children[16][0][10][0][4][0][8][0][1][2].text)
#         self.v3 = to_array(children[16][0][10][0][4][0][9][0][1][2].text)
#         self.v4 = to_array(children[16][0][10][0][4][0][10][0][1][2].text)
#         self.v5 = to_array(children[16][0][10][0][4][0][11][0][1][2].text)
#         self.v6 = to_array(children[16][0][10][0][4][0][12][0][1][2].text)
#         print("XML format 2")
#
#     def _xml_format_3(self):
#         tree = ET.parse(self.path)
#         children = list(tree.getroot())
#
#         # short ecg data:
#
#         self.i = to_array(children[15][0][10][0][4][0][1][0][1][2].text)
#         self.ii = to_array(children[15][0][10][0][4][0][2][0][1][2].text)
#         self.iii = to_array(children[15][0][10][0][4][0][3][0][1][2].text)
#         self.aVR = to_array(children[15][0][10][0][4][0][4][0][1][2].text)
#         self.aVL = to_array(children[15][0][10][0][4][0][5][0][1][2].text)
#         self.aVF = to_array(children[15][0][10][0][4][0][6][0][1][2].text)
#         self.v1 = to_array(children[15][0][10][0][4][0][7][0][1][2].text)
#         self.v2 = to_array(children[15][0][10][0][4][0][8][0][1][2].text)
#         self.v3 = to_array(children[15][0][10][0][4][0][9][0][1][2].text)
#         self.v4 = to_array(children[15][0][10][0][4][0][10][0][1][2].text)
#         self.v5 = to_array(children[15][0][10][0][4][0][11][0][1][2].text)
#         self.v6 = to_array(children[15][0][10][0][4][0][12][0][1][2].text)
#         print("XML format 3")
#
#     def _xml_format_4(self):
#         tree = ET.parse(self.path)
#         children = list(tree.getroot())
#
#         self.i = to_array(children[6][0][11][0][4][0][1][0][1][2].text)
#         self.ii = to_array(children[6][0][11][0][4][0][2][0][1][2].text)
#         self.iii = to_array(children[6][0][11][0][4][0][3][0][1][2].text)
#         self.aVR = to_array(children[6][0][11][0][4][0][4][0][1][2].text)
#         self.aVL = to_array(children[6][0][11][0][4][0][5][0][1][2].text)
#         self.aVF = to_array(children[6][0][11][0][4][0][6][0][1][2].text)
#         self.v1 = to_array(children[6][0][11][0][4][0][7][0][1][2].text)
#         self.v2 = to_array(children[6][0][11][0][4][0][8][0][1][2].text)
#         self.v3 = to_array(children[6][0][11][0][4][0][9][0][1][2].text)
#         self.v4 = to_array(children[6][0][11][0][4][0][10][0][1][2].text)
#         self.v5 = to_array(children[6][0][11][0][4][0][11][0][1][2].text)
#         self.v6 = to_array(children[6][0][11][0][4][0][12][0][1][2].text)
#         print("XML format 4")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_dir', default="", help="Directory of the ECG XML file.")
    parser.add_argument('--save_dir', default="static/Img_From_File", help="Saved directory.")
    args = parser.parse_args(args=[])

    args.file_dir = "/data.json"
    args.save_dir = "/home/zhuo/disk/zhuo/VCGtool/static/Img_From_File"

    data = PatientDataJson(args)
    data.show_vcg()

