# -*- coding: utf-8 -*-
import turtle as t
import time

from information import display_info, print_result

#konstanter
G = 6.67408E-11     #tyngdekonstanten
AU = 1.496E11       #astronomisk enhet (for skalering)
M = 1.989E30        #solmassen

#animasjonsfunksjonen vår
def update_bodies(bodies, centre, deltat, scale):
    """finner akselerasjonen og oppdaterer farten og posisjonen på planetene"""
    
    #looper gjennom alle par av legemer og finne summen av kreftene på dem
    for p in bodies:
        #summen av kreftene i x- og y-retning
        sum_x = sum_y = 0
        
        for q in bodies:
            #vi vil ikke regne ut kraften fra et legee på seg selv
            if (p == q): 
                continue
            
            #tyngden i x- og y-komponent fra q på p
            gx, gy = p.gravity_pull(q)
            
            #legger de til i summen
            sum_x += gx
            sum_y += gy
            
        #oppdaterer posisjonen ved å se på nåværende fart
        p.x += p.vx * deltat
        p.y += p.vy * deltat
        
        #oppdaterer farten ved å se på akselerasjonen (eulers metode)
        #vi må dele på massen for å få akselerasjonen (a = (\Sigma F) / m)
        p.vx += (sum_x / p.m) * deltat
        p.vy += (sum_y / p.m) * deltat
        
def animate(bodies, centre, deltat, scale, timer, step):
    """animerer planetenes bevegelse"""    
    #oppdater planetens info og tegner deres posisjon
    update_bodies(bodies, centre, deltat, scale)
    
    #tegner streker og oppdaterer info i konsoll ved gjevne tidsmellomrom
    if (int(timer / deltat) % 100 == 0):
        #oppdater konsollinfo
        display_info(bodies, timer)
            
        #tegn banelinjer og posisjon
        for b in bodies:
            b.draw_line(scale, centre)
            #tegner planetens posisjon
            b.draw_dot(scale, centre)

    #gi tilbake neste sekundtelling
    return timer + deltat
        
#denne må være global for at vi skal kunne endre på den i zoome funksjonene våre
frame_size = 1000
#rammen vår i de 4 koordinatene (må også være global)
center = [0, 0]
def simulate(planet_name, centre_name, system, relative_orbit, deltat, err, scalar, step):
    """simulerer banene med utgangspunkt i valgt planet og gitte betingelser"""
    
    """ jeg definerer disse funksjonene inline fordi funksjonen i screen.onkey()
        ikke kan ta argumenter og jeg ønsker ikke å gjøre screen og bodies til
        globale variabler, altså må zoom_in og zoom_out ha tilgang til screen
        og bodies i sitt eget scope, så de må være definert inni simulate()
    """
    def reset_screen(screen, bodies):
        """hver gang screen.setwordlcoordinates() kalles, blir alle turtle
        innstillingene resettet av en eller anngen grunn, så vi denne funksjonen
        setter de tilbake til ønskede innstilinger"""
        #endrer skjermstørrelsen med hensyn på nævernde zoom
        screen.setworldcoordinates(center[0] - frame_size, center[1] - frame_size,
                                       center[0] + frame_size, center[1] + frame_size)
        
        #stiller inn skilpaddene til ønskede innstillinger
        for b in bodies:
            b.turtles_reset()
    
    """vi velger å zoome eksponensielt fordi i desto lenger ut vi beveger oss
    i universet, desto større mellomrom er det mellom ting. vi må også resette
    displayet for at zoomingen skal komme i effekt."""
    
    zoom_ammount = 1.5
    
    def zoom_out():
        #henter variabelen inn i dette scopet
        global frame_size
        #zoomer ut
        frame_size *= zoom_ammount
        reset_screen(screen, bodies)
        
    def zoom_in():
        #henter variabelen inn i dette scopet
        global frame_size
        #zoomer inn
        frame_size /= zoom_ammount
        reset_screen(screen, bodies)
        
        
    """funksjoner for å flytte seg i skjermen"""
    #avstnd vi beveger oss er avhengig av hvor langt vi har zoomet inn
    move_ammount = .4
    
    def move_up():
        global center, frame_size
        center[1] += frame_size * move_ammount;
        reset_screen(screen, bodies)
            
    def move_down():
        global center, frame_size
        center[1] -= frame_size * move_ammount;
        reset_screen(screen, bodies)
            
    def move_right():
        global center, frame_size
        center[0] += frame_size * move_ammount;
        reset_screen(screen, bodies)
    
    def move_left():
        global center, frame_size
        center[0] -= frame_size * move_ammount;
        reset_screen(screen, bodies)
        
    """funksjoner for å endre farge"""
    def light_mode():
        #bakgrunnsfarge
        t.bgcolor("white")
        
    def dark_mode():
        #bakgrunnsfarge
        t.bgcolor("black")
        
    #legemene vi skal animere
    bodies = system
    
    centre = False
    
    #finner ønsket planet blant planetene våre
    for b in bodies:
        if b.name == planet_name:
            #planeten vi skal undersøke
            planet = b
        if b.name == centre_name:
            #planeten vi kretser om
            centre = b
            
    #for optimalisering av tegning
    screen = t.Screen()         #setter opp grafikkfeltet
    screen.tracer(0, 0)         #ingen aning hvordan denen funker 
                                #(men den gjør programmet raskere)
    reset_screen(screen, bodies)#setter opp skjermen med standard zoom
    
    #sekundteller (i animasjonen)
    timer = 0
    
    #sekundteller (i virkeligheten)
    t0 = time.time()
    
    #vi fortsetter til ønsket planet har gått én hel runde dersom ikke
    #uendelig animasjon er skrudd på
    while (planet_name == "" or not planet.period_done(err, relative_orbit)):
        #vi vil kunne zoome ut og inn, så vi må aktivt sjekke om knapper trykkes
        screen.onkey(zoom_out, "Down")    #piltast ned
        screen.onkey(zoom_in, "Up")       #piltast opp
        
        #vi vil kunne bevege oss rundt
        screen.onkey(move_up, "w")      #opp
        screen.onkey(move_left, "a")    #venstre
        screen.onkey(move_down, "s")    #ned
        screen.onkey(move_right, "d")   #høyre
        
        #farge
        screen.onkey(light_mode, "l")
        screen.onkey(dark_mode, "b")
        
        screen.listen()
        
        #animer systemet og oppdater timeren
        timer = animate(bodies, centre, deltat, scalar / AU, timer, step)
        
        #refresh skjerm (trengs pga. screen.tracer())
        screen.update()    
    
    #sluttid i sekunder (realtime)
    t1 = time.time()
    
    #print resultater av simulasjonen (tiden brukt er dif. mellom slutt- og starttid)
    print_result(planet, timer, deltat, err, t1 - t0)
    
    #avslutter turtle slik at den ikke kræsjer
    t.done()
    