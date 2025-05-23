# ==========================================================Import==============================================================
import json
import os
import random
import time


# ==========================================================Spartfil==============================================================
SPARFIL = "speldata.txt"
# ==========================================================Variabel==============================================================
bonus_mot_alvin = False
inventory = []
karaktär = ""
karaktär_bonus = {}
# ==========================================================MENY==============================================================
def visa_instruktioner():
    try:
        with open("readme.txt", "r", encoding="utf-8") as fil:
            print(fil.read())
    except FileNotFoundError:
        print("readme.txt kunde inte hittas.")

def start():
    print("=== FLY FRÅN ALVIN ===")
    print("1. Starta nytt spel")
    print("2. Ladda sparat spel")
    print("3. Radera sparat spel")
    print("4. Läs spelinstruktionerna")
    val = input("Välj ett alternativ: ").strip()

    if val == "1":
        nytt_spel()
    elif val == "2":
        om_laddad = ladda_spel()
        if om_laddad:
            print("Spelet återupptas...")
            ett_till_rum() 
        else:
            nytt_spel()

    elif val == "3":
        radera_sparfil()
        start()
    elif val == "4":
        visa_instruktioner()
        input("PRESS any wordle to get back ")
        start()
    else:
        print("Ogiltigt val.")
        start()


# ==========================================================Funktion för sparfil==============================================================
# funktion för att spara spelet
def spara_spel():
    # variabler i spelet vars data sparas
    data = {
        "bonus_mot_alvin": bonus_mot_alvin,
        "inventory": inventory,
        "karaktär": karaktär,
        "karaktär_bonus": karaktär_bonus,
    }
# öppnar filen som heter SPARFIL i skrivläge och sparar datan som JSON
    with open(SPARFIL, "w") as f: 
        json.dump(data, f) # Skriver dictionary till filen i JSON format
    print("Spelet har sparats!")

# Funktion att ladda ett psarat spel 
def ladda_spel():
    # Deklarerar att de här variablerna är globala 
    global bonus_mot_alvin, inventory, karaktär, karaktär_bonus
# Den kollar så att filen finns annars ett medelande 
    if not os.path.exists(SPARFIL):
        print("Ingen sparfil hittades.")
        return False
# öppnar filen och läser tillbaka datan till programet
    with open(SPARFIL, "r") as f:
        # Skriver in JSON innehållet in i vårat directory 
        data = json.load(f)
# ladda in de värden vi har sparat
    bonus_mot_alvin = data["bonus_mot_alvin"]
    inventory.clear()
    inventory.extend(data["inventory"])
    karaktär = data["karaktär"]
    karaktär_bonus = data["karaktär_bonus"]

    print(f"Spelet laddades! Du spelar som {karaktär} och har {len(inventory)} föremål.")
    return True

# tar bort den sparade filen 
def radera_sparfil():
    # kollar så att filen finns annars error medelande
    if os.path.exists(SPARFIL):
        os.remove(SPARFIL)
        print("Sparfilen har raderats.")
    else:
        print("Ingen sparfil att radera.")


# ===============================================================Start Definitioner==============================================================
def välj_karaktär():
    global karaktär, karaktär_bonus
    print("\nVälj din karaktär:")
    print("1. Krigare – Extra skada varje attack (+2 dmg)")
    print("2. Läkare – Bättre läkning (+5 HP vid läka)")
    print("3. Tjuv – Undviker fiendeattacker ibland (25% chans)")
    print("4. Alkemist – Föremålseffekter förstärks")

    val = input("Ange numret på din karaktär: ").strip()

    if val == "1":
        karaktär = "Krigare"
        karaktär_bonus = {"extra_skada": 2}
    elif val == "2":
        karaktär = "Läkare"
        karaktär_bonus = {"extra_läkning": 5}
    elif val == "3":
        karaktär = "Tjuv"
        karaktär_bonus = {"undvik_chans": 0.25}
    elif val == "4":
        karaktär = "Alkemist"
        karaktär_bonus = {"föremål_bonus": True}
    else:
        print("Ogiltigt val. Försök igen.")
        välj_karaktär()

    print(f"\nDu valde {karaktär}!")

