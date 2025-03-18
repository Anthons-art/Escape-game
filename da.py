import random

def start():
    print("Välkommen till 'Fly från Alvin'. Ditt uppdrag är att hitta en väg ut ur hans hus innan han hittar dig.")
    print("Du är i en cell.")
    har_nyckel = input("Har du nyckeln? (ja/nej): ").strip().lower()

    if har_nyckel == "ja":
        ett_till_rum()
    else:
        print("Du måste hitta nyckeln först. Försök igen!")
        start()

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
    svar = input("Gåta: Vad är alltid framför dig men kan aldrig ses? ").strip().lower()
    
    if "framtiden" in svar:
        print("Rätt svar!")
        Alvin()
    else:
        print("Fel svar. Försök igen.")
        pussel()

def Anthin():
    print("\nDu möter Anthin – en vakt blockerar din väg!")
    stridssystem("Anthin", fiende_hp=30, fiende_skada=(4, 8))
    Alvin()

def Alvin():
    print("\nDu möter slutbossen: Alvin!")
    stridssystem("Alvin", fiende_hp=50, fiende_skada=(6, 12))
    print("\nDu har hittat vägen ut ur Alvins hus och räddat din värdighet. Du vann!")

def stridssystem(fiende_namn, fiende_hp, fiende_skada):
    spelar_hp = 40

    while spelar_hp > 0 and fiende_hp > 0:
        print(f"\nDin HP: {spelar_hp} | {fiende_namn}s HP: {fiende_hp}")
        val = input("Vad vill du göra? (attack/special/läka): ").strip().lower()

        if val == "attack":
            skada = random.randint(5, 10)
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
            heal = random.randint(8, 15)
            spelar_hp += heal
            print(f"Du läker dig själv med {heal} HP.")

        else:
            print("Ogiltigt val. Du tappar din tur!")

        if fiende_hp > 0:
            skada_fra_fiende = random.randint(fiende_skada[0], fiende_skada[1])
            spelar_hp -= skada_fra_fiende
            print(f"{fiende_namn} attackerar dig och gör {skada_fra_fiende} skada!")

    if spelar_hp <= 0:
        print("\nDu förlorade striden och vaknar tillbaka i cellen...")
        start()
    else:
        print(f"\nDu besegrade {fiende_namn}!")


start()