#!/usr/bin/env python
'''
Viewer for Fortran-datafile
'''

import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np

def create_layout():
    return [
        [sg.Text('N-body data viewer', size=(30, 1)),
         sg.InputText("Planeten-Nummer", key="time", size=(8,1)),
         sg.Ok(),
         sg.Cancel()]
        ]

layout = create_layout()
window = sg.Window("Viewer window",location=(100,100)).Layout(layout)

while True:
    event, values = window.read()
    print("=== event:", event, "===")
    if event in [None, "Cancel"]:
        break

print("Bye")
