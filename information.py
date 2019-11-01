# -*- coding: utf-8 -*-
def sec_to_time(sec):
    """gjør om antall sekunder til et finere tidsformat"""
    
    #vi må håndtere et positivt tall for å unngå blandede fortegn
    if (sec < 0):
        sec *= -1
        #men vi husker at tallet er negativt
        ret = "- "
    else:
        ret = ""
        
    #hent antall år
    years = sec // (365*24*60*60)
    sec -= years * (365*24*60*60)
    
    #hent antall dager
    days = sec // (24*60*60)
    sec -= days * 24*60*60
    
    #hent antall timer
    hours = sec // (60*60)
    sec -= hours * 60*60
    
    #hent antall minutter
    minutes = sec // 60
    sec -= minutes * 60
    
    #sec bestemmer nå gjenværende sekunder
    
    #returnerer tiden som en f-literal for enkel bruk videre
    ret += f"{years} år, {days} dager, {hours} timer, "
    ret += f"{minutes} minutter og {sec:.2f} sekunder"
    
    return ret

def display_info(bodies, timer):
    """printer en fin tabell med relevant info til konsollen"""
    #lager fin tabell
    print("-" * 100)
    
    #overskrifter med enheter
    print(f"Name\t\tAngle (grader)\tPerioapsis (meter)\tDistanse (meter)\tApoapsis (meter)")
    #bruker seperate funksjon for alle planetene
    for b in bodies:
        b.print_info()
        
    #print info om simulert tid i simulasjonen
    print(f"\nTid passert: " + sec_to_time(timer))
    
    #slutt tabell
    print("-" * 100)
    
def print_result(planet, timer, deltat, err, time_elapsed):
    """printer resultatene fra simulasjonen"""
    #vi vil skille den litt fra alle tabellene vi tidligere har printet ut
    print("\n\n")
    
    print("*" * 100) #fin ramme
    
    #print all informasjonen vi trenger (reeltid brukt på simulasjon,
    #delta-t og feilmarginen for vinkelen)
    print(f"Simulering av rundetid for {planet.name} ferdig på " +
          sec_to_time(time_elapsed) + " sekunder med følgende parametre:\n")
    print(f"Deltat-t: {deltat} sekunder (" + sec_to_time(deltat) + ")")
    print(f"Feilmargin: {err} grad(er)")
    
    print("-" * 50) #fint skille
    
    #printer info om planetens rundetid (simulert tid)
    print(f"Tid brukt i simuluasjon: " + sec_to_time(timer))
    #ikke sikkert planeten har disse attributtene
    try:
        #men hvis den har det, så printer vi det i fint format
        print(f"Tid ifølge NASAs data: " + sec_to_time(planet.T))
        #hvis vi samenlikner t med t_0 har vi: avvik i % = (t - t_0) / (t_0 * 100)
        print(f"Dette gir et avvik på: " + sec_to_time(timer - planet.T) +
              f" ({(timer - planet.T) * 100 / (planet.T):.4f} % avvik)")
    except:
        pass
    
    print("*" * 100) #fin ramme

