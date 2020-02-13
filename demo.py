#!/usr/bin/env python
'''
Example of (almost) all widgets, that you can use in PySimpleGUI.
'''

import PySimpleGUI as sg
import os
import random

class Planet():
    ''' Planet for the Solar system ... '''

    def __init__(self, name, symbol="Symbol", image=None, mass=1, a=1, e=0, i=0, O=0, o=0, t=0):
        self.name   = name
        self.symbol = symbol
        self.image  = image
        self.mass   = mass
        self.a = a
        self.e = e
        self.i = i
        self.O = O
        self.o = o
        self.t = t

    def __repr__(self):
        return self.name

sandwich_planets = []
default_planets = []
#for planetname in ["Merkur", "Venus", "Erde", "Mars", "Jupiter", "Saturn", "Uranus", "Neptun", "Pluto"]:
default_planets.append(Planet("Sun", image="sun.png"))
default_planets.append(Planet("Merkur", image="merkur.png"))
default_planets.append(Planet("Venus",  image="merkur.png"))
default_planets.append(Planet("Erde",   image="erde.png"))
default_planets.append(Planet("Mars",   image="mars.png"))
default_planets.append(Planet("Jupiter",image="jupiter.png"))
default_planets.append(Planet("Saturn", image="saturn.png"))
default_planets.append(Planet("Uranus", image="uranus.png"))
default_planets.append(Planet("Neptun", image="neptun.png"))
default_planets.append(Planet("Pluto",  image="pluto.png"))

print(default_planets)

mypics = []
for root, dirs, files in os.walk("."):
    # print(files)
    for f in files:
        if f[-4:] == ".png":
            mypics.append(os.path.join(root, f))
print("meine bilder mit pfad:")
print(mypics)

col1 = sg.Column(key="planet1", layout=[[sg.Text('la la la', key="text1"), ],
                                        [sg.Image(filename="saturn.png")],
                                         [sg.Text("a"), sg.InputText(key="a1", size=(4, 1)),
                                         sg.Text("e"), sg.InputText(key="e1", size=(4, 1)),
                                         sg.Text("i"), sg.InputText(key="i1", size=(4, 1))],
                                        [sg.Text("O"), sg.InputText(key="O1", size=(4, 1)),
                                         sg.Text("o"), sg.InputText(key="o1", size=(4, 1)),
                                         sg.Text("t"), sg.InputText(key="t1", size=(4, 1))],


                                        ])

#[sg.ProgressBar(100, orientation='h', size=(20, 20),
#                key='progressbar')],
## [sg.Listbox(default_planets,key="listbox", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
##                size=(10, 10)),
cols = []
for p in default_planets:
    print(p.name)
    cols.append(  sg.Col(layout=[[sg.Button( p.name, tooltip=p.name, image_filename=os.path.join("data",p.name.lower()+".png"), image_subsample=3, border_width=0, button_color=("black" if p.name == "sun" else "yellow",None) )],
                             [sg.Checkbox(text="",default=True, key="c_" + p.name.lower())]]) )


layout = [

    [sg.Text('Planeten Sandwich Solar System', size=(30, 1))],
    cols,

    [sg.InputText('This is my text')],
    [sg.Combo(values=default_planets,key="selectPlanets"),
     sg.Button("übernehmen")],
    [sg.Text('Verwendete Planeten:')],
    [sg.Text("nothing", key="usedPlanets", size=(10,10))],
    [sg.Button("ok"), sg.Cancel()]]

window = sg.Window('sss', layout)
#progress_bar = window['progressbar']
i = 1
while True:
    event, values = window.read()
    if event in [None, "Cancel"]:
        break
    print(event, values)
    #print(window["text1"].__dict__)
    #if event == "next" or event == "bild1":
    #    window["bild1"].update(image_filename="vortrag.png")
    if event == "übernehmen":
        window["usedPlanets"].update(values["selectPlanets"])
    if event in [p.name for p in default_planets]:
        window["c_"+event.lower()].update(not values["c_"+event.lower()])

print("Bye")
