#!/usr/bin/env python
'''
GUI for creating parameter-file for Solar-System simulating program
'''

import PySimpleGUI as sg
import os
import pickle
#import random


class Planet():
    ''' Planet for the Solar system ... '''

    def __init__(self, name, symbol="Symbol", image=None, a=1, e=0, i=0, o=0, O=0, M=0, m=1):
        self.name = name
        self.symbol = symbol
        self.image = image
        self.a = a # semi major axis
        self.e = e # eccentricity
        self.i = i # inclination
        self.o = o # omega
        self.O = O # Omega
        self.M = M # mean anomaly
        self.m = m # mass

    def __repr__(self):
        return self.name

elements = ["a", "e", "i", "o", "O", "M", "m"] # orbital elements names # __dict__ ?
# or: elements ="aeioOMm"
default_planets = {}
# for planetname in ["Sun", "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]:
pfad = "data"
default_planets["Sun"]     = Planet("Sun",     image=os.path.join(pfad, "sun.png"),     m=1500.0, a=0)
default_planets["Mercury"] = Planet("Mercury", image=os.path.join(pfad, "mercury.png"), m=2.1,  a=0.4)
default_planets["Venus"]   = Planet("Venus",   image=os.path.join(pfad, "venus.png"),   m=3.2,  a=0.7)
default_planets["Earth"]   = Planet("Earth",   image=os.path.join(pfad, "earth.png"),   m=4.3,  a=1)
default_planets["Mars"]    = Planet("Mars",    image=os.path.join(pfad, "mars.png"),    m=3.4,  a=1.6)
default_planets["Jupiter"] = Planet("Jupiter", image=os.path.join(pfad, "jupiter.png"), m=14.5, a=5.2)
default_planets["Saturn"]  = Planet("Saturn",  image=os.path.join(pfad, "saturn.png"),  m=13.6, a=10)
default_planets["Uranus"]  = Planet("Uranus",  image=os.path.join(pfad, "uranus.png"),  m=7.7,  a=20)
default_planets["Neptune"] = Planet("Neptune", image=os.path.join(pfad, "neptune.png"), m=6.8,  a=30)
default_planets["Pluto"]   = Planet("Pluto",   image=os.path.join(pfad, "pluto.png"),   m=1.1,  a=40)

print("default_planets.keys() :",
       default_planets.keys())
allchecks = [False for p in default_planets]
allchecks[0] = True
allchecks[1] = True
mypics = []
for root, dirs, files in os.walk("."):
    # print(files)
    for f in files:
        if f[-4:] == ".png":
            mypics.append(os.path.join(root, f))
print("mypics :",
       mypics)

# --- creating layout inside functions so that it can be used several times
#     inside the main loop when creating new layouts. it is not allowed to
#     re-use an existing layout without this trick!

def recalc_total():
    """ calculates total number of asteroids """
    sum = 1
    for e in elements:
        try:
            sum *= (float(values["ast_amount_" + e]) + 1 - ivdelta)
        except:
            #print("values[ast_amount_" + e, "] :", values["ast_amount_" + e] )
            #print("ivdelta:", ivdelta)
            print("error calculating amount " + e)
            window["ast_total"].update("\u03a3: 5^6 ?")
            break
    else:  # schleife lief vollständig durch ohne ein einziges break
        print("recalculating without errors. Result =", sum)
        window["ast_total"].update("\u03a3: {}".format(sum))

def create_cols(checks):
    """checks is a list of Booleans"""
    print("checks:", checks)
    cols = [sg.Col(layout=[[sg.Button("all", tooltip=" select all planets ")],
                           [sg.Button("none", tooltip=" unselect all planets ")],
                          ])
           ]
    for i, planet in enumerate(default_planets.values()):
        cols.append(sg.Col(layout=[[sg.Button(planet.name, tooltip=planet.name, image_filename=planet.image,
                                              image_subsample=5, border_width=0,
                                              button_color=("black" if planet.name == "Sun" else "yellow", None))],
                                   [sg.Checkbox(text="", default=checks[i], key="c_" + planet.name.lower())]]))
        #print("cols created:", cols)
    return cols

def create_layout(checks=allchecks, l2 = False): # l2: Layout2 ("übernehmen")
    return [
        [sg.Text('Planeten Sandwich Solar System', size=(30, 1))],
        create_cols(checks),
        [sg.Text("Anzahl Extra Planeten:"),
         sg.Spin(values=list(range(10)),initial_value=3,key="extra", size=(3,0)) ,
         sg.Checkbox(text="Asteroiden",key="asteroids",default=True),
         sg.Text("    Time [yrs]:"), sg.InputText("1e7", key="time", size=(8,0)),
         sg.Text("    Delta-t:"), sg.InputText("1e4", key="delta_t", size=(8,0)),
         sg.Text("    Precission:"),
         sg.Spin(values=list(range(1,15)),initial_value=11,key="precission", size=(3,0)),
         sg.Text("    Integrator:"),
         sg.Combo(values=["Integrator1","Integrator2","Integrator3"], default_value="Integrator2", key="integrator"),
        ],
        [sg.Button("übernehmen", disabled = l2), sg.Cancel(), sg.Button("Load"),
         sg.Button("Save",disabled = not l2) ],
        [sg.Text('Verwendete Planeten:')],
            ]
        ##sg.Input(key="extra")
        # sg.OK() : Kurzform von sg.Button("ok")

def create_layout2():
    newchecks = []
    for planet in default_planets.values():
        newchecks.append(values["c_" + planet.name.lower()])
    # print("checks =", checks)
    # create a COMPLETE NEW LAYOUT by function,
    #   do not re-use the old one by variable
    # ??? list.copy() ???
    layout2 = create_layout(checks=newchecks, l2=True)
    layout2.append([sg.Text("Name", size=(12,1)),
                    sg.Text("", size=(8,1)),
                    sg.Text("a   [AU]", size=(14,1), tooltip=" semi major axis "),
                    sg.Text("e"       , size=(14,1), tooltip=" eccentricity "),
                    sg.Text("i   [°] ", size=(14,1), tooltip=" inclination "),
                    sg.Text("o   [°] ", size=(14,1), tooltip=" omega "),
                    sg.Text("O   [°] ", size=(14,1), tooltip=" Omega "),
                    sg.Text("M   [°] ", size=(14,1), tooltip=" mean anomaly "),
                    sg.Text("m   [kg | m_Sol]", size=(14, 1), tooltip=" mass "),
                    ])
    extra_planets = {}
    for i in range(values["extra"]):
        extra_planets["X"+str(i+1)] = Planet(name="X"+str(i+1))
    for p in list(default_planets.values())+list(extra_planets.values()):
        if p.name[0] == "X" or values["c_" + p.name.lower()]:
            row = []
            # "natural" planet rows get only name as first column,
            # "extra" planet rows get name and a combofield to copy values
            row.append(sg.Text(p.name, size=(12,0)))
            if p.name[0] == "X":
                row.append(sg.Combo(values=[n for n in list(default_planets.keys())+list(extra_planets.keys()) if (n != "Sun" and n!=p.name)],
                             default_value = "Earth",
                             key = p.name + "_copy", size=(6,1),
                             enable_events = True))
            else:
                row.append(sg.Text("",size=(8,1)))
            for nr, elm in enumerate(elements):
                if p.name == "Sun" and elm != "m":
                    # sun only has a field for mass and no other fields
                    row.append(sg.Text("",size=(14,1)))
                else:
                    row.append(sg.Input(p.__dict__[elm], size=(14, 1),
                                       key="val_"+elm+"_" + p.name.lower()))  # val=value
            #col_o.append([sg.Input(p.o, size=(15, 1),
            #                       key="val_o_" + p.name)])
            layout2.append(row)
    #### asteroiden ------
    if values["asteroids"]:
        #------- astro min
        row = [sg.Text("Asteroiden minimum:", size=(22,0))]
        for elm in elements:
            #row.append(sg.InputText(default_text="0", key="ast_min_"+elm, size=(15,0)))
            row.append(sg.Col(pad=(0,0),
                          layout=[[sg.InputText(
                              default_text="0",
                              key="ast_min_" + elm,
                              size=(8,0), pad=(0,0),
                              enable_events=True),
                              sg.Button("*", key="ast_min_calc_" + elm, pad=(0,0))]]))
        layout2.append(row)
        #--- asteroids max
        row = [sg.Text("Asteroiden maximum:", size=(22,0))]
        for elm in elements:
            #row.append(sg.InputText(default_text="0", key="ast_max_" + elm, size=(15, 0)))
            row.append(sg.Col(pad=(0,0),
                          layout=[[sg.InputText(
                              default_text="10",
                              key="ast_max_" + elm,
                              size=(8,0), pad=(0,0),
                              enable_events=True),
                              sg.Button("*", key="ast_max_calc_" + elm, pad=(0,0))]]))
        layout2.append(row)
        #--- asteroids stepsize
        row = [sg.Text("Asteroiden stepsize:", size=(22,0))]
        for elm in elements:
            row.append(sg.Col(pad=(0,0),
                              layout=[[sg.InputText(
                                    default_text="2",
                                    key="ast_step_"+elm,
                                    size=(8,0),pad=(0,0),
                                    enable_events=True),
                                    sg.Button("*",key="ast_step_calc_"+elm,pad=(0,0))]]))
        layout2.append(row)
        #--- asteroids amount
        row = [sg.Text("Ast. amount:", size=(11, 0)),
               sg.Radio("I",tooltip=" Intervals ",group_id="iv",key="iv_i",enable_events=True,default=True,pad=(0,0)),
               sg.Radio("V",tooltip=" Values ",   group_id="iv",key="iv_v",enable_events=True,default=False,pad=(0,0)),
               ]
        for elm in elements:
            row.append(sg.Col(pad=(0,0),
                              layout=[[sg.InputText(
                                    default_text="5",
                                    key="ast_amount_"+elm,
                                    size=(8,0),pad=(0,0),
                                    enable_events=True),
                                    sg.Button("*",key="ast_amount_calc_"+elm,pad=(0,0))]]))
        row.append(sg.Text(" ? ",key="ast_total",size=(5,0)))
        layout2.append(row)
        #row.append(sg.Column(layout=[[
        #    sg.Radio(text="stepsize", group_id="radio_"+elm, default=False, key ="radio_"+elm+"_steps" )],
        #    [sg.Radio(text="quantity", group_id="radio_"+elm, default=True,  key ="radio_"+elm+"_quantity")],
        #    [sg.Radio(text="random",   group_id="radio_"+elm, default=False, key ="radio_"+elm+"_random")]
        #    ]))
        #layout2.append(row)
        #--- asteroids amount ------
        # ------ random ----
    # end for
    return layout2

layout = create_layout()
loc = (10, 30)
window = sg.Window('Sandwich1 window', location=loc).Layout(layout)

ivdelta = 0 # Intervals, not Values for asteroids

while True:
    event, values = window.read()
    if event in [None, "Cancel"]:
        break
    if event == "all":  # check all planets checkboxes
        for p in default_planets.keys():
            window["c_"+p.lower()].update(True)
    if event == "none": # uncheck all planets checkboxes
        for p in default_planets.keys():
            window["c_"+p.lower()].update(False)
    if event in list(default_planets.keys()): # if click on planet icon, toggle planet checkbox
        window["c_" + event.lower()].update(not values["c_" + event.lower()])
    if event == "übernehmen":
        layout2 = create_layout2()
        #print(layout2)
        window1 = sg.Window('Sandwich2 ', location=loc).Layout(layout2)
        window.Close()
        window = window1
        window.finalize()
        recalc_total() # damit schon anfangs Zahl existiert
        # Problem: dict values ist noch nicht befüllt!
    if event == "Save": # SAVE all parameters
        print(values)
        filename = sg.PopupGetFile("Choose File Name for SAVE-ing")
        print(filename)
        with open(filename, 'wb') as handle: # wb: Write Binary
            pickle.dump(values, handle, protocol=0) # pickle.HIGHEST_PROTOCOL)
    if event == "Load": # LOAD saved parameters
        # zuerst checks, extra(planeten) und asteroids auslesen aus pickle
	#   und formular neu bauen
        filename = sg.PopupGetFile("Choose File Name for LOAD-ing")
        with open(filename, 'rb') as handle: # rb: Read Binary
            pickle_values = pickle.load(handle)
        print("file loaded")
        #--------
        for k in pickle_values: # k = key
            if "c_" in k or k == "asteroids" or k == "extra":
                window[k].update(pickle_values[k])
                values[k] = pickle_values[k]
                print("updating from pickle...", k)

        layout2 = create_layout2()
        #print(layout2)
        window1 = sg.Window('Sandwich2 ', location=loc).Layout(layout2)
        window.Close()
        window = window1
        window.finalize()
        print("formular ready for loading values from pickle...")
        for k in pickle_values:
            window[k].update(pickle_values[k])
            values[k] = pickle_values[k]
            print("second time updating from pickle...", k)
        recalc_total()
    if "_copy" in event: # copy values from "regular" planet to X-planet
        sourceplanet = values[event] # zB Jupiter
        targetrow = event[:2].lower() # zB x2
        for elm in elements:
            if sourceplanet[0] == "X":
                window["val_" + elm + "_" + targetrow].update(values["val_"+elm+"_"+sourceplanet.lower()])
            else:
                 window["val_"+elm+"_"+targetrow].update(default_planets[sourceplanet].__dict__[elm])
    #---- asteroiden - klumpert ------
    if event == "iv_i":
        if ivdelta == 0:
            continue # while-loop
        ivdelta = 0
        # recalc: subtract 1 from asteroids-amounts
        for elm in elements:
            window["ast_amount_" + elm].update(float(values["ast_amount_" + elm]) -1 )
        print("iv_i geklickt")
    elif event == "iv_v":
        if ivdelta == 1:
            continue # while-loop
        ivdelta = 1
        # recalc: add 1 to asteroids-amounts
        for elm in elements:
            window["ast_amount_" + elm].update(float(values["ast_amount_" + elm]) +1 )
        print("iv_v geklickt")
    if "ast_" in event:
        print("Asteroiden-Zeux, event:", event)
        elm = event[-1]
        what = event[4:7] # Buchstaben 4, 5, 6; 7 ist nicht mehr dabei!
        if what == "ste":
            what = "step"
        elif what == "amo":
            what = "amount"
        if "_calc_" in event:
            #ivdelta = values["iv_v"] # 1 wenn angeklickt, sonst 0
            print("ivdelta:", ivdelta)
            if what == "min":
                try:
                    result = ( float(values["ast_max_"+elm])
                             - (float(values["ast_amount_"+elm])-ivdelta)
                               * float(values["ast_step_"+elm])
                             )
                except:
                    result = "Error!"
            elif what == "max":
                try:
                    result = ( (float(values["ast_amount_"+elm])-ivdelta)
                             * float(values["ast_step_"+elm])
                             + float(values["ast_min_"+elm])
                             )
                except:
                    result = "Error!"
            elif what == "step":
                try:
                    result = ( ( float(values["ast_max_"+elm])
                             - float(values["ast_min_"+elm]) )
                             / (float(values["ast_amount_"+elm])-ivdelta)
                             )
                except:
                    result = "Error!"
            elif what == "amount":
                try:
                    result = float( ( float(values["ast_max_"+elm])
                               - float(values["ast_min_"+elm]) )
                               / float(values["ast_step_"+elm])
                               + ivdelta
                             )
                except:
                    result = "Error!"
            #<what == ...>
            window["ast_"+what+"_"+elm].update(result)
            values["ast_"+what+"_"+elm] = result
            #--- disable calc buttons until new manual change
            for w in ("min", "max", "step", "amount"):
                k = "ast_" + w + "_calc_" + elm # key
                window[k].update(disabled=True)

            #------- calculating total count of asteroids
            if what == "amount" and result != "Error!":
                recalc_total()
                if result != int(result):
                    window["ast_" + what + "_" + elm].update(background_color="red")
                else:
                    window["ast_" + what + "_" + elm].update(background_color="white")

        else: # <if "_calc_" in event:>
            '''händische Änderung eines asteroiden-inputfeldes, 
            jetzt kontrollieren ob spalte erlaubte Werte liefert'''

            #--- enable calc buttons because of new manual change
            for w in ("min", "max", "step", "amount"):
                k = "ast_" + w + "_calc_" + elm # key
                window[k].update(disabled=False)

            ### elm = event[-1]
            if "_amount_" in event: # and "_calc_" not in event:
                """ausführen nur bei händischer wertänderung"""
                print("recalculating....(because manual change event)")
                # farb-check. int("1.0") ergibt error, float("1.0") ist erlaubt
                print("farb check mit ", values[event])
                try:
                    red = float(values[event]) != int(float(values[event]))
                except:
                    red = True
                print(red)
                if red:
                    window[event].update(background_color="red")
                else:
                    window[event].update(background_color="white")
                #  total amount of asteroids ausrechnen
                recalc_total()
                #result = 1
                #for elm in elements:
                #    try:
                #        result *= float(values["ast_amount_" + elm])
                #    except:
                #        print("error calculating amount "+elm)
                #        break
                #
                #else:  # schleife lief durch ohne ein einziges break vollständig
                #    print("recalculating without errors. Result=", result)
                #    window["ast_total"].update("Total: {}".format(result))
            #<if "_amount_" in event: # and "_calc_" not in event:>
        # <if "_calc_" in event:>
print("Bye")
