import asyncio
from typing import Dict


class InsufficientFundsError(Exception):
    pass

def external_auth_service(account_number: str, amount: float) -> bool:
    return True

class Account:

    def __init__(self, account_number: str, owner: str, balance: float = 0.0):
        self.account_number = account_number
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float):

        if amount < 0:
            raise ValueError("Kwota depozytu nie może być ujemna.")
        self.balance += amount

    def withdraw(self, amount: float):

        if amount > self.balance:
            raise InsufficientFundsError("Niewystarczające środki na koncie.")
        self.balance -= amount

    async def transfer(self, to_account: "Account", amount: float):

        await asyncio.sleep(0.01)

        if amount > self.balance:
            raise InsufficientFundsError("Niewystarczające środki na koncie do przelewu.")

        self.balance -= amount
        to_account.deposit(amount)


class Bank:

    def __init__(self):
        self.accounts: Dict[str, Account] = {}

    def create_account(self, account_number: str, owner: str, initial_balance: float = 0.0):

        if account_number in self.accounts:
            raise ValueError(f"Konto o numerze {account_number} już istnieje.")
        account = Account(account_number, owner, initial_balance)
        self.accounts[account_number] = account
        return account

    def get_account(self, account_number: str):

        if account_number not in self.accounts:
            raise ValueError(f"Konto o numerze {account_number} nie istnieje.")
        return self.accounts[account_number]

    async def process_transaction(self, transaction_func):

        await asyncio.sleep(0.01)
        return await transaction_func()
