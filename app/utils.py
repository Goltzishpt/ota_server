import re
import logging
from datetime import datetime


import gspread
from oauth2client.service_account import ServiceAccountCredentials

def setup_logger() -> logging.Logger:
    logger = logging.getLogger('OTA Server')
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False

    return logger

logger = setup_logger()

def get_google_sheets_client():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    return client


def send_data_to_sheet(sheet_name, data):
    try:
        client = get_google_sheets_client()
        sheet = client.open(sheet_name).sheet1

        row = [data.get('mac'), data.get('fwv'), data.get('status'), data.get('timestamp')]
        sheet.append_row(row)
    except gspread.SpreadsheetNotFound:
        logger.info(f"Table with name '{sheet_name}' not found. Please check the name and sharing settings.")
    except Exception as e:
        logger.info(f"An error occurred: {e}")


def trigger_report(mac, fwv, status):
    data = {
        'mac': mac,
        'fwv': fwv,
        'status': status,
        'timestamp': datetime.utcnow().isoformat()
    }
    send_data_to_sheet('otaserver', data)


def is_valid_mac(mac):
    return bool(re.match(r'^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$', mac))