def visa_ryggsäck():
    if inventory:
        print("\n Föremål i din ryggsäck:")
        for i, item in enumerate(inventory, 1):
            print(f"{i}. {item}")
    else:
        print("\n Din ryggsäck är tom.")

def använd_föremål():
    if not inventory:
        print("Du har inga föremål att använda.")
        return 0

    visa_ryggsäck()
    val = input("Ange numret på föremålet du vill använda (eller tryck Enter för att avbryta): ").strip()
    print()
    if val == "":
        return 0

    try:
        index = int(val) - 1
        föremål = inventory[index]
    except (ValueError, IndexError):
        print("Ogiltigt val.")
        return 0

    if föremål == "healing-potion":
        heal = random.randint(15, 25)
        if karaktär_bonus.get("föremål_bonus"):
            heal += 10
        inventory.remove(föremål)
        print(f"Du använder en healing-potion och återfår {heal} HP!")
        return heal

    elif föremål == "mystisk ring":
        extra = random.randint(1,100)
        if karaktär_bonus.get("föremål_bonus"):
            extra += 5
        inventory.remove(föremål)
        print(f"Du sätter på den mystiska ringen och gör {extra} extra skada i denna runda!")
        return -extra

    elif föremål == "stark attack-elixir":
        extra = random.randint(10, 20)
        if karaktär_bonus.get("föremål_bonus"):
            extra += 5
        inventory.remove(föremål)
        print(f"Du använder stark attack-elixir och gör {extra} extra skada i denna runda!")
        return -extra

    else:
        print("Föremålet har ingen effekt just nu.")
        return 0
    
def lägg_till_föremål(föremål):
    inventory.append(föremål)
    print(f"Du har fått ett nytt föremål: {föremål}")
    spara_spel()

# ===============================================================RUM==============================================================

def nytt_spel():
    global bonus_mot_alvin
    bonus_mot_alvin = False
    välj_karaktär()
    print("\nVälkommen till 'Fly från Alvin'. Ditt uppdrag är att hitta en väg ut ur hans hus innan han hittar dig.")
    print("Du är i en cell.")
    har_nyckel = input("Har du nyckeln? (ja/nej): ").strip().lower()

    if har_nyckel == "ja":
        ett_till_rum()
    else:
        print("Du måste hitta nyckeln först. Försök igen!")
        nytt_spel1()

def nytt_spel1():
    global bonus_mot_alvin
    bonus_mot_alvin = False
    print("Du är fortfarande i cellen.")
    har_nyckel = input("Har du nyckeln? (ja/nej): ").strip().lower()

    if har_nyckel == "ja":
        ett_till_rum()
    else:
        print("Du måste hitta nyckeln först. Försök igen!")
        nytt_spel()

def ett_till_rum():
    print("\nDu är i ett till rum.")
    val = input("Vill du gå vänster eller höger? (vänster/höger): ").strip().lower()

    if val == "vänster":
        pussel()
    elif val == "höger":
        Anthin()
    else:
        print("Ogiltigt val. Försök igen.")
        ett_till_rum()
    
def pussel():
    print("\nDu stöter på ett pussel.") 
    pusselval = random.choice(["1", "2", "3"])
    if pusselval == "1":
            svar = input("Gåta: Vad är alltid framför dig men kan aldrig ses? ").strip().lower()
            while svar != "framtiden":
                print("Fel svar, försök igen.")
                svar = input()
                print("Det är inte baktiden.")
                
            print("Rätt svar!")
            lägg_till_föremål("healing-potion")
            tickande_bomb()

    elif pusselval == "2":
            svar = input("Gåta: Vad kan du hålla i din vänstra hand men aldrig i din högra? ").strip().lower()
            while svar != "Höger hand" or "höger hand" or "Din högra hand":
                print("Fel svar, försök igen.")
                svar = input()
                print("Det är inte din högra fot (Det kan jag lova).")
                
            print("Rätt svar!")
            lägg_till_föremål("healing-potion")
            tickande_bomb()

    elif pusselval == "3":
            svar = input("Gåta: Vad har ett öga men kan inte se? ").strip().lower()
            while svar != "En nål" or "en nål" or "nål":
                print("Fel svar, försök igen.")
                svar = input()
                print("Det är inte en flygel (det må det inte vara!)")
                
            print("Rätt svar!")
            lägg_till_föremål("healing-potion")
            tickande_bomb()

