l=[]
n = 0
nb = 0
with open("res/fr-pastrié.txt", 'r') as f:
    for i in f:
        n+=1
        a = i.rstrip()
        l.append(a)

print(n,"mots à traiter...")

words = []

for word in l:
        good = True
        if len(word)<9 and len(word)>4: # garder les mots entre 5 et 8 charactères
            for letter in word:
                if letter not in "abcdefghijklmnopqrstuvwxyz": # garder uniquement les charactères classiques (ie. pas de àéèç...)
                    good = False
            if good and word not in words:
                words.append(word)
                nb+=1

with open("res/fr.txt", 'w') as f:
    for wrd in words:
        f.write(wrd+"\n")

print("Terminé,",nb,"mots traités !")