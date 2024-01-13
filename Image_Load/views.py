from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http.request import QueryDict
from django.http.response import JsonResponse
from Image_Load.tools.plot import paint_color
from Image_Load.tools.Find_Quadrant import Find_Quadrant
import json
import os
import numpy as np
# from django.http import JsonResponse
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
from djangoProject import settings

import argparse
from Image_Load.tools.patient import patient_data
from Image_Load.tools.patient import patient_data_NJ
from Image_Load.tools.patient import patient_data_2
from Image_Load.tools.patient import patient_data_3
from Image_Load.tools.patient import PatientDataJson


def login(request):
    # It seems like an analyzer，I'm not quite sure how it work，but I read the file successfully
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_dir', default="", help="Directory of the ECG XML file.")
    parser.add_argument('--save_dir', default="static/Img_From_File", help="Saved directory.")
    args = parser.parse_args(args=[])

    # args.file_dir = "D:/530/VCGtool/VCGtool/data/data.json"

    global patient

    if request.method == "POST":

        print("file:", request.FILES)
        type = request.POST.get('file_type')
        loadfile = request.FILES.get('upload')
        
        if loadfile is not None:
            filename = os.path.join(settings.BASE_DIR, "data",loadfile.name)
            with open(filename, 'wb') as f:
                # a_file.file 文件数据
                # a_file.file.read() 读出来
                data = loadfile.file.read()
                f.write(data)
        
        else:
            return HttpResponse("No file uploaded.")


        # read file which user uploaded
        if not loadfile:
            return HttpResponse("File not found")
            # Print 'file not found' while user didn't upload a readable file
        else:
            args.file_dir = filename
            if type == '0':
                try:
                    patient = patient_data(args)
                except:
                    return HttpResponse("Wrong File Type")

            elif type == '1':
                try:
                    print(args.file_dir)
                    patient = patient_data_NJ(args)
                except:
                    return HttpResponse("Wrong File Type")
            elif type == '2':
                try:
                    print(args.file_dir)
                    patient = patient_data_2(args)
                except:
                    return HttpResponse("Wrong File Type")
            elif type == '3':
                try:
                    print(args.file_dir)
                    patient = patient_data_3(args)
                except:
                    return HttpResponse("Wrong File Type")
            elif type == '4':
                # try:
                print(args.file_dir)
                patient = PatientDataJson(args)
                # except:
                #     return HttpResponse("Wrong File Type")

            patient.show_vcg()  # for the final figure
            return render(request, "login.html", context={'name': patient.name,
                                                          'pid': patient.pid,
                                                          'gender': patient.sex})
            # return everything that used in the front
    else:
        return render(request, "login.html", )  # Load Html File While Web request the page


def first(request):
    if request.is_ajax():  # Get Ajax Post
        global result
        points = json.loads(request.body)

        # points on canvas
        Onset_Of_QRS = points[0]["firstX"]
        R_Peak = points[1]["secondX"]
        Onset_Of_ST = points[2]["thirdX"]
        T_Peak = points[3]["fourthX"]
        T_End = points[4]["fifthX"]

        # resize the point to fit canvas
        resize = 1200 / 860
        Onset_Of_QRS = int(Onset_Of_QRS * resize)
        R_Peak = int(R_Peak * resize)
        Onset_Of_ST = int(Onset_Of_ST * resize)
        T_Peak = int(T_Peak * resize)
        T_End = int(T_End * resize)
        vm = np.sqrt(np.power(patient.vcg[0], 2) + np.power(patient.vcg[1], 2) + np.power(patient.vcg[2], 2))

        # calculate the points in space
        Onset_Of_QRS = int((Onset_Of_QRS / 1200) * len(vm))
        R_Peak = int((R_Peak / 1200) * len(vm))
        Onset_Of_ST = int((Onset_Of_ST / 1200) * len(vm))
        T_Peak = int((T_Peak / 1200) * len(vm))
        T_End = int((T_End / 1200) * len(vm))

        vcg = patient.vcg
        savedir = patient.save_dir

        # paint color and find quadrant
        paint_color(vcg, Onset_Of_QRS, R_Peak, Onset_Of_ST, T_Peak, T_End, fig_dir=os.path.join(savedir, 'Color_'))
        T_Peak_Quadrant = Find_Quadrant(patient.vcg, T_Peak)
        message1 = T_Peak_Quadrant[0]
        message2 = T_Peak_Quadrant[1]

        # save data as a dict
        # global result
        result = {'Onset_Of_QRS': [Onset_Of_QRS, vm[Onset_Of_QRS]],
                  'R_Peak': [R_Peak, vm[R_Peak]],
                  'Onset_Of_ST': [Onset_Of_ST, vm[Onset_Of_ST]],
                  'T_Peak': [T_Peak, vm[T_Peak]],
                  'T_End': [T_End, vm[T_End]],
                  'message1': message1,
                  'message2': message2
                  }
        # when everything ready,use this to create json file
        with open('static/Result_File/Result.json', 'w') as save:
            json.dump(result, save)

        return HttpResponse("Successfully get json file")  # A test return

    return render(request, "first.html")


def second(request):
    return render(request, "second.html", context={'message1': result['message1'], 'message2': result['message2']})


def second_without_label(request):
    return render(request, "secondTwo.html", context={'msg1': result['message1'], 'msg2': result['message2']})
