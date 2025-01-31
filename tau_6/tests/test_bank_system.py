import pytest
from unittest.mock import patch

from src.bank_system import (
    Bank,
    Account,
    InsufficientFundsError
)
import src.bank_system

@pytest.fixture
def bank_setup():

    bank = Bank()
    bank.create_account("123", "Alice", 1000.0)
    bank.create_account("456", "Bob", 500.0)
    return bank

@pytest.fixture
def single_account():

    return Account(account_number="111", owner="TestOwner", balance=100.0)


def test_account_deposit(single_account):
    single_account.deposit(50)
    assert single_account.balance == 150

def test_account_deposit_negative_value(single_account):
    with pytest.raises(ValueError):
        single_account.deposit(-100)

def test_account_withdraw_success(single_account):
    single_account.withdraw(30)
    assert single_account.balance == 70

def test_account_withdraw_insufficient_funds(single_account):
    with pytest.raises(InsufficientFundsError):
        single_account.withdraw(200)

@pytest.mark.asyncio
async def test_account_transfer_success(bank_setup):
    alice = bank_setup.get_account("123")  # saldo 1000
    bob = bank_setup.get_account("456")    # saldo 500

    await alice.transfer(bob, 200)
    assert alice.balance == 800
    assert bob.balance == 700

@pytest.mark.asyncio
async def test_account_transfer_insufficient_funds(bank_setup):
    alice = bank_setup.get_account("123")
    bob = bank_setup.get_account("456")

    with pytest.raises(InsufficientFundsError):
        await bob.transfer(alice, 1000)


def test_bank_create_account(bank_setup):
    new_acc = bank_setup.create_account("999", "Charlie", 300)
    assert new_acc.balance == 300
    assert new_acc.owner == "Charlie"
    assert bank_setup.get_account("999") is new_acc

def test_bank_create_account_already_exists(bank_setup):
    with pytest.raises(ValueError):
        bank_setup.create_account("123", "Someone", 50)

def test_bank_get_account_valid(bank_setup):
    account = bank_setup.get_account("123")
    assert account.owner == "Alice"

def test_bank_get_account_invalid(bank_setup):
    with pytest.raises(ValueError):
        bank_setup.get_account("9999")

@pytest.mark.asyncio
async def test_bank_process_transaction(bank_setup):
    alice = bank_setup.get_account("123")
    bob = bank_setup.get_account("456")

    async def sample_transaction():
        await alice.transfer(bob, 100)
        return "OK"

    result = await bank_setup.process_transaction(sample_transaction)
    assert result == "OK"
    assert alice.balance == 900
    assert bob.balance == 600


@pytest.mark.asyncio
async def test_transfer_exception(bank_setup):
    alice = bank_setup.get_account("123")
    bob = bank_setup.get_account("456")

    with pytest.raises(InsufficientFundsError):
        await alice.transfer(bob, 999999)


@pytest.mark.asyncio
@patch("src.bank_system.external_auth_service", return_value=True)
async def test_transfer_with_mocked_auth_service(mock_auth, bank_setup):
    alice = bank_setup.get_account("123")
    bob = bank_setup.get_account("456")

    is_authorized = src.bank_system.external_auth_service(alice.account_number, 200)

    mock_auth.assert_called_once_with("123", 200)

    if is_authorized:
        await alice.transfer(bob, 200)

    assert alice.balance == 800
    assert bob.balance == 700


@pytest.mark.parametrize("deposit_amount, expected_balance", [
    (100, 200.0),
    (0, 100.0),
    (50.5, 150.5),
])
def test_account_deposit_parametrized(single_account, deposit_amount, expected_balance):
    single_account.deposit(deposit_amount)
    assert single_account.balance == pytest.approx(expected_balance)