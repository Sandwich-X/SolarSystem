
#!/usr/bin/env python
'''
Viewer for Fortran-datafile
'''

import PySimpleGUI       as sg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # eigentlich ab 3.2.0 nicht nötig
import numpy             as np
import os                # os.path.join

SOURCE_FILE = os.path.join("data", "coo.dat")

def create_layout():
    return [
        [sg.Text('N-body data viewer')],
        [sg.Frame(" File",
                  [[sg.Button("Read")]])],
        [sg.Frame(" Data ",
                  [[sg.Text("Planeten-Nummer:"), sg.InputText( "7", key="bodynr", size=(3,1))],
                   [sg.Text("x axis:"), sg.InputText("1", key="xnr", size=(3,1))], # combo !
                   [sg.Text("y axis:"), sg.InputText("2", key="ynr", size=(3,1))], # combo !
                   [sg.Text("z axis:"), sg.InputText("0", key="znr", size=(3,1))], # combo !
                  ])],
        [sg.Frame(" Plot ",
                  [[sg.Text("Number of last lines to show:"), sg.InputText("10", key="linesnr", size=(7,1)),
                    sg.Button("Show")]])],
        [sg.Cancel()],
        ]

layout = create_layout()
window = sg.Window("Viewer window",location=(200,200)).Layout(layout)

plt.ion()
while True:
    event, values = window.read()
    print("=== event:", event, "===")
    if event in [None, "Cancel"]:
        break
    if event == "Read":
        data = {}
        #         body    spalte2        spalte 3        spalte 5
        #data = {"1": [[1,2,3,4,5,....], [5,5,5,5,....], [....]]    ,
        #        "2": ...}
        with open(SOURCE_FILE) as sf:
            #--- 1st: check how many body(number)s and columns
            #         and create data:
            while True:
                line = sf.readline()
                if line[0] != "#":
                    break
                print("found comment line:", line)
            nam_cols = line.split() # NAMe of COLumns
            print("found headers:", line)
            print("nam_cols:", nam_cols)
            fields = sf.readline().split()  # data column
            num_cols = len(fields)
            while True:
                 #fields = sf.readline().split()   # data column
                 #num_cols = len(list1) # number of data columns in data file, including body
                 bodynr = fields[0] #
                 if bodynr not in data:
                     data[bodynr] = [[] for i in range(1,num_cols) ] # create empty lists
                 else:
                     for i in range(1, num_cols):
                         data[bodynr][i - 1].append(float(fields[i]))
                 line = sf.readline()
                 if line == "":
                     break
                 fields = line.split()  # data column
                 #print("fields:",fields)
        print("#bodies = len(data)          :", data.keys())
        print("#cols   = len(data[bodynr])   :", len(data[bodynr]))
        print("#data   = len(data[bodynr][0]):", len(data[bodynr][0]))
    
    if event == "Show":
        x_nr = int(values["xnr"])
        y_nr = int(values["ynr"])
        z_nr = int(values["znr"])
        dim3 = (z_nr != 0)  # 3D: 3-DIMensional
        print("dim3:   ", dim3)
        body_nr = values["bodynr"] # int(%)
        print("body_nr:", body_nr)
        #if len(data['x']) == 0 or len(data['y']) == 0:
        #    sg.Popup("No data read!")
        #    continue
        lines_nr = int(values["linesnr"])
        #input("-1-")
        visual_data = {'x':data[body_nr][int(values["xnr"])][-lines_nr:],
                       'y':data[body_nr][int(values["ynr"])][-lines_nr:],
                       'z':data[body_nr][int(values["znr"])][-lines_nr:]}
        #input("-2-")
        #print("len(visual_data['x']:",len(visual_data['x']))
        if dim3:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot(visual_data["x"],visual_data["y"],visual_data["z"], '.')
        else:
            plt.plot(visual_data["x"],visual_data["y"])
        #input("-3-")
        plt.show()
print("Bye")
