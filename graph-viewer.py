#!/usr/bin/env python
'''
Viewer for Fortran-datafile
'''

import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
import os          # os.path.join , os.walk

SOURCE_FILE = os.path.join("data", "coo.dat")

def create_layout():
    return [
        [sg.Text('N-body data viewer')],
        [sg.Text("Planeten-Nummer:"),
         sg.InputText("7", key="bodynr", size=(3,1))],
        [sg.Text("Number of last lines:"),
         sg.InputText("7", key="linesnr", size=(3,1))],
        [sg.Text("x:"),
         sg.InputText("1", key="xnr", size=(3,1))], # combo !
        [sg.Text("y:"),
         sg.InputText("2", key="ynr", size=(3,1))], # combo !
        [sg.Text("z:"),
         sg.InputText("0", key="znr", size=(3,1))], # combo !
        [sg.Ok(),
         sg.Cancel()]
        ]

layout = create_layout()
window = sg.Window("Viewer window",location=(100,100)).Layout(layout)

cols = "xyz"

while True:
    event, values = window.read()
    print("=== event:", event, "===")
    if event in [None, "Cancel"]:
        break
    if event == "Ok":
        data = {"x":[], "y":[], "z":[]}
        with open(SOURCE_FILE) as f:
            for number, line in enumerate(f):
                #print("number:", number)
                #print("line:", line)
                if number < 7:
                    continue
                fields = line.split(" ")
                print("fields:", fields)
                counter = -1
                for field in fields:
                    print("field:", field)
                    input()
                    if field == "":
                        continue
                    counter += 1
                    print("counter1:", counter)
                    input()
                    if counter == 0: # = body-nr spalte
                        if int(field) != int(values["bodynr"]):
                            break # inner for-loop
                    print("counter2:", counter)
                    input()
                    if   counter == int(values["xnr"]):
                        data["x"].append(float(field))
                    elif counter == int(values["ynr"]):
                        data["y"].append(float(field))
                    elif counter == int(values["znr"]):
                        data["z"].append(float(field))
        #input()
        print("data:", data)
                    
                        

print("Bye")
