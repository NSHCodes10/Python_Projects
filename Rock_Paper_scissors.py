import random

user_wins = 0
computer_wins = 0

options = ["rock","paper","scissors"]
#            0       1        3
# options [0]...This is index. If we wanna only index 0, index 1, index 2 then

while True:
    user_input = input("Type Rock/Paper/scissors or Q to quit: ").lower()
    if user_input == "q":
      break
    
    if user_input not in options:
        continue

    random_number = random.randint(0, 2)
    # rock == 0, paper == 1, scissors == 2

    computer_pick = options[random_number]
    print("computer picked", computer_pick + ".")

    if user_input == "rock" and computer_pick == "scissors":
       print("you won!")
       user_wins += 1
       

    elif user_input == "paper" and computer_pick == "rock":
       print("you won!")
       user_wins += 1
       

    elif user_input == "scissors" and computer_pick == "paper":
       print("you won!")
       user_wins += 1

    else:
       print("You lost!")
       computer_wins += 1
    
print("You won", user_wins, "times.")
print("The computer won", computer_wins, "times.")
print("Goodbye!")




