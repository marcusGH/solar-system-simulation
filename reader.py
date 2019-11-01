# -*- coding: utf-8 -*-
def reader(loc):
    """samler NASA-dataen i en ordbok der hver planet er en 
    key for en ordbok med sin data"""
    #returverdi
    ret = {}    #dictionary
    #åpner gitt fil
    with open(loc, "r") as file:
        #henter inn nøklene fra toppen av filen, fjerner nyline-karakteren og
        #lager en array med nøkler som tilsvarer informasjonen som kommer senere
        keys = file.readline().replace('\n', '').split(',')     #kommaseparert data
        
        #går gjennom alle linjene med planetdata
        for line in file:
            #fjerner newline-karakteren og deler linja opp etter ulik data 
            #tilsvarende nøklene. vi får en array med data der data[i] har data
            #om keys[i].
            data = line.replace('\n', '').split(',')
            
            #vi lager en ordbok for de ulike verdiene til planeten
            planet_data = {}
            #går gjennom all dataen utenom navnet (den første verdien)
            for i in range(1, len(data)):
                #og kobler den sammen med tilsvarende nøkkel
                try:
                    #vi ønsker å ha tall-variabler hvis mulig
                    planet_data[keys[i]] = float(data[i])
                except ValueError:
                    #ellers lagrer vi det som en streng
                    planet_data[keys[i]] = data[i]
                
            #vi kobler så denen dataen til planetnavnet
            #key = name, value = info om planeten
            ret[data[0]] = planet_data
        
    #gi så alle oppsamlet data tilbake
    return ret
