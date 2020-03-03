#!/usr/bin/env python
'''
GUI for creating input-file for Solar-System simulating program (N-body)
'''

import PySimpleGUI as sg
import os
import pickle
import numpy as np
#import random

class Planet():
    ''' Planet of the Solar system ... '''
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
x_elm = {}
for e in elements:
    x_elm[e] = 0.0
form_string = {"a" : "{:13.10f} ",
               "e" : "{:16.14f} ",
               "i" : "{:12.9f} ", # i<100.0 !
               "o" : "{:13.9f} ",
               "O" : "{:14.10f} ",
               "M" : "{:14.10f} ",
               "m" : "{:19.13e}",
              }

# or: elements ="aeioOMm"
default_planets = {}
extra_planets = {}
# for planetname in ["Sun", "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]:
pfad = "data"
default_planets["Sun"]     = Planet("Sun",     image=os.path.join(pfad, "sun.png"),     a=0, m=1.0)
default_planets["Mercury"] = Planet("Mercury", image=os.path.join(pfad, "mercury.png"), a=0.3870984049, e=0.20562759001856, i=7.00541320, o= 29.103337372, O= 48.3386427671, M=300.323037377, m=1.6601367952719E-07)
default_planets["Venus"]   = Planet("Venus",   image=os.path.join(pfad, "venus.png"),   a=0.7233295705, e=0.00679961969640, i=3.39467959, o= 54.717583807, O= 76.6952704868, M=254.371105055, m=2.4478395979668E-06)
default_planets["Earth"]   = Planet("Earth",   image=os.path.join(pfad, "earth.png"),   a=0.9999997512, e=0.01669866878286, i=0.00075327, o=103.94642037,  O=358.8589930163, M=206.899923805, m=3.0404327387108E-06)
default_planets["Mars"]    = Planet("Mars",    image=os.path.join(pfad, "mars.png"),    a=1.5237507286, e=0.09335352423353, i=1.85030907, o=286.4617875,   O= 49.5756757952, M=230.813834555, m=3.2271493621539E-07)
default_planets["Jupiter"] = Planet("Jupiter", image=os.path.join(pfad, "jupiter.png"), a=5.2027870233, e=0.04833790226352, i=1.30463475, o=275.2010177,   O=100.4706642588, M=183.897808735, m=9.5479066214732E-04)
default_planets["Saturn"]  = Planet("Saturn",  image=os.path.join(pfad, "saturn.png"),  a=9.5300498501, e=0.05334351875332, i=2.48644437, o=339.5198854,   O=113.6685162395, M=238.293160282, m=2.8587764436821E-04)
default_planets["Uranus"]  = Planet("Uranus",  image=os.path.join(pfad, "uranus.png"),  a=19.235307728, e=0.04732287311718, i=0.77246832, o= 99.865744927, O= 74.0328700914, M=111.687917146, m=4.3554006968641E-05)
default_planets["Neptune"] = Planet("Neptune", image=os.path.join(pfad, "neptune.png"), a=30.140843059, e=0.00624892789382, i=1.77180286, o=261.73961138,  O=131.755959637 , M=257.158043637, m=5.1775913844879E-05)
default_planets["Pluto"]   = Planet("Pluto",   image=os.path.join(pfad, "pluto.png"),   a=39.3101258977112664, e=0.2549485836749273, i=17.1355669386750655, o=113.7848500826763853, O=110.3143490241281341, M=5.4416930098650553, m=6.553E-09)

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
    for elm in elements:
        try:
            sum *= (float(values["ast_amount_" + elm]) + 1 - ivdelta)
        except:
            #print("values[ast_amount_" + e, "] :", values["ast_amount_" + e] )
            #print("ivdelta:", ivdelta)
            print("error calculating amount " + elm)
            window["ast_total"].update("\u03a3: 5^6 ?") # u03a3 = \N{greek capital letter sigma}
            break
    else:  # schleife lief vollständig durch ohne ein einziges break
        print("recalculating without errors. Result =", sum)
        window["ast_total"].update("\u03a3: {}".format(sum))

