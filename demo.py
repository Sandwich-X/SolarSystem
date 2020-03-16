#!/usr/bin/env python
'''
GUI for creating input-file for Solar-System simulating program (N-body)

??? TO DO :
roter Hintergrund bei Count nur wenn float, nicht bei Error oder sonst;
oder bei allen rot, wenn nicht san_...
'''

import PySimpleGUI as sg
import os
import pickle
import numpy as np
#import random

CALC_ERR_MSG = "Error !\a" # CALCulation ERRor MeSsaGe

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
#end class Planet()

elements = ["a", "e", "i", "o", "O", "M", "m"] # orbital elements names # __dict__ ?
#elements = "aeioOMm"
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
            sum *= (float(values["ast_cnt_" + elm]) + 1 - delta_iv)
        except:
            #print("values[ast_cnt_" + e, "] :", values["ast_cnt_" + e] )
            #print("delta_iv:", delta_iv)
            #window["status"].update ... ??? überschreibt vorherige Status-Meldung
            print("error calculating count " + elm)
            window["ast_total"].update("?")
            break
    else:  # schleife lief vollständig durch ohne ein einziges break
        print("recalculating without errors. Result =", sum)
        window["ast_total"].update(sum)
#end def recalc_total()

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
#end def create_cols(checks)

def create_layout(checks=allchecks, l2 = False): # l2: Layout2 ("Create")
    # zwex Test
    #tab1_layout = [[sg.T('This is inside tab 1')]]
    #tab2_layout = [[sg.T('This is inside tab 2')],
    #               [sg.In(key='in')]]
    return [
        [sg.Text('Solar System N-Body Integrator', size=(30, 1))],
        create_cols(checks),
        [sg.Text("Number of eXtra planets:"),
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
        #[sg.Text('')], # "Verwendete Planeten:"
        #[sg.TabGroup([[sg.Tab('Tab 1', tab1_layout),
        #               sg.Tab('Tab 2', tab2_layout)]])],
    ]
#end def create_layout(checks=allchecks, l2 = False)

def create_layout2():
    newchecks = []
    for planet in default_planets.values():
        newchecks.append(values["chk_" + planet.name])
    # print("checks =", checks)
    # create a COMPLETE NEW LAYOUT by function,
    #   do not re-use the old one by variable
    # ??? list.copy() ??? deepcopy !!!
    layout2 = create_layout(checks=newchecks, l2=True)
    sz = (14,1)
    row = [sg.Text(" Name", background_color="grey", size=(10,1)),
           #sg.Text("", size=(8,1)),
           sg.Combo(values=["0: ELE ", "1: HEL ", "2: BAR "],
                    default_value="0: ELE ",
                    key="coord_type",
                    tooltip=" Type of coordinates: " \
                        + "\n   0: ELEments (orbital) " \
                        + "\n   1: HELiocentric " \
                        + "\n   2: BARycentric ",
                    size=(6,1), enable_events=True)]
    for i in range(1,7): # 1, ..., 6
        row.append(sg.Text(key="coord_"+str(i), background_color="grey", size=sz))
    row.append(sg.Text(" m   [ m_Sol ]"  , tooltip=" Mass   [Solar Mass]", background_color="grey", size=sz))
    layout2.append(row)
    extra_planets = {}
    for i in range(values["extra"]):
        extra_planets["X"+str(i+1)] = Planet(name="X"+str(i+1))
    for p in list(default_planets.values())+list(extra_planets.values()):
        if p.name[0] == "X" or values["chk_" + p.name]:
            row = []
            # "natural" planet rows get only name as first column,
            # "extra" planet rows get name and a combofield to copy values
            row.append(sg.Text(p.name, size=(10,0)))
            if p.name[0] == "X": # first letter of planet name = "X"?
                row.append(sg.Combo(values=[n for n in list(default_planets.keys())+list(extra_planets.keys()) if (n != "Sun" and n != p.name)],
                             #default_value = "Earth",
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
    #--- asteroids
    if values["asteroids"]:
        #--- asteroids min
        row = [sg.Text("Asteroids minimum:", size=(20,0))]
        for elm in elements:
            row.append(sg.InputText(default_text="0", key="ast_min_" + elm,
                                    size=(9,0),pad=((4,0),0)))
            row.append(sg.Button("*", key="ast_min_calc_" + elm,
                                 tooltip=" Calculate ",
                                 size=(0,0), pad=((4,6),0) ) )
        layout2.append(row)
        #--- asteroids include min max
        row = [sg.Text("Ast. include min,max:", size=(20,0))]
        for i in range(1,7):
            row.append(sg.Checkbox("min",key="ast_min_incl_"+str(i),tooltip=" include Min "+str(i),default=True,pad=(0,0)))
            row.append(sg.Checkbox("max",key="ast_max_incl_"+str(i),tooltip=" include Max "+str(i),default=True,pad=((0,12),0)))
        layout2.append(row)
        #--- asteroids max
        row = [sg.Text("Asteroids maximum:", size=(20,0))]
        for elm in elements:
            row.append(sg.InputText(default_text="10", key="ast_max_" + elm,
                                    size=(9,0), pad=((4,0),0)) )
            row.append(sg.Button("*", key="ast_max_calc_" + elm,
                                 tooltip=" Calculate ",
                                 size=(0,0), pad=((4,6),0) ) )
        layout2.append(row)
        #--- asteroids stepsize
        row = [sg.Text("Asteroids stepsize:", size=(20,0))]
        for elm in elements:
            row.append(sg.InputText(default_text="2", key="ast_stp_"+elm,
                                    size=(9,0), pad=((4,0),0),
                                    enable_events=True) )
            row.append(sg.Button("*", key="ast_stp_calc_" + elm,
                                 tooltip=" Calculate ",
                                 size=(0,0), pad=((4,6),0) ) )
        layout2.append(row)
        #--- asteroids count
        row = [sg.Text("Ast. count:", size=(9,0)),
               sg.Radio("I", tooltip=" Intervals (not Values)", default=True,
                        group_id="iv", key="iv_i", pad=(0,0),
                        enable_events=True),
               sg.Radio("V", tooltip=" Values (not Intervals)", default=False,
                        group_id="iv", key="iv_v", pad=((0,2),0),
                        enable_events=True),
               ]
        for elm in elements:
            row.append(sg.InputText(default_text="5", key="ast_cnt_"+elm,
                                    size=(9,0), pad=((4,0),0),
                                    enable_events=True) )
            row.append(sg.Button("*", key="ast_cnt_calc_" + elm,
                                 tooltip=" Calculate ",
                                 size=(0,0), pad=((4,6),0) ) )
        layout2.append(row)
        #row.append(sg.Column(layout=[[
        #    sg.Radio(text="stepsize", group_id="radio_"+elm, default=False, key ="radio_"+elm+"_steps" )],
        #    [sg.Radio(text="quantity", group_id="radio_"+elm, default=True,  key ="radio_"+elm+"_quantity")],
        #    [sg.Radio(text="random",   group_id="radio_"+elm, default=False, key ="radio_"+elm+"_random")]
        #    ]))
        #layout2.append(row)
        #--- asteroids count ------
        # ------ random ----
    # end for elm
    layout2.append(
        [sg.StatusBar("", (115,0), key="status", tooltip=" StatusBar ",
                      background_color="grey"), # doppelt!!!
         # (101,0) + ((125,0),0) statt (117,0) + ((12,0),0) ist auch eine fkt. Version
         # d.h. 16 Buchstaben mehr und 113 Pixel weniger: 1 Buchstabe = 7 Pixel
         sg.Text(" \u03a3: ", tooltip=" Total count of asteroids ",
                 pad=((12,0),0), background_color="grey"),
                 # u03a3 = \N{greek capital letter sigma}
         sg.Text(" ? ", key="ast_total", tooltip=" Total count of asteroids ",
                 size=(10, 0), pad=(0, 0), background_color="grey")])
    return layout2
#end def create_layout2()

def set_cnt_zero():
    a_cnt = delta_iv  # 0 (or 1)
    window["ast_cnt_"+elm].update(a_cnt,
                                  background_color="white") # in case color was red
    values["ast_cnt_"+elm] = a_cnt  # for total_count
    window["status"].update(" Set 'Count' to " + str(a_cnt),
                            background_color="grey")
# end def set_cnt_zero()

def try_2_int(x): # TRY to 'convert' x (usually Asteroid_CouNT) to INTeger
    try:
        f = float(x) # float because int("1.0") does not work,
    except:          #     but int(float("1.0")) does
        return x
    i = int(f)
    if i == f:
        return i
    else:
        return f
#end def try_2_int()

def san_check_and_calc(iv_delta):
    #sanity_check:
    try:
        a_min = float(values["ast_min_" + elm])
        san_min = True
    except:
        san_min = False
    print("san_min:", san_min)
    try:
        a_max = float(values["ast_max_" + elm])
        san_max = True
    except:
        san_max = False
    print("san_max:", san_max)
    try:
        a_stp = float(values["ast_stp_" + elm])
        san_stp = True
    except:
        san_stp = False
    print("san_stp:", san_stp)
    print('values["ast_cnt_' + elm + '"] :',
          values["ast_cnt_" + elm])
    try: # 1st try float
        a_cnt = float(values["ast_cnt_" + elm])
        san_cnt = True
    except:
        san_cnt = False
    print("san_cnt:", san_cnt, " (float)")
    try: # then finally int
        a_cnt = int(a_cnt)
        san_cnt = True
    except:
        san_cnt = False
    print("san_cnt:", san_cnt, " (int)")
    #end sanity check
    #--- start calculation:
    # basic equation: max - min = step * count
    if to_calc == "min":  # min = max - step * count
        if not san_max:
            return (CALC_ERR_MSG,
                    "Need value for 'Max' to calculate 'Min'!")
        else:
            if not san_stp:
                if not san_cnt:
                    return (CALC_ERR_MSG,
                            "Need either one zero value in 'Step' or 'Count', or a float in 'Step' and an int in 'Count' to calculate 'Min'!")
                elif a_cnt == 0:
                    return (a_max,)
                else:
                    return (CALC_ERR_MSG,
                            "Need also a value in 'Step' to calculate 'Min'!")
                # end if not san_cnt
            else:  # san_stp = True
                if a_stp == 0.0:
                    set_cnt_zero()
                    return (a_max,)
                else:
                    if not san_cnt:
                        return (CALC_ERR_MSG,
                                "Need also a int value in 'Count' to calculate 'Min'!")
                    else:
                        return (a_max - a_stp * a_cnt,)
                                #"Successfully calculated 'Min'.")
                    # end if not san_cnt
                # end if a_stp == 0.0
            # end if not san_stp
        # end if not san_max
    elif to_calc == "max":  # max = min + step * count # similar to before but min <-> max
        if not san_min:
            return (CALC_ERR_MSG,
                    "Need value for 'Min' to calculate 'Max'!")
        else:
            if not san_stp:
                if not san_cnt:
                    return (CALC_ERR_MSG,
                            "Need either one zero value in 'Step' or 'Count', or a float in 'Step' and an int in 'Count' to calculate 'Max'!")
                elif a_cnt == 0:
                    return (a_min,)
                else:
                    return (CALC_ERR_MSG,
                            "Need also a value in 'Step' to calculate 'Max'!")
                # end if not san_cnt
            else:  # san_stp = True
                if a_stp == 0.0:
                    set_cnt_zero()
                    return (a_min,)
                else:
                    if not san_cnt:
                        return (CALC_ERR_MSG,
                                "Need also a int value in 'Count' to calculate 'Max'!")
                    else:
                        return (a_min + a_stp * a_cnt,)
                                #"Successfully calculated 'Max'.")
                    # end if not san_cnt
                # end if a_stp == 0.0
            # end if not san_stp
        # end if not san_min
    elif to_calc == "stp":  # step = ( max - min ) / count
        if not san_cnt:
            if san_min and san_max:
                if a_min == a_max:
                    set_cnt_zero()
                    return (0.0,)
                else:
                    return (CALC_ERR_MSG,
                            "Need an (int) value for 'Count' or 'Min'='Max' to calculate 'Step'!")
                # end if a_min == a_max
            else:
                return (CALC_ERR_MSG,
                        "Too less (meaningfull) values given for calculating 'Step'!")
            # end if san_min and san_max
        else:  # san_cnt=True
            if a_cnt == 0:
                if san_min:
                    a_max = a_min
                    window["ast_max_"+elm].update(a_max)
                    msg = f"Set 'Max' to {a_max} (= 'Min')" # MeSsaGe
                    #msg = "Set 'Max' to %s (= 'Min')" % str(a_max)
                    #msg = "Set 'Max' to " + str(a_max) + "( = 'Min')")
                elif san_max:
                    a_min = a_max
                    window["ast_min_"+elm].update(a_min)
                    msg = f"Set 'Min' to {a_max} (= 'Max')" # MeSsaGe
                    #msg = "Set 'Min' to %s (= 'Max')" % str(a_min) # MeSsaGe
                    #msg = "Set 'Min' to " + str(a_min) + "( = 'Max')") # MeSsaGe
                else: # san_min=False & san_max=False
                    msg = "Missing 'Min' and 'Max' might cause problems!" # ???
                # end if san_min elif san_max
                return (0.0, msg)
            else:  # a_cnt != 0
                if not san_min:
                    return (CALC_ERR_MSG,
                            "Need value for 'Min' to calculate 'Step'!")
                elif not san_max:
                    return (CALC_ERR_MSG,
                            "Need value for 'Max' to calculate 'Step'!")
                else:  # san_min=True and san_max=True
                    if a_min == a_max:
                        set_cnt_zero()
                    return ( (a_max - a_min) / a_cnt,)
                             #"Successfully calculated 'Step'.")
                # end if not san_min elif not san_max else
            # end if a_cnt == 0 else
        # end if not san_cnt else
    elif to_calc == "cnt":  # count = ( max - min ) / step # similar to before but stp <-> cnt
        if not san_stp:
            if san_min and san_max:
                if a_min == a_max:
                    # set_stp_zero() : # useful because not san_stp
                    a_stp = 0.0
                    window["ast_cnt_"+elm].update(a_stp)
                    values["ast_cnt_"+elm] = a_stp  # for total_count
                    # end set_stp_zero()
                    return (0, "Set 'Step' to " + str(a_stp))
                else:
                    return (CALC_ERR_MSG,
                            "Need an (int) value for 'Step' or 'Min'='Max' to calculate 'Count'!")
                # end if a_min == a_max
            else:
                return (CALC_ERR_MSG,
                        "Too less (meaningfull) values given for calculating 'Count'!")
            # end if san_min and san_max
        else:  # san_stp=True
            if a_stp == 0: # 0.0
                if san_min:
                    a_max = a_min
                    window["ast_max_"+elm].update(a_max)
                    return (0, f"Set 'Max' to {a_max} (= 'Min')")
                    return (0, "Set 'Max' to %s (= 'Min')" % str(a_max) )
                    #return (0, "Set 'Max' to " + str(a_max) + "( = 'Min')")
                elif san_max:
                    a_min = a_max
                    window["ast_min_"+elm].update(a_min)
                    return (0, f"Set 'Min' to {a_max} (= 'Max')" )
                    #return (0, "Set 'Min' to %s (= 'Max')" % str(a_min) )
                    #return (0, "Set 'Min' to " + str(a_min) + "( = 'Max')")
                else: # neither san_min nor san_max
                    return (CALC_ERR_MSG,
                            "Need at least also 'Min' or 'Max' to calculate 'Count'!")
                # end if san_min elif san_max
            else:  # a_stp != 0
                if not san_min:
                    return (CALC_ERR_MSG,
                            "Need value for 'Min' to calculate 'Count'!")
                elif not san_max:
                    return (CALC_ERR_MSG,
                            "Need value for 'Max' to calculate 'Count'!")
                else:  # san_min=True and san_max=True
                    return (try_2_int( (a_max - a_min) / a_stp + iv_delta ),)
                            #"Successfully calculated 'Count'.")
                # end if not san_min elif not san_max else
            # end if a_stp == 0 else
        # end if not san_stp else
    # end if to_calc == ...
    #
    # To Do: z.B. cnt = 0 berechnet (weil min = max) dann stp bleibt zwar wert
    #             aber ausgrauen, wenn nicht == 0.0
    #
    # incl., excl.
    # -------+---------+-----------------+
    #       |         |      Count      |
    # Werte | Interv. +-----+-----+-----+
    #       |         | i i | i e | e e |
    # -------+---------+-----+-----+-----+
    #     5 |       4 |   5 |   4 |   3 |
    # -------+---------+-----+-----+-----+
    #     4 |       3 |   4 |   3 |   2 |
    # -------+---------+-----+-----+-----+
    #     3 |       2 |   3 |   2 |   1 |
    # -------+---------+-----+-----+-----+
    #     2 |       1 |   2 |   1 | * 0 |
    # -------+---------+-----+-----+-----+
    #     1 |       0 |   1 | * 0 | *-1 |
    # -------+---------+-----+-----+-----+
#def san_check_and_calc()

def create_range(elm): # float range
    return np.arange(float(values["ast_min_"+elm]),
                     float(values["ast_max_"+elm])
                    +float(values["ast_stp_"+elm]),
                     float(values["ast_stp_"+elm]))
#end def create_range(elm)

def name_coords(ct): # Coord Type
    if ct == "0":
        print("ct-0 branch")
        window["coord_1"].update    ("a   [AU]")
        window["coord_1"].SetTooltip(" Semi-major axis   [Astronomical Units]")
        window["coord_2"].update    (" e")
        window["coord_2"].SetTooltip(" Eccentricity   [pure number]")
        window["coord_3"].update    (" i   [ ° ] ")
        window["coord_3"].SetTooltip(" Inclination   [Degrees 0-360]")
        window["coord_4"].update    (" \u03c9   [ ° ] ") # \u03c9 = \N{greek small letter omega}
        window["coord_4"].SetTooltip(" Argument of periapsis   [Degrees 0-360]")
        window["coord_5"].update    (" \u03a9   [ ° ] ") # \u03a9 = \N{greek capital letter omega}
        window["coord_5"].SetTooltip(" Longitude of the ascending node   [Degrees 0-360]")
        window["coord_6"].update    (" M   [ ° ] ")
        window["coord_6"].SetTooltip(" Mean anomaly   [Degrees 0-360]")
        # \N{SUBSCRIPT two}
    elif ct == "1" or ct == "2":
        print("ct-1|2 branch")
        window["coord_1"].update    (" x   [?]")  # ,background_color="green")
        window["coord_1"].SetTooltip(" x Position   [?]")
        window["coord_2"].update    (" y   [?]")
        window["coord_2"].SetTooltip(" y Position   [?]")
        window["coord_3"].update    (" z   [?]")
        window["coord_3"].SetTooltip(" z Position   [?]")
        window["coord_4"].update    (" v_x   [?]")
        window["coord_4"].SetTooltip(" x Velocity   [?]")
        window["coord_5"].update    (" v_y   [?]")
        window["coord_5"].SetTooltip(" y Velocity   [?]")
        window["coord_6"].update    (" v_z   [?]")
        window["coord_6"].SetTooltip(" z Velocity   [?]")
    else:
        print("ct-no branch")
#end def name_coords(ct)

layout = create_layout()
layout.append([sg.StatusBar(" Please create your Constellation / Solar System!",
                            (93, 0), key="status", tooltip=" StatusBar ",
                            background_color="grey")]) # doppelt!!!

loc = (0, 0)
window = sg.Window('N-Body Lie (1)', location=loc).Layout(layout)

delta_iv = 0 # = Intervals, 1 = Values for asteroids

while True:
    event, values = window.read()
    print("=== event:", event, "===")
    if event in [None, "Cancel"]:
        break
    window["status"].update("")
    if event == "All":  # check all planets checkboxes
        for p in default_planets.keys():
            window["chk_"+p].update(True)
    elif event == "None": # uncheck all planets checkboxes
        for p in default_planets.keys():
            window["chk_"+p].update(False)
    elif "img_" in event: # in list(default_planets.keys()): # if click on planet icon, toggle planet checkbox
        new_key = event.replace("img","chk")
        window[new_key].update(not values[new_key])
    elif event == "Create":
        win_tmp = sg.Window("Please wait ...",
                            [[sg.T("... until constellation is created!")]]).finalize()
        window.Close()
        layout2 = create_layout2()
        #print(layout2)
        window = sg.Window('N-Body Lie Integrator', location=loc).Layout(layout2).finalize()
        name_coords("0")
        # finalize(), damit recalcen kann
        recalc_total() # damit schon anfangs Zahl existiert
        # Problem: dict values ist noch nicht befüllt!
        win_tmp.close()
        #window["coord_type"].Invoke("0: ELE")
    elif event == "Save": # SAVE all parameters
        print(values)
        filename = sg.PopupGetFile("Choose File Name for SAVE-ing")
        print(filename)
        with open(filename, 'wb') as handle: # wb: Write Binary
            pickle.dump(values, handle, protocol=0) # pickle.HIGHEST_PROTOCOL)
    elif event == "Load": # LOAD saved parameters
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
    elif event == "Write": # WRITE input-file for Fortran-program
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
                #print("x_elm["a"] :", x_elm["a"])
                for x_elm["e"] in create_range("e"):
                    #print("  x_elm["e"] :", x_elm["e"])
                    for x_elm["i"] in create_range("i"):
                        #print("    x_elm["i"] :", x_elm["i"])
                        for x_elm["o"] in create_range("o"):
                            #print("      x_elm["o"] :", x_elm["o"])
                            for x_elm["O"] in create_range("O"):
                                #print("        x_elm["O"] :", x_elm["O"])
                                for x_elm["M"] in create_range("M"):
                                    #print("          x_elm["M"] :", x_elm["M"])
                                    for elm in elements:
                                        f.write(form_string[elm].format(x_elm[elm]))
                                    f.write("0.0\n") # mass of asteroid
                                # end for x_elm["M"]
                            # end for x_elm["O"]
                        # end for x_elm["o"]
                    # end for x_elm["i"]
                # end for x_elm["e"]
            # end for x_elm["a"]
            f.write("# a_[AU]        eccentricity      inclinat.     omega         Omega          mean_anom.   mass_[sun]\n")
        #</with open>
        continue
    elif event == "Run":   # RUN Fortran-program
        print("Button 'Run' pressed")
        continue
    elif event == "coord_type":
        ct = values["coord_type"][0] # 1st letter
        print("ct :", ct)
        name_coords(ct)
    elif "_copy" in event: # COPY values from "regular" planet to X-planet
        sourceplanet = values[event] # zB Jupiter
        targetrow = event[:2] # zB x2
        for elm in elements:
            if sourceplanet[0] == "X":
                window["val_" + elm + "_" + targetrow].update(values["val_"+elm+"_"+sourceplanet])
            else:
                 window["val_"+elm+"_"+targetrow].update(default_planets[sourceplanet].__dict__[elm])
    #---- asteroids - stuff ------
    elif event == "iv_i":
        if delta_iv == 0: # nothing to do
            continue # while-loop
        delta_iv = 0
        # recalc: subtract 1 from asteroids-counts
        for elm in elements:
            window["ast_cnt_" + elm].update(float(values["ast_cnt_" + elm]) -1 )
        print("iv_i geklickt")
    elif event == "iv_v":
        if delta_iv == 1: # nothing to do
            continue # while-loop
        delta_iv = 1
        # recalc: add 1 to asteroids-counts
        for elm in elements:
            window["ast_cnt_" + elm].update(float(values["ast_cnt_" + elm]) +1 )
        print("iv_v geklickt")
    elif "ast_" in event:
        print("Asteroiden-Zeux, event:", event)
        elm     = event[-1]  # last letter: ELeMent
        to_calc = event[4:7] # Buchstaben 4, 5 und 6; 7 ist nicht mehr dabei!
        #if to_calc == "ste": to_calc = "step"
        #elif to_calc == "amo": to_calc = "amount"
        if "_calc_" in event:
            #delta_iv = values["iv_v"] # 1 wenn angeklickt, sonst 0
            print("calc: delta_iv:", delta_iv)
            result = san_check_and_calc(delta_iv) # list with 1 or 2 (status_msg) elements
            if len(result) > 1:
                window["status"].update(
                    " Asteroids "+elm+": "+result[1]+" ",
                    text_color = "red" if result[0] == CALC_ERR_MSG else "white")
            result = result[0]
            window["ast_"+to_calc+"_"+elm].update(result)
            values["ast_"+to_calc+"_"+elm] = result # esp. for "cnt"
            #else white ???
                # if len(result) > 2: window["status"].update(text_color = result[2])
            #--- disable calc buttons until new manual change
            #for tc in ("min", "max", "stp", "cnt"): # tc = to_calc
            #    k = "ast_" + tc + "_calc_" + elm # k = key
            #    window[k].update(disabled=True)
            #--- calculating total count of asteroids
            if to_calc == "cnt" and result != CALC_ERR_MSG:
                window["ast_cnt_" + elm].update(result)  # for total_count
                recalc_total()
                if result != int(result):
                    window["ast_" + to_calc + "_" + elm].update(background_color="#ffcccc")
                    window["status"].update(" Count must be a (" \
                                            + ("positive" if delta_iv else "non-negative") \
                                            +") integer! ")
                else:
                    window["ast_" + to_calc + "_" + elm].update(background_color="white")

        else: # <if "_calc_" in event:>
            '''händische Änderung eines asteroiden-inputfeldes, 
            jetzt kontrollieren ob spalte erlaubte Werte liefert'''

            #--- enable calc buttons because of new manual change
            for tc in ("min", "max", "stp", "cnt"):
                k = "ast_" +tc + "_calc_" + elm # key
                window[k].update(disabled=False)

            ### elm = event[-1]
            if "_cnt_" in event: # and "_calc_" not in event:
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
                    window[event].update(background_color="#ffcccc")
                    window["status"].update(" Count must be an integer! ")
                else:
                    window[event].update(background_color="white")
                #  total count of asteroids ausrechnen
                recalc_total()
                #result = 1
                #for elm in elements:
                #    try:
                #        result *= float(values["ast_cnt_" + elm])
                #    except:
                #        print("error calculating count "+elm)
                #        break
                #
                #else:  # schleife lief durch ohne ein einziges break vollständig
                #    print("recalculating without errors. Result=", result)
                #    window["ast_total"].update("Total: {}".format(result))
            #<if "_cnt_" in event: # and "_calc_" not in event:>
        # <if "_calc_" in event:>
    # end if elif event
print("Bye")
