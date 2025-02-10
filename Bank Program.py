#Show Balance
#Deposit
#Withdraw

def show_balance(balance):
    print("***************************************")
    print(f"your balance is ${balance:.2f}")     #shows decimal ex..2f == $_.00
    print("***************************************")

def deposit():
    print("***************************************")
    amount = float(input("Enter an amount to be deposited: "))  #use float because we have use '"$" and "cents" numbers'' so use float key.
    print("***************************************")
    if amount<0:                         #we do not want any negative deposit so use this command
        print("***************************************")
        print("That is not a valid amount")
        print("***************************************")
        return 0
    else:
        return amount

def withdraw(balance):
    print("***************************************")
    amount = float(input("Enter your amount to be withdraw:  "))
    print("***************************************")

    if amount > balance:
        print("***************************************")
        print("Insufficient funds")
        print("***************************************")
        return 0                #do need to return somthing because we have use elif and else and as per logic the amt >bal
    elif amount <0:
        print("***************************************")
        print("Amount must be a greater than 0")
        print("***************************************")
        return 0
    else:
        return amount
        
def main():
  balance = 0
  is_running = True    #apply boolean keyword

  while is_running:
    print("***************************************")

    print("       Banking program      ")

    print("***************************************")

    print("       1.Show Balance       ")
    print("       2.Deposit            ")
    print("       3.Withdraw           ")
    print("       4.Exit               ")

    print("***************************************")

    choice = input("Enter your choice (1-4): ")

    if choice =='1':
         show_balance(balance)
    elif choice =='2':
        balance += deposit()
    elif choice =='3':
        balance -= withdraw(balance)
    elif choice =='4':
        is_running = False
    else:
        print("***************************************")
        print("That is not valid choice")
        print("***************************************")


  print("***************************************")
  print("Thank you have a nice day!")
  print("***************************************")

if __name__ == '__main__':
    main()

    