def tickande_bomb():
    global bonus_mot_alvin
    print("\nDu går vidare men upptäcker en TICKANDE BOMB!")
    print("Du måste avaktivera bomben genom att skriva in rätt kod innan tiden går ut.")
    kod = str(random.randint(1, 10))
    försök_kvar = 3

    while försök_kvar > 0:
        gissning = input(f"\nSkriv en siffra i intervallet 1-10 kod (1-10) (Försök kvar: {försök_kvar}): ")
        if gissning == kod:
            print("Du lyckades avaktivera bomben! Du får en bonus i nästa strid.")
            bonus_mot_alvin = True
            staty_rum()
            return
        else:
            print("Fel kod!")
            försök_kvar -= 1

    print("Bomben exploderar! Du överlever men skadas allvarligt.")
    bonus_mot_alvin = False
    labyrint()

def Anthin():
    print("\nDu möter Anthin – en vakt blockerar din väg!")
    om_vinst = stridssystem("Anthin", fiende_hp=30, fiende_skada=(4, 8))
    if om_vinst:
        lägg_till_föremål("stark attack-elixir")
        snabb_dörr_reflex()

def snabb_dörr_reflex():
    print("\nDu springer mot en dörr som håller på att stängas!")
    print("Tryck snabbt på 'E' för att hinna igenom innan dörren stängs.")
    print("Du har 3 sekunder på dig...")

    starttid = time.time()
    svar = input("TRYCK 'E' NU! ➤ ").strip().lower()
    slut_tid = time.time()

    tid_tagen = slut_tid - starttid

    if svar == "e" and tid_tagen <= 3:
        print("Du hann genom dörren precis i tid!")
        staty_rum()
    else:
        print("Du var för långsam eller tryckte fel! Dörren slog igen på dig.")
        print("Du tar skada innan du kommer in i en labyrint")
        staty_rum()

def staty_rum():
    print("\nDu går in i ett dunkelt rum med en mystisk staty i mitten.")
    print("En inskription lyder: 'Jag lyser på natten men försvinner på dagen. Vad är jag?'")
    svar = input("Skriv ditt svar: ").strip().lower()
    
    if "stjärna" or "stjärnor" or "stjärna" or "månen" or "måne" in svar:
        print("Rätt svar! Statyns mun öppnas och ett föremål faller ut.")
        lägg_till_föremål("guldnyckel")
        labyrint()
    else:
        print("Fel svar. Statyn rör sig hotfullt. Försök igen!")
        staty_rum()
        
def labyrint():
    print("\nDu hamnar i en mystisk labyrint som inte borde få plats i alvins lilla hus och måste välja rätt väg!")
    val = input("Välj riktning (vänster/höger/rakt fram): ").strip().lower()
    
    if val == "vänster":
        print("Du hittar en genväg ut!")
        Alvin()
    elif val == "höger":
        print("Du går vilse och hamnar tillbaka vid starten.")
        labyrint()
    elif val == "rakt fram":
        print("Du hittar en kista!")
        lägg_till_föremål("mystisk ring")
        Alvin()
    else:
        print("Ogiltigt val. Försök igen.")
        labyrint()