def create_cols(checks):
    """checks is a list of Booleans"""
    print("checks:", checks)
    #print("sg.COLOR_SYSTEM_DEFAULT :", sg.COLOR_SYSTEM_DEFAULT)
    #cols = [sg.Col(layout=[[sg.Button("All", tooltip=" select all planets ")],
    #                       [sg.Button("None", tooltip=" unselect all planets ")]])]
    cols = []
    for i, planet in enumerate(default_planets.values()):
        cols.append(sg.Col(layout=[
            [sg.Button("", image_filename = planet.image,
                           image_subsample = 5, border_width = 0,
                           key = "img_" + planet.name,
                           pad = (0,0),
                           #button_color=("black" if planet.name == "Sun" else "yellow", sg.theme_background_color())
                      )],
            [sg.Checkbox(text=planet.name+"  ", default=checks[i],
                         key = "chk_" + planet.name,
                         tooltip = " " + planet.name + " ",
                         pad = (0,0),
                        )]], # end of layout
            element_justification="center", pad=(0,5))) # size & pad in pixels
        #print("cols created:", cols)
    return cols

def create_layout(checks=allchecks, l2 = False): # l2: Layout2 ("Create")
    # zwex Test
    tab1_layout = [[sg.T('This is inside tab 1')]]
    tab2_layout = [[sg.T('This is inside tab 2')],
                   [sg.In(key='in')]]
    return [
        [sg.Text('Solar System N-Body Integrator', size=(30, 1))],
        create_cols(checks),
        [sg.Text("Number of extra planets:"),
         sg.Spin(values=list(range(10)), initial_value=3, key="extra", size=(3,0)),
	     sg.Text(""),
         sg.Checkbox(text="Asteroids", key="asteroids", default=True, tooltip=" Check for including asteroids (have zero mass) "),
         sg.Text("    Time [yrs]:", tooltip=" Total integration time "),
	     sg.InputText("1e7", key="time", size=(8,0)),
         sg.Text("    Delta-t:"),
	     sg.InputText("1e4", key="delta_t", size=(8,0), tooltip=" Timestep for intermediate output "),
         sg.Text("    Precision:"),
         sg.Spin(values=list(range(1,15)),initial_value=-13,key="logeps", size=(3,0)),
         sg.Text("    Integrator:"),
         sg.Combo(values=["Integrator1","Integrator2","Integrator3"], default_value="Integrator2", key="integrator"),
        ],
        [sg.Frame(" Program ",
	         [[sg.Cancel(tooltip=" Quit program ") ]]),
         #sg.VerticalSeparator(),
	     sg.Frame(" Planets ",
	         [[sg.Button("All",                      tooltip=" Select all planets "),
	           sg.Button("None",                     tooltip=" Unselect all planets ") ]]),
         #sg.VerticalSeparator(),
	     sg.Frame(" Constellation ",
	         [[sg.Button("Create", disabled = l2,    tooltip=" Create constellation "),
               sg.Button("Load",                     tooltip=" Load constellation "),
               sg.Button("Save",  disabled = not l2, tooltip=" Save constellation ") ]]),
         #sg.VerticalSeparator(),
	     sg.Frame(" Calculation ",
             [[sg.Button("Write", disabled = not l2, tooltip=" Write input-file for Fortran-program "),
               sg.Button("Run",   disabled = not l2, tooltip=" Run Fortran-program ") ]]),
         ],
        [sg.Text('')], # "Verwendete Planeten:"
        [sg.TabGroup([[sg.Tab('Tab 1', tab1_layout),
                       sg.Tab('Tab 2', tab2_layout)]])],
    ]

def create_layout2():
    newchecks = []
    for planet in default_planets.values():
        newchecks.append(values["chk_" + planet.name])
    # print("checks =", checks)
    # create a COMPLETE NEW LAYOUT by function,
    #   do not re-use the old one by variable
    # ??? list.copy() ???
    layout2 = create_layout(checks=newchecks, l2=True)
    sz = (14,1)
    layout2.append([sg.Text(" Name", background_color="grey", size=(12,1)),
                    sg.Text("", size=(8,1)),
                    sg.Text(" a   [ AU ]",       background_color="grey", size=sz, tooltip=" Semimajor axis "),
                    sg.Text(" e"       ,         background_color="grey", size=sz, tooltip=" Eccentricity "),
                    sg.Text(" i   [ ° ] ",      background_color="grey", size=sz, tooltip=" Inclination "),
                    sg.Text(" \u03c9   [ ° ] ", background_color="grey", size=sz, tooltip=" Argument of periapsis "),
                    sg.Text(" \u03a9   [ ° ] ", background_color="grey", size=sz, tooltip=" Longitude of the ascending node "),
                    sg.Text(" M   [ ° ] ",      background_color="grey", size=sz, tooltip=" Mean anomaly "),
                    sg.Text(" m   [ m_Sol ]",    background_color="grey", size=sz, tooltip=" Mass "),
                    ])
    # \u03c9 = \N{greek small letter omega}
    # \u03a9 = \N{greek capital letter omega}
    # \N{SUBSCRIPT two}
    extra_planets = {}
    for i in range(values["extra"]):
        extra_planets["X"+str(i+1)] = Planet(name="X"+str(i+1))
    for p in list(default_planets.values())+list(extra_planets.values()):
        if p.name[0] == "X" or values["chk_" + p.name]:
            row = []
            # "natural" planet rows get only name as first column,
            # "extra" planet rows get name and a combofield to copy values
            row.append(sg.Text(p.name, size=(12,0)))
            if p.name[0] == "X":
                row.append(sg.Combo(values=[n for n in list(default_planets.keys())+list(extra_planets.keys()) if (n != "Sun" and n!=p.name)],
                             default_value = "Earth",
                             key = p.name + "_copy", size=(6,1),
			     tooltip=" copy from ",
                             enable_events = True))
            else:
                row.append(sg.Text("",size=(8,1)))
            for elm in elements:
                if p.name == "Sun" and elm != "m":
                    # sun only has a field for mass and no other fields
                    row.append(sg.Text("",size=sz))
                else:
                    row.append(sg.Input(p.__dict__[elm], size=(14, 1),
                                       key = "val_" + elm + "_" + p.name))  # val=value
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

def create_range(elm):
    return np.arange(float(values["ast_min_"+elm]),
                     float(values["ast_max_"+elm])
                    +float(values["ast_step_"+elm]),
                     float(values["ast_step_"+elm]))

layout = create_layout()
loc = (10, 30)
window = sg.Window('N-Body Lie (1)', location=loc).Layout(layout)

ivdelta = 0 # Intervals, not Values for asteroids

while True:
    event, values = window.read()
    if event in [None, "Cancel"]:
        break
    if event == "All":  # check all planets checkboxes
        for p in default_planets.keys():
            window["chk_"+p].update(True)
    if event == "None": # uncheck all planets checkboxes
        for p in default_planets.keys():
            window["chk_"+p].update(False)
    if "img_" in event: # in list(default_planets.keys()): # if click on planet icon, toggle planet checkbox
        new_key = event.replace("img","chk")
        window[new_key].update(not values[new_key])
    if event == "Create":
        win_tmp = sg.Window("Please wait ...",
                            [[sg.T("... until constellation is created!")]]).finalize()
        window.Close()
        layout2 = create_layout2()
        #print(layout2)
        window = sg.Window('N-Body Lie Integrator', location=loc).Layout(layout2).finalize()
        # finalize(), damit recalcen kann
        recalc_total() # damit schon anfangs Zahl existiert
        # Problem: dict values ist noch nicht befüllt!
        win_tmp.close()
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
            if "chk_" in k or k == "asteroids" or k == "extra":
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
    if event == "Write": # WRITE input-file for Fortran-program
        print("Button 'Write' pressed")
        #filename = sg.PopupGetFile("Choose File Name for SAVE-ing")
        filewrite = sg.PopupGetFile("Choose File Name for WRITE-ing")
        with open (filewrite, "w") as f:
            f.write("{:0g} {:0g}\n".format(float(values["time"]),float(values["delta_t"])))
            f.write(" 0        /INI [0=EL,1=HEL,2=BAR] *** TO DO ***\n")
            f.write(" 12       /N [Anzahl der Lie-Terme] *** TO DO ***\n")
            f.write("{:2g} {:2g}     /N_masse,N_masselos\n".format(
                    len(allchecks), int(values["extra"])))
            f.write("{:3g}       /logeps\n".format(float(format(values["logeps"]))))
            f.write("1D-11     /SWMINI = StepWidthMINImum *** TO DO ***\n")
            f.write("0d0  0    /swsum(t0[tage]), nstep *** TO DO ***\n")
            f.write(values["integrator"] + "\n\n")
            for p in list(default_planets.values()) + list(extra_planets.values()):
                if not values["chk_" + p.name] and p.name[0] != "X":
                    continue # planet not check-selected and not an extra planet
                for elm in elements:
                    print("p.name = '" + p.name + "'")
                    print("elm    = '" + elm    + "'")
                    if p.name == "Sun" and elm != "m":
                        # sun has only mass field/value
                        f.write("0.0          ")
                    else:
                        f.write(form_string[elm].format(float(values["val_" + elm + "_" + p.name] + " ")))
                f.write("\n") # newline after each planet
            f.write("\n")  # newline after all planets
            #dbg = False
            for x_elm["a"] in create_range("a"):
                #print("xa :", xa)
                for x_elm["e"] in create_range("e"):
                    #print("  xe :", xe)
                    for x_elm["i"] in create_range("i"):
                        #print("    xi :", xi)
                        for x_elm["o"] in create_range("o"):
                            #print("      xo :", xo)
                            for x_elm["O"] in create_range("O"):
                                #print("        xO :", xO)
                                for x_elm["M"] in create_range("M"):
                                    #print("          xM :", xM)
                                    for elm in elements:
                                        f.write(form_string[elm].format(x_elm[elm]))
                                    f.write("0.0\n") # mass of asteroid
                                #</for xM>
                            # </for xO>
                        # </for xo>
                    # </for xi>
                # </for xe>
            # </for xa>
            f.write("# a_[AU]        eccentricity      inclinat.     omega         Omega          mean_anom.   mass_[sun]\n")
        #</with open>
        continue
    if event == "Run":   # RUN Fortran-program
        print("Button 'Run' pressed")
        continue
    if "_copy" in event: # COPY values from "regular" planet to X-planet
        sourceplanet = values[event] # zB Jupiter
        targetrow = event[:2] # zB x2
        for elm in elements:
            if sourceplanet[0] == "X":
                window["val_" + elm + "_" + targetrow].update(values["val_"+elm+"_"+sourceplanet])
            else:
                 window["val_"+elm+"_"+targetrow].update(default_planets[sourceplanet].__dict__[elm])
    #---- asteroiden - klumpert ------
    if event == "iv_i":
        if ivdelta == 0: # nothing to do
            continue # while-loop
        ivdelta = 0
        # recalc: subtract 1 from asteroids-amounts
        for elm in elements:
            window["ast_amount_" + elm].update(float(values["ast_amount_" + elm]) -1 )
        print("iv_i geklickt")
    elif event == "iv_v":
        if ivdelta == 1: # nothing to do
            continue # while-loop
        ivdelta = 1
        # recalc: add 1 to asteroids-amounts
        for elm in elements:
            window["ast_amount_" + elm].update(float(values["ast_amount_" + elm]) +1 )
        print("iv_v geklickt")
    if "ast_" in event:
        print("Asteroiden-Zeux, event:", event)
        elm = event[-1]
        what = event[4:7] # Buchstaben 4, 5 und 6; 7 ist nicht mehr dabei!
        if what == "ste":
            what = "step"
        elif what == "amo":
            what = "amount"
        if "_calc_" in event:
            #ivdelta = values["iv_v"] # 1 wenn angeklickt, sonst 0
            print("ivdelta:", ivdelta)
            try:
                a_min = float(values["ast_min_"+elm])
            except:
                sg.Popup("Error",custom_text="Min-Value is not a float!",no_titlebar=True)
                continue # while True, window.read(
            try:
                a_max = float(values["ast_max_"+elm])
            except:
                sg.Popup("Error",custom_text="Max-Value is not a float!",no_titlebar=True)
                continue  # while True, window.read(
            try:
                a_stp = float(values["ast_step_"+elm])
            except:
                sg.Popup("Error",custom_text="Step-Value is not a float!",no_titlebar=True)
                continue  # while True, window.read(
            try:
                a_amo = float(values["ast_amount_"+elm])
            except:
                sg.Popup("Error", custom_text="Amount-Value is not an integer!", no_titlebar=True)
                continue  # while True, window.read(
            if int(a_amo) == a_amo:
                  a_amo = int(a_amo)
            else:
                sg.Popup("Error",custom_text="Amount-Value is not an integer!",no_titlebar=True)
                continue  # while True, window.read(

            if what == "min":
                try:
                    result = a_max - (a_amo-ivdelta) * a_stp
                except:
                    result = "Error!"
            elif what == "max":
                if a_stp == 0 or a_amo == 0:
                    result = a_min
                    sg.Popup("ToDo: Amount = 1 setzen!")
                else:
                    try:
                        result = (a_amo-ivdelta) * a_stp + a_min
                    except:
                        result = "Error!"
            elif what == "step":
                if a_min == a_max or (a_amo-ivdelta) == 0:
                    result = 0
                    sg.Popup("ToDo: Amount = 1 oder max=min setzen!")
                else:
                    try:
                        result = ( a_max - a_min ) / (a_amo-ivdelta)
                    except:
                        result = "Error!"
            elif what == "amount":
                if a_min == a_max or a_stp == 0:
                    result = 1 + ivdelta
                    sg.Popup("ToDo: Step = 0 oder max=min setzen!")
                else:
                    try:
                        result = float( ( a_max - a_min ) / a_stp + ivdelta )
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
