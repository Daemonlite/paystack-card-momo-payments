from decouple import config
import requests
import logging

logger = logging.getLogger(__name__)

class CardPayment: 
    def initiate_charge(self, amount, email, card_number, card_expiry, card_cvc):
        endpoint = "https://api.paystack.co/charge"
        secret_key = config("PAYSTACK_KEY")
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "amount": int(amount) * 100, 
            "email": email,
            "currency": "GHS",
            "payment_method": "card",
            "card": {
                "number": card_number,
                "expiry": card_expiry,
                "cvc": card_cvc,
            },
        }

        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return {"status": False, "message": str(e)}

        return response.json()

    def verify_transaction(self, reference):
        endpoint = f"https://api.paystack.co/transaction/verify/{reference}"
        secret_key = config("PAYSTACK_KEY")
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return {"status": False, "message": str(e)}

        data = response.json()
        return {"status": True, "data": data.get("data", {})}

    def refund_transaction(self, reference, amount):
        endpoint = "https://api.paystack.co/refund"
        secret_key = config("PAYSTACK_KEY")
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "transaction": reference,
            "amount": int(amount) * 100,
        }

        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return {"status": False, "message": str(e)}

        return response.json()

    def get_transaction_details(self, reference):
        endpoint = f"https://api.paystack.co/transaction/{reference}"
        secret_key = config("PAYSTACK_KEY")
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return {"status": False, "message": str(e)}

        return response.json()