def Alvin(extra_skada=False):
    print("\nDu möter slutbossen: Alvin!")
    fiende_hp = 65
    if bonus_mot_alvin:
        fiende_hp -= 15
        print("Du har en fördel – Alvin har mindre HP tack vare bombframgång!")

    överlevde = stridssystem("Alvin", fiende_hp=fiende_hp, fiende_skada=(6, 12), extra_skada=extra_skada)
    
    if överlevde:
        avslut = random.choice(["frihet", "fångad_igen", "förbannelse"])
        if avslut == "frihet":
            print("\nDu har hittat vägen ut ur Alvins hus och räddat din värdighet. Du vann!")
        elif avslut == "fångad_igen":
            print("\nPrecis när du tror att du är fri, fångar Alvins hund Timmy dig och äter upp dig. Bättre lycka nästa gång...")
            start()
        elif avslut == "förbannelse":
            print("\nDu besegrar Alvin... men förbannelsen över huset fångar din själ. Du blir nästa fånge. Spelet slutar här.")
    else:
        print("\nAlvin besegrar dig... Du ser mörkret falla och ditt öde är beseglat. Du dog. Game over.")

# ==========================================================Stridsystemet=============================================================
def stridssystem(fiende_namn, fiende_hp, fiende_skada, extra_skada=False):
    spelar_hp = 40
    självläkningar_kvar = 3  # Ny variabel för max antal självläkningar

    if extra_skada:
        spelar_hp -= 15
        print("Du är skadad från tidigare hinder – du börjar med lägre HP!")

    while spelar_hp > 0 and fiende_hp > 0:
        print(f"\nDin HP: {spelar_hp} | {fiende_namn}s HP: {fiende_hp} | Självläkningar kvar: {självläkningar_kvar}")
        val = input("Vad vill du göra? (attack/special/läka/använd/ryggsäck): ").strip().lower()

        if val == "attack":
            skada = random.randint(5, 10)
            if karaktär_bonus.get("extra_skada"):
                skada += karaktär_bonus["extra_skada"]
            fiende_hp -= skada
            print(f"Du attackerar och gör {skada} skada mot {fiende_namn}.")
        elif val == "special":
            if random.random() < 0.5:
                skada = random.randint(12, 20)
                fiende_hp -= skada
                print(f"Specialattack lyckades! Du gör {skada} skada mot {fiende_namn}.")
            else:
                print("Specialattack misslyckades!")
        elif val == "läka":
            if självläkningar_kvar > 0:
                heal = random.randint(10, 18)
                if karaktär_bonus.get("extra_läkning"):
                    heal += karaktär_bonus["extra_läkning"]
                spelar_hp += heal
                självläkningar_kvar -= 1
                print(f"Du läker dig själv med {heal} HP. ({självläkningar_kvar} självläkningar kvar)")
            else:
                print("Du har inga självläkningar kvar!")
        elif val == "använd":
            effekt = använd_föremål()
            if effekt > 0:
                spelar_hp += effekt
            elif effekt < 0:
                skada = abs(effekt)
                fiende_hp -= skada
                print(f"Föremålseffekt: Du gör {skada} extra skada mot {fiende_namn}!")
        elif val == "ryggsäck":
            visa_ryggsäck()
            continue
        else:
            print("Ogiltigt val. Du tappar din tur!")

        if fiende_hp > 0:
            if karaktär_bonus.get("undvik_chans") and random.random() < karaktär_bonus["undvik_chans"]:
                print(f"{fiende_namn} försöker attackera dig, men du undviker slaget som en smidig tjuv!")
            else:
                skada_fra_fiende = random.randint(fiende_skada[0], fiende_skada[1])
                spelar_hp -= skada_fra_fiende
                print(f"{fiende_namn} attackerar dig och gör {skada_fra_fiende} skada!")

    if spelar_hp <= 0:
        print(f"\nDu förlorade striden mot {fiende_namn}...")
        if fiende_namn == "Alvin":
            return False
        else:
            print("Du vaknar tillbaka i cellen...")
            start()
            spara_spel()
            return True
    else:
        print(f"\nDu besegrade {fiende_namn}!")
        spara_spel()
        return True

# ===============================================================Starta programmet=============================================================

start()
