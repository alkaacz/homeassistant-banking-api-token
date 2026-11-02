from datetime import timedelta

DOMAIN = "banking_api_token"
CONF_BANK = "bank"
CONF_ACCOUNT_ID = "account_id"
CONF_READ_TOKEN = "read_token"
CONF_PAY_TOKEN = "pay_token"
DEFAULT_SCAN_INTERVAL = 300
SCAN_INTERVAL = timedelta(seconds=DEFAULT_SCAN_INTERVAL)
BANK_CREDITAS = "creditas"
BANK_FIO = "fio"
PLATFORMS = ["sensor"]
