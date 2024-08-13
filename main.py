from datetime import datetime
import json
from momo import MomoPayment
from mailer import send_email

momo = MomoPayment(
    phone_number='0209414099',
    email='test@mail.com',
    name='daemonlite'
)

if __name__ == "__main__":
    while True:
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Paystack Mobile Money And Card Payments")
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Created by Daemonlite")

        print('----------------------------------------------------------------')
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Select Preferred Payment Option")
        print('----------------------------------------------------------------')
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - [1] Mobile Money")
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - [2] Debit/Credit Card")
        print('----------------------------------------------------------------')
        selection = str(input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Select an option to continue,type exit() to exit: "))

        if selection == 'exit()':
            break

        if selection == '1':
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - [1] Transfer Funds")
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - [2] Deposit Funds")
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - [3] Check Balance")
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - [4] Print Statement")

            option = str(input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Select an option to continue: "))
            
            if option == '1':
                print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - [] ")
                name = str(input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Enter Recipient Name : "))
                phone = str(input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Enter Recipient Phone Number : "))
                amount = str(input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Enter amount to transfer : "))
                tr = momo.transfer_funds(amount=amount,phone_number=phone,name=name)

                print(tr["message"])
            
            elif option == '2':
                amount = str(input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Enter amount to Deposit : "))
                tr = momo.send_mobile_money_prompt(amount)
                print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - \n {tr['data']['message']}")

            elif option == '3':
                tr = momo.check_account_balance()
                print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Your balance is {tr['data'][0]['balance']}")
                

            elif option == '4':
                start_date = input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Enter Start Date:  ")
                end_date = input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Enter End Date:  ")

                tr = momo.fetch_transaction_statements(start_date, end_date)
                
                # Ensure that the data is in the correct format for JSON serialization
                transaction_data = tr['data']
                
                # Write the JSON data to a file
                with open('statement.json', 'w') as f:
                    json.dump(transaction_data, f, indent=4)  # Using indent for pretty-printing
                
                send_email()
                
                print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - statement has been sent through mail")
                    
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Invalid Option")

        elif selection == '2':
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - [1] Transfer Funds")
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - [2] Deposit Funds")
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - [3] Request Refund")
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - [4] Print Statement")
            
            option = str(input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Select an option to continue: "))

            if option == '1':
                pass


            elif option == '2':
                pass


            elif option == '3':
                pass
                


            elif option == '4':
                start_date = input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Enter Start Date (YYYY-MM-DD):  ")
                end_date = input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Enter End Date (YYYY-MM-DD):  ")

                try:
                    tr = momo.fetch_transaction_statements(start_date, end_date)
                    transaction_data = tr['data']
                    
                    # Filter transactions to include only those with channel 'card'
                    card_transactions = [transaction for transaction in transaction_data if transaction.get('channel') == 'card']
                    
                    # Write the filtered JSON data to a file
                    with open('statement.json', 'w') as f:
                        json.dump(card_transactions, f, indent=4)  # Pretty-printing
                    
                    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Card transactions have been successfully written to 'statement.json'")
                
                except KeyError as e:
                    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Error: Missing expected key in transaction data - {e}")
                
                except Exception as e:
                    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - An unexpected error occurred: {e}")
        else:
            print()
            print()
            print('----------------------------------------------------------------')
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Invalid Option")

            print('----------------------------------------------------------------')

            print()
            print()

 
















