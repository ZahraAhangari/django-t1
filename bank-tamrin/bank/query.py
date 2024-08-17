from user.models import User
from account.models import Account

import logging

from django.db.models import Max
from django.db import transaction
from django.db.models import F

import random
import string
from faker import Faker



#ایجاد 20000 کوئری یا 1000000 کوئری

fake = Faker()

#num_accounts=1000000 / num_accounts=20000
def random_accounts(num_accounts=20000):
    accounts = []
    for _ in range(num_accounts):
        user = User.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            code_melli=''.join(random.choices(string.digits, k=10))
        )
        account = Account(
            owner=user,
            account_number=''.join(random.choices(string.digits, k=24)),
            balance=random.randint(1000, 1000000000)
        )
        accounts.append(account)

    Account.objects.bulk_create(accounts)
    return True




# لیست نام صاحب هر حساب و موجودی آن حساب

def get_account_owners_and_balances():

    logging.basicConfig(filename='logs/get_account_owners_and_balances.log', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info("Started get_account_owners_and_balances")

    accounts = Account.objects.all().select_related('owner')
    for account in accounts:
        logger.info(f" Account owner: {account.owner.first_name} {account.owner.last_name}, Balance: {account.balance}")

    logger.info("Finished get_account_owners_and_balances")
    return True




# حسابی که بیشترین موجودی را دارد

def max_balance():

    logging.basicConfig(filename='logs/max_balance.log', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info("Started max_balance")

    max_balance = Account.objects.annotate(max_balance=Max('balance')).order_by('-max_balance').first()
    logger.info(f" account with max balance: Owner: {max_balance.account_number}, Balance: {max_balance.balance}")

    logger.info("Finished max_balance")
    return True




#5 حسابی که کمترین موجودی را دارند

def min_balance(count=5):

    logging.basicConfig(filename='logs/min_balance.log', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info("Started min_balance")

    data = Account.objects.annotate(max_balance=Max('balance')).order_by('balance')[:count]
    for account in data:
        logger.info(f"Account: Owner: {account.account_number}, Balance: {account.balance: .2f}")

    logger.info("Finished min_balance")
    return True




#انتقال مقدار مشخصی پول از حسابی به حساب دیگر

def transfer_money(from_acc, to_acc, amount):

    logging.basicConfig(filename='logs/transfer_money.log', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info("Started transfer_money")


    with transaction.atomic():

        try:
            # تعریف دو شی از کلاس Account
            from_account = Account.objects.get(account_number=from_acc)
            to_account = Account.objects.get(account_number=to_acc)

        except Account.DoesNotExist:
            logger.error(f"an account with number {from_acc} or {to_acc} was not found")
            return False

        if from_account.balance < amount:
            logger.error(f"account balance {from_acc} is not enough")
            return False

        from_account.balance -= amount
        from_account.save()

        to_account.balance += amount
        to_account.save()


        logger.info(f"Transferred {amount} from {from_account.account_number} to {to_account.account_number}")
        logger.info("Finished transfer_money")
        return True




# لیست حساب هایی که شناسه ی حساب از موجودی آن بیشتر است
def find_account_number():

    logging.basicConfig(filename='logs/find_account_number.log', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info("Started find_account_number")

    accounts = Account.objects.filter(account_number__gt=F('balance')).values('account_number', 'balance')

    for account in accounts:
        logger.info(f"Account number: {account['account_number']}, Balance: {account['balance']}")

    logger.info("Finished find_account_number")
    return True




# لیست حساب هایی که کدملی صاحب حساب از موجودی آن بیشتر است
def find_code_melli():

    logging.basicConfig(filename='logs/find_code_melli.log', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info("Started find_code_melli")

    accounts = Account.objects.filter(account_number__gt=F('balance')).select_related('owner')

    for account in accounts:
        logger.info(f"code_melli: {account.owner.code_melli}, Balance: {account.balance}")

    logger.info("Finished find_code_melli")
    return True




if __name__ == "__main__":

    random_accounts()

    get_account_owners_and_balances()
    max_balance()
    min_balance()

    transfer_money()
    #transfer_money('1234567890', '9876543210', 1000)

    find_account_number()
    find_code_melli()
