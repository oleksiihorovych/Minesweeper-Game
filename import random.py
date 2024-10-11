import random

person = random.randint(1, 2)
position = random.randint(1, 6)

tmp = -1
personSet = {"Ilya", "Lesha"}
print(random.choice(list(personSet)))
print()

while tmp != position:
    tmp = int(input("Enter a number: "))

print("LOSER")
