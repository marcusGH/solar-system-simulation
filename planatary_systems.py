# -*- coding: utf-8 -*-
import numpy as np

from reader import reader
from body_class import Body

#konstanter
G = 6.67408E-11     #tyngdekonstanten
AU = 1.496E11       #astronomisk enhet (for skalering)
M = 1.989E30        #solmassen

#-------------------- Diverse planetsystemer som vi kan leke med --------------

def solar_system_aux(names, colors, centre, planet_name, input_data):
    ret = []
    for i in range(len(names)):
        #hovedplanet skal starte vanlig
        if (names[i] == planet_name):
            random = False
        else:
            random = True
        ret.append(Body(planet=names[i], centre=centre, 
                        color=colors[i], input_data = input_data, random=random))
        
    return ret
    

def solar_system(planet_name):
    """returnerer alle planetene i solsystemet"""
    #leser inn data
    input_data = reader("data/solar_system.txt")
    
    """
    Vi definerer alle planetene vi ønsker. Dette kunne enkelt blitt gjort i en
    funksjon (se jupiter-systemet), men da mister vi muligheten til å bestemme
    fargene på planetene på en oversiktlig måte. Derfor har jeg gjort det slik
    jeg gjorde nedenfor"""
    
    ret = []
    
    #sola må defineres som en punktmasse uten fart i sentrum
    sun = Body(M, color="yellow", name="Sun")
    
    planet_names = ["Earth", "Mars", "Venus", "Mercury", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
    planet_colors = ["blue", "red", "green", "brown", "brown", "yellow", "yellow", "blue", "grey"]
    
    #alle planetene
    ret += solar_system_aux(planet_names, planet_colors, sun, planet_name, input_data)
    ret.append(sun)
    
    #månen (jorda er den første planeten)
    ret.append(Body(planet="Moon",  centre=ret[0], color="grey", input_data = input_data))

    #deimos = Body(planet="Deimos", centre=mars, color="brown",  input_data = input_data)
    #phobos = Body(planet="Phobos", centre=mars, color="yellow", input_data = input_data)
       
    #returnerer en array med alle planetene
    return ret
    
def jupiter_system():
    """returnerer jupiter og dens måner"""
    #leser inn data
    input_data = reader("data/jupiter_moons.txt")
    
    #definerer sentrumet som planeten jupiter 
    #(vi bruker her det zevsentriske systemet) (jupiters navn på gresk = zevs)
    jupiter = Body(1.89E27, color="red", name="Jupiter")
    
    #månene
    moons = []
    #orker ikke å gi planetene forskjellige farger, så legger de til i en loop
    for key in input_data:
        #alle kretser om jupiter og vi bryr oss ikke om fargene
        moons.append(Body(planet=key, centre=jupiter, input_data = input_data, color="white"))
    
    #retunerer lista over alle planetene
    return [jupiter, *moons]

def three_body_system():
    """returnerer 3 soler"""
    
    sun1 = Body(M, 1E11, 0, 0, 2.5E4, color="green")
    sun2 = Body(M, -3E10, 3E10, 1.5E4, -1E4, color="red")
    sun3 = Body(M, -3E10, -3E10, -4E4, -3E4, color="blue")
    sun4 = Body(M, -1E12, 0, 5E4, 1E3, color="grey")
    sun5 = Body(M, 1E12, 0, 0, 0, color="yellow")
    sun6 = Body(M * 100, 0, 3E12, 1E5, -4E5, color="brown")
    sun7 = Body(M * 10000, 0, -5E12, np.sqrt(G * M * 2500 / 5E12), 0, color="black")
    sun8 = Body(M * 10000, 0, 5E12, -np.sqrt(G * M * 2500 / 5E12), 0, color="black")
    
    return [sun1, sun2, sun3, sun4, sun5, sun6, sun7, sun8]

def binary_star_system():
    """dobbeltstjernesystemet fra oppgave 4-11 i fysikkboka"""
    #avstanden mellom stjernene
    d = 3E12
    
    #massen til stjernene
    m_a = 2.1 * M
    m_b = 1.0 * M
    
    #radiusene i banen deres
    r_a = d / 3.1
    r_b = 2.1 * r_a
    
    #banefarten deres
    v_a = np.sqrt(G * m_b * r_a / d**2)
    v_b = np.sqrt(G * m_a * r_b / d**2)
    
    #planetene
    A = Body(m_a, r_a, 0, 0, v_a, name="Sirius A", color="blue")
    B = Body(m_b, -r_b, 0, 0, -v_b, name="Sirus B", color="red")
    
    #returnerer planetene
    return [A, B]