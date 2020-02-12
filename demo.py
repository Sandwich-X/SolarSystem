#!/usr/bin/env python
'''
Example of (almost) all widgets, that you can use in PySimpleGUI.
'''

import PySimpleGUI as sg
import os
import random

mypics = []
for root, dirs, files in os.walk("."):
    # print(files)
    for f in files:
        if f[-4:] == ".png":
            mypics.append(os.path.join(root, f))
print("meine bilder mit pfad:")
print(mypics)

#[sg.Button(key="bild1", button_color=sg.TRANSPARENT_BUTTON,
#           image_filename="saturn.png")],


#[sg.Text("x"), sg.InputText(key="x1", size=(4, 1)),
# sg.Text("y"), sg.InputText(key="y1", size=(4, 1)),
# sg.Text("z"), sg.InputText(key="z1", size=(4, 1)), ],
#[sg.Text("u"), sg.InputText(key="u1", size=(4, 1)),
# sg.Text("v"), sg.InputText(key="v1", size=(4, 1)),
# sg.Text("w"), sg.InputText(key="w1", size=(4, 1))],

col1 = sg.Column(key="planet1", layout=[[sg.Text('la la la', key="text1"), ],
                                        [sg.Image(filename="saturn.png")],
                                         [sg.Text("a"), sg.InputText(key="a1", size=(4, 1)),
                                         sg.Text("e"), sg.InputText(key="e1", size=(4, 1)),
                                         sg.Text("i"), sg.InputText(key="i1", size=(4, 1))],
                                        [sg.Text("O"), sg.InputText(key="O1", size=(4, 1)),
                                         sg.Text("o"), sg.InputText(key="o1", size=(4, 1)),
                                         sg.Text("t"), sg.InputText(key="t1", size=(4, 1))],

                                        ])

col2 = sg.Column(key="planet2", layout=[[sg.Text('la la la', key="text2"), ],
                                        [sg.Button(key="bild1", button_color=sg.TRANSPARENT_BUTTON,
                                                   image_filename="venus.png")], ])

#[sg.ProgressBar(100, orientation='h', size=(20, 20),
#                key='progressbar')],

layout = [

    [sg.Text('Planeten Sandwich Solar System', size=(30, 1))],
    [sg.InputText('This is my text')],
    [col1],
    [sg.Button("ok"), sg.Cancel()]]

window = sg.Window('Vokabeltrainer', layout)
#progress_bar = window['progressbar']
i = 1
while True:
    event, values = window.read()
    if event in [None, "Cancel"]:
        break
    print(event, values)
    print(window["text1"].__dict__)
    #if event == "next" or event == "bild1":
    #    window["bild1"].update(image_filename="vortrag.png")
    if event == "random":
        bi = random.choice(mypics)
        window["bild1"].update(image_filename=bi + ".png")
        window["text1"].update(bi)
#    if event == "good":
#        i += 1
#        progress_bar.UpdateBar(i)

print("Bye")

