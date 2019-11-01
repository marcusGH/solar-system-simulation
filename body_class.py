# -*- coding: utf-8 -*-
import numpy as np
import turtle as t
import math
import random as r

#konstanter
G = 6.67408E-11     #tyngdekonstanten
AU = 1.496E11       #astronomisk enhet (for skalering)
M = 1.989E30        #solmassen

#jeg bruker klasser for å organisere dataen til legemmene på en kompakt måte
class Body():
    #planetene i bane har ekstra informasjon knyttet til seg, så vi har en
    #egen funksjon for dem
    def init_planet(self, input_data, planet, centre, random):
        """ 
         *   ------------------
         *   Initialiserer Body-klassen med planetens data fra planet_data.
         *   Denne funksjonen fungerer også for måner fordi vi bare ser på
         *   banen i forhold til et sentrum, så vi lar sola være sentrum hvis
         *   vi har en planet. For måner bruker vi en spesifik planet som
         *   sentrum, for eksempel jorda dersom vi ser på månen.
         *   ------------------
        """
        #henter ut dataen om valgt planet
        planet_data = input_data[planet]
        
        #vi trenger navnet til senere informasjonsprinting
        self.name = planet
        
        #det samme gjelder referanselegemet, altså legemet det krester rundt
        self.centre = centre
        
        #massen fra datasettet gitt i 10^24 kg
        self.m = planet_data["mass"] * 1E24
        
        #dataen på avstanden er gitt i antall millioner kilometer, altså 10^9 m
        #for måner tar denne dataen utgangspunkt i planeten den kretser om, 
        #ikke sola
        self.d = planet_data["distance_from_sun"] * 1E9  #midt imellom pe og ap
        self.pe = planet_data["perihelion"] * 1E9        #perioapsis er minste avstand
        self.ap = planet_data["aphelion"] * 1E9          #apoapsis er største avstand
        
        #rundetiden er gitt i antall dager, altså 24*60*60 sekunder
        self.T = planet_data["orbital_period"] * 24 * 60 * 60
        
        #initialiserer startpos og fart
        
        if (random):
            #tilfeldig startvinkel for alt
            start_ang = r.uniform(0, 2 * np.pi)
            
            #startpunktet er i aphelion
            self.x = centre.x + math.cos(start_ang) * self.ap
            self.y = centre.y + math.sin(start_ang) * self.ap
            
            #absoluttverdien av hastigheten
            v = np.sqrt(G * centre.m * (2 / self.ap - 1 / self.d))
            
            #farten er den farten man får i øverste punktet
            self.vx = centre.vx - math.cos(start_ang - np.pi / 2) * v
            self.vy = centre.vy - math.sin(start_ang - np.pi / 2) * v
            
        else:
            #vi ønsker å starte banen vår rett øst for senteret og
            #i planetens/månenes høyeste punkt i banen (apoapsis)
            #så vi starter i senterets posisjon og beveger oss til høyre
            #tilsvarende høyden planetens/månens bane i det høyeste punktet
            self.x, self.y = centre.x + self.ap, centre.y
            
            #absoluttverdien av hastigheten i øverste punkt i eliptisk bane
    
            #Vi får denne formelen ved å se på bevart mekanisk energi i 
            #flytting fra sirkulær- til elpitisk bane
            #vi må bruke massen til legemet vi går rundt
            v = np.sqrt(G * centre.m * (2 / self.ap - 1 / self.d))
            
            #i utgangspunktet peker fartsvektoren rett opp. Vi lar også planeten
            #rotere i positiv retning. Vi må også ta hensyn til sentrumets hastighet
            #i sin bane ettersom en måne også kretser om sola, så vi legger til 
            #den relative banehastigheten til sentrumets hastighet i sine bane
            self.vx, self.vy = 0, v + centre.vy
            
    
    #initialisering av legemeet (vi har mange valgfrie argumenter, så 
    #vi gir parameterne en default verdi slik at man kan ignorere dem)
    def __init__(self, m = 0, x = 0, y = 0, vx = 0, vy = 0, name = "NaN", random = True,
                 color = "black", centre = False, planet = False, input_data = None):
        """ --------------------------
            intialiseringsklassen vår:
            
            m       = masse
            x, y    = x- og y-koordinatene 
            vx, vy  = x- og y-komponetene til fartsvektoren
            name    = navnet vi tilegner legemet
            color   = fargen vi tegner legemet med
            
            De tre neste parameterne bruker vi dersom vi har en planet/måne 
            i bane rundt noe
            
            centre     = legemet det går rundt (referanselegeme) (sola for planetene)
            planet     = hvilken planet i datasettet vi henter info om
            input_data = ordboka med all dataen fra NASA
            -------------------------- """
              
        #Vi ønsker både en prikk for planeten og en linje som følger den
        #derfor tilegner vi hver planet to "turtle"-er
        self.turtle_dot = t.Turtle()
        self.turtle_line = t.Turtle()
        
        #vi må kunne hente opp fargen senere når vi skal tegne planetene
        self.color = color
        
        #default-instillingene til turtle er uønskede, så vi setter våre egne
        self.turtles_reset()        
        
        #vi har en egen initialiseringsmetode for planetene i bane rundt sola
        #ettersom de har en bestemt eliptisk bane
        if (planet):
            self.init_planet(input_data, planet, centre, random)
            
        #og en annen for andre legemeer (uten spesifike baner)
        else:
            #se notat over
            self.m = m
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            #dersom det ikke er en planet, må vi gi et navn som argument
            self.name = name
            
        #vi trenger å vise at denne variabelen ikke har noen verdi første gang
        #draw_line() funksjonen kjøres
        self.prev_pos = False
        
        #Variabelen sier om vi har gjort ferdig en halv bane om sentrumet
        #vi starter med å nettop ha fulført en helt bane, så denne er False
        self.half_orbit_done = False    #trengs til period_done()
        
    def dist(self, other):
        """avstanden til et annet legeme"""
        #bruker bare pytagoras på delta-x og delta-y
        return np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def gravity_pull(self, other):
        """returnerer hhv. x- og y-komponenten til tyngden fra other på self"""
        #For å slippe å gjøre samme operasjoner 2 ganger, finner vi første
        #denne komponenten og gjenbruker den to ganger
        temp = G * self.m * other.m / self.dist(other)**3
        gx = temp * (other.x - self.x)      #x-komponenten til tyngden
        gy = temp * (other.y - self.y)      #y-komponenten til tyngden
        
        #returnerer x- og y-komponentene til tyngden
        return gx, gy
    
    def turtles_reset(self):
        """resetter turtle-ene til ønskede innstillinger"""
        #Vi vil ikke se en stor trekant på tegninga
        self.turtle_dot.hideturtle()
        self.turtle_line.hideturtle()
        
        #starter med pennen oppe for å unngå unødvendig tegning
        self.turtle_dot.penup()
        self.turtle_line.penup()
        
        #alle legemer har en farge i turtle-plottet
        self.turtle_dot.pencolor(self.color)
        self.turtle_line.pencolor(self.color)
    
    def relative_pos(self, other):
        """returnerer posisjonen i forhold til en annen planet dersom den andre
        planeten var i sentrum av solsystemet"""
        
        #avstanden mellom planeten
        d = self.dist(other)
        #angle between planets
        ang = math.atan2(self.y - other.y, self.x - other.x)
        
        #returns new position
        return d * math.cos(ang), d * math.sin(ang)
        
    def draw_dot(self, scale, centre):
        """tegner legemet der det befinner seg med riktig skala"""
        #vi ønsker ikke å se spor av dottene, så vi vasker skjermen for disse
        self.turtle_dot.clear()
        
        #finn posisjon
        if (centre):
            x, y = self.relative_pos(centre)
        else:
            x, y = self.x, self.y
        
        #gå til posisjon og tegn
        #for at grafikkfeltet ikke skal bli for stort, nedskalerer vi det        
        self.turtle_dot.goto(x * scale, y * scale)
        #7 er en passende størrelse på prikken
        self.turtle_dot.dot(7)
    
    def draw_line(self, scale, centre):
        """tegner en line fra forrige linjeslutt til planetens nåværende posisjon"""
        
        #finn posisjon
        if (centre):
            x, y = self.relative_pos(centre)
        else:
            x, y = self.x, self.y
        
        #første gang vi kjører denne funksjonen (prev_pos initialisert til False)
        if (not self.prev_pos):
            #vi setter prev_pos til nåværende posisjon
            self.prev_pos = x * scale, y * scale
        
        #nåverende posisjon (med riktig skala)
        self.cur_pos = x * scale, y * scale
        
        #tegner en linje fra forrige posisjon til nåværende posisjon
        self.turtle_line.penup()
        self.turtle_line.goto(self.prev_pos)
        self.turtle_line.pendown()
        self.turtle_line.goto(self.cur_pos)
        self.turtle_line.penup()
        
        #og oppdaterer forrige posisjon til neste gang vi kjører funksjonen
        self.prev_pos = self.cur_pos
    
    def angle(self, relative_angle = True):
        """returnerer vinkelen i omløpet i forhold til legemet i sentrum.
           Dersom vinkelen er satt til å være absolutt, er det i forhold 
           til grafikkfeltet og ikke legemet objektet går i bane rundt"""
        if (not relative_angle):
            #vi må reverse x-komponenten for å få riktig trekant
            rad = math.atan2(-self.vx, self.vy)
        else:
            #vi må ta hensyn til legemet det kretser rundt for å finne
            #relativ fart i forhold til dette. Vi trekker derfor fra dens fart
            rad = math.atan2(-(self.vx - self.centre.vx),
                             (self.vy - self.centre.vy))
            
        #arctan gir svaret i radianer
        ang = math.degrees(rad)     #V_f = [-180, 180)
        return ang
    
    def period_done(self, err, relative_orbit = True):
        """sjekker om legemet har gått en hel runde"""
        #vi beregner vinkelen utifra om si ser på bane rundt f.eks. sola eller jorda
        if (relative_orbit):
            #vi vil ha relativ vinkel
            ang = self.angle(True)
        else:
            ang = self.angle(False)
        
        #vi har gått en hel runde
        if (self.half_orbit_done and abs(ang) < err):
            self.half_orbit_done = False
            return True
        
        #vi har nettop gått en halv runde
        elif (not self.half_orbit_done and abs(ang) > 180 - err):
            self.half_orbit_done = True
            return False
        
        #dersom ingenting skjer, gi False
        else:
            return False
    
    def print_info(self):
        """printer info om legemet"""
        #alle planeter har ikke disse egenskapene
        #men vi prøver å legge dem til hvis vi kan
        try:
            #vi lagrer variablene som strenger slik at vi kan printe "NaN"
            #dersom tallene ikke er tilgjengelig
            ap = f"{self.ap:.4e}"
            pe = f"{self.pe:.4e}"
            d = f"{self.dist(self.centre):.4e}"
            ang = f"{self.angle():.2f}"
        #ellers ignorer vi dem
        except AttributeError:
            #vi må ha litt mellomrom for å kompansere for tallets lengde
            ap = pe = d = ang = "NaN     "
        
        #vi printer ut informasjonen med tabulatorer
        print(f"{self.name}\t\t"+
              ang + "\t\t" + pe + "\t\t"+ d + "\t\t"+ ap)
        