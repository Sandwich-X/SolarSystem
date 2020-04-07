
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
        #data = {"x":[], "y":[], "z":[]}
        x_nr = int(values["xnr"])
        y_nr = int(values["ynr"])
        z_nr = int(values["znr"])
        dim3 = (z_nr != 0) # 3D: 3-DIMensional
        print("dim3:   ", dim3)
        #counter = 0
        with open(SOURCE_FILE) as sf:
            #--- 1st: check how many body(number)s and columns
            #         and create data:
            for i in range(5): # 0..4 # 5 commentary lines at beginning
                print("i:", i, sf.readline())
            nam_cols = sf.readline().split() # NAMe of COLumns
            print("nam_cols:", nam_cols)
            line1 = sf.readline().split()
            num_cols = len(line1)
            print("line1:", line1)
            print("num_cols:", num_cols)
            body1 = line1[0]
            num_bodies = 1
            nam_bodies = [body1]
            print("body1:", body1)
            data[body1] = [[] for i in range(1,num_cols) ]
            print("data:", data)
            while True:
                body_nr = sf.readline().split()[0]
                if body_nr == body1:
                    break # while True
                data[body_nr] = [[] for i in range(len(line1)-1) ]
                num_bodies += 1
                nam_bodies += body_nr
            print("data:", data)
            print("num_bodies:", num_bodies)
            print("nam_bodies:", nam_bodies)
            input()
            #--- 2nd: rewind and read all data:
            sf.seek(0)
            for number, line in enumerate(sf):
                #print("number:", number)
                #print("line:", line)
                #input()
                if number < 6: # 1st 5 lines commentary
                    continue
                fields = line.split() # separation by any whitespace
                #print("fields:", fields)
                #input()
                #counter += 1
                #print(f"Got {counter}. datapoint:")
                #print(" x-value:", fields[x_nr])
                #print(" y-value:", fields[y_nr])
                for i in range(1,num_cols):
                    data[fields[0]][i-1].append(float(fields[i]))
                #data[body_nr][y_nr-1].append(float(fields[y_nr]))
                #if dim3:
                    #data[body_nr][z_nr].append(float(fields[z_nr]))
                    #print(" z-value:", fields[z_nr])
                #print("data:", data)
                #input()
            #end for
        #end with
        #input()
        print("#bodies = len(data)          :", len(data))
        print("#cols   = len(data[body1])   :", len(data[body1]))
        print("#data   = len(data[body1][0]):", len(data[body1][0]))
    if event == "Show":
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
