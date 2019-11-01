# -*- coding: utf-8 -*-

#siden prosjektet har endt opp som veldig omfattende, har jeg delt opp koden i flere filer
#jeg importerer så delene av koden etter hvert som jeg trenger den
from simulation import simulate
from planatary_systems import solar_system, binary_star_system, jupiter_system, three_body_system
from random import seed

"""
HOW TO USE:
Skriv inn navnet på planeten i main() funksjonen og kjør programmet.
Bruk "ned"- og "opp"-tastene for å zoome hhv. ut og inn
og "asdw" for å bevege deg rundt.
"""

# -*- coding: utf-8 -*-

#for å unngå mest mulige globale variabler, er hovedoperasjonene i en funksjon
def main():    
    """ -------------initialbetingelser for simulasjonen -------------------"""
    #antall sekunder vi går mellom hvert steg
    deltat =  (60)
    #feilmargin for vinkelen til planeten
    err = .2            #antall grader
    #random seed for random generatoren
    seed(42)
    #planeten/månen vi ønsker å observere rundetiden til
    planet = ""
    #systemet vi skal animere
    system = solar_system(planet)
    #planeten vi setter i sentrum av solsystemet
    centre = "Moon"
    #vil vi se når planeten går rundt sentrumet i sin abolsutte bane, 
    #eller relativt til et annet legeme (sentrumet til planetens bane)?
    relative_orbit = True
    
    """ -------------initialbetingelser for grafikken ----------------------"""
    #skalar slik at ting får plass i turtle-grafikkfeltet
    scalar = 100    #antall turtle-enheter per astronomisk enhet
    #antall steg vi venter mellom å oppdatere konsollinfo og linjer bak planetene
    step = 100
    
    #kjører simulasjonen
    simulate(planet, centre, system, relative_orbit, 
             deltat, err, scalar, step)

#kaller hovedfunksjonen vår
main()