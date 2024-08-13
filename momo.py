import json
import requests
from decouple import config
import logging
logger = logging.getLogger(__name__)


class MomoPayment:
    def __init__(self,phone_number,email,name) -> None:
        self.phone_number = phone_number
        self.email = email
        self.name = name


    def check_network(self, phone_number=None):
        # Use self.phone_number if phone_number is not provided
        number_to_check = phone_number if phone_number is not None else self.phone_number

        # Ensure the phone number is a string and its length is 10
        if not isinstance(number_to_check, str) or len(number_to_check) != 10:
            return "Invalid phone number"

        # Determine the network based on the prefix
        prefix = number_to_check[:3]
        if prefix in ["020", "050"]:
            network = "VOD"
        elif prefix in ["027", "057", "026", "056"]:
            network = "ATL"
        elif prefix in ["059", "024", "054"]:
            network = "MTN"
        else:
            network = "Unknown network"

        print(network)
        return network



    def send_mobile_money_prompt(self,amount):
        endpoint = "https://api.paystack.co/charge"
        secret_key = config("PAYSTACK_KEY")
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }

        print(headers)

        network = self.check_network(self.phone_number)
        logger.warning(network)
        # Prepare request payload
        payload = {
            "amount": int(amount) * 100,
            "email": self.email,
            "currency": "GHS",
            "mobile_money": {"phone": self.phone_number, "provider": network},
        }

        response = requests.post(endpoint, json=payload, headers=headers)
        return response.json()


    def verify_transaction(self,reference):
        endpoint = f"https://api.paystack.co/transaction/verify/{reference}"
        secret_key = config("PAYSTACK_KEY")
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }

        response = requests.get(endpoint, headers=headers)
        ret = response.json()

        return ret["data"]["status"]



    def verify_momo_otp(self,otp, reference):
        endpoint = f"https://api.paystack.co/charge/submit_otp"
        secret_key = config("PAYSTACK_KEY")
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }
        params = {"otp": otp, "reference": reference}

        params_json = json.dumps(params)

        response = requests.post(endpoint, data=params_json, headers=headers)

        res = response.json()
        if res['status'] == False:
            print(res)
            return res['message']
        return res["data"]["status"]


    """
    in order for this to work a reference should be created for the 
    particular user before sending the money
    """


    def create_mobile_money_recipient(self,name, account_number):
        endpoint = "https://api.paystack.co/transferrecipient"
        secret_key = config("PAYSTACK_KEY")
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }

        bank_code = self.check_network(account_number)

        # Prepare request payload
        payload = {
            "type": "mobile_money",
            "name": name,
            "account_number": account_number,
            "bank_code": bank_code,
            "currency": "GHS",
        }

        response = requests.post(endpoint, json=payload, headers=headers)
        return response.json()


    def transfer_funds(self,amount,phone_number,name):
        endpoint = "https://api.paystack.co/transfer"
        secret_key = config("PAYSTACK_KEY")
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }
        print(amount)
        recipient_code = self.create_mobile_money_recipient(name, phone_number)
        # Prepare request payload
        payload = {
            "source": "balance",
            "amount": amount * 100,
            "reference": config("PAYSTACK_REFERENCE"),
            "recipient": recipient_code["data"]["recipient_code"],
            "reason": "test",
            "currency": "GHS",
        }
        print(f'recipient code : {recipient_code["data"]["recipient_code"]}')

        response = requests.post(endpoint, json=payload, headers=headers)
        return response.json()
    

    def check_account_balance(self):
        endpoint = "https://api.paystack.co/balance"
        secret_key = config("PAYSTACK_KEY")
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }

        response = requests.get(endpoint, headers=headers)
        return response.json()

    def fetch_transaction_statements(self, start_date=None, end_date=None, per_page=50, page=1):
        endpoint = "https://api.paystack.co/transaction"
        secret_key = config("PAYSTACK_KEY")
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "per_page": per_page,
            "page": page,
        }

        response = requests.get(endpoint, headers=headers, params=params)
        return response.json()


