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
default_planets = {}
#for planetname in ["Sun", "Merkur", "Venus", "Erde", "Mars", "Jupiter", "Saturn", "Uranus", "Neptun", "Pluto"]:
default_planets["Sun"] = Planet("Sun", image=os.path.join("data", "sun.png"), mass=1500)
default_planets["Merkur"] = Planet("Merkur", image=os.path.join("data","merkur.png"), mass=2)
default_planets["Venus"] = Planet("Venus",  image=os.path.join("data","venus.png"), mass=3)
default_planets["Earth"] = Planet("Earth",   image=os.path.join("data","erde.png"), mass=4)
default_planets["Mars"] = Planet("Mars",   image=os.path.join("data","mars.png"), mass=3)
default_planets["Jupiter"] = Planet("Jupiter",image=os.path.join("data","jupiter.png"), mass =14)
default_planets["Saturn"] = Planet("Saturn", image=os.path.join("data","saturn.png"), mass=13)
default_planets["Uranus"] = Planet("Uranus", image=os.path.join("data","uranus.png"), mass=7)
default_planets["Neptun"] = Planet("Neptun", image=os.path.join("data","neptun.png"), mass=6)
default_planets["Pluto"] = Planet("Pluto",  image=os.path.join("data","pluto.png"), mass=1)

print(default_planets.keys())
planet_names = list(default_planets.keys())
allchecks = [True for p in default_planets]
mypics = []
for root, dirs, files in os.walk("."):
    # print(files)
    for f in files:
        if f[-4:] == ".png":
            mypics.append(os.path.join(root, f))
print("meine bilder mit pfad:")
print(mypics)



# ------creating layout inside functions so that it can be used several times inside the main loop
# ------when creating new layouts. it is not allowed to re-use an existing layout without this trick!
def create_cols(checks):
    """checks is a list of Booleans"""
    print("checks:", checks)
    cols = []
    for i, planet in enumerate(default_planets.values()):

        cols.append(  sg.Col(layout=[[sg.Button( planet.name, tooltip=planet.name, image_filename=planet.image, image_subsample=3, border_width=0, button_color=("black" if planet.name == "Sun" else "yellow",None) )],
                                 [sg.Checkbox(text="",default=checks[i], key="c_" + planet.name.lower())]]) )
        print("cols created:", cols)
    return cols

def create_layout(checks=allchecks):
    return [

    [sg.Text('Planeten Sandwich Solar System', size=(30, 1))],
    create_cols(checks),
    [sg.Button("ok"), sg.Cancel()],
    [ sg.Button("übernehmen")],
    [sg.Text('Verwendete Planeten:')],
    [sg.Text("nothing", key="usedPlanets", size=(10,10))],

    ]

layout = create_layout()
location = (100,100)
window = sg.Window('Sandwich1 window', location=location).Layout(layout)


while True:
    event, values = window.read()
    if event in [None, "Cancel"]:
        break

    #print(event, values)
    # if click on planet icon, toggle planet checkbox
    if event in planet_names:
        window["c_"+event.lower()].update(not values["c_"+event.lower()])
    if event == "übernehmen":
        newchecks = []
        for planet in default_planets.values():
            newchecks.append(values["c_"+planet.name.lower()])
        

        #print("checks=", checks)
        layout2 =  create_layout(checks=newchecks) # create a COMPLETE NEW LAYOUT by function, do not re-use the old one by variable
        col_Name = [[sg.Text("Name")]]
        col_mass = [[sg.Text("Mass")]]
        col_a = [[sg.Text("a")]]
        col_e = [[sg.Text("e")]]
        col_i = [[sg.Text("i")]]
        for name in planet_names:
            if values["c_"+name.lower()]:
                col_Name.append([sg.Text(name)])
                col_mass.append([sg.Input(default_planets[name].mass)])
                col_a.append([sg.Input(default_planets[name].a)])
                col_e.append([sg.Input(default_planets[name].e)])
                col_i.append([sg.Input(default_planets[name].i)])


        layout2.append([sg.Col(layout=col_Name), sg.Col(layout=col_mass), sg.Col(layout=col_a), sg.Col(layout=col_e),
                       sg.Col(layout=col_i)])

        print(layout2)
        window1 = sg.Window('Sandwich2 ', location=location).Layout(layout2)
        window.Close()
        window = window1

print("Bye")
