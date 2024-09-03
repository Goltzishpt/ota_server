import os
from flask import request, send_file, abort
from datetime import datetime

from app import app
from app.utils import logger, trigger_report, is_valid_mac
from app.config import FW_VERSION, FW_DIR


devices = {}


@app.route('/version.txt', methods=['GET'])
def version():
    logger.info("All headers received for version.txt request:")
    for header, value in request.headers.items():
        logger.info(f"{header}: {value}")

    mac = request.headers.get('br-mac')
    fwv = request.headers.get('br-fwv')

    logger.info(f"br-mac: {mac}")
    logger.info(f"br-fwv: {fwv}")

    if not any((mac, fwv)):
        abort(400, "Missing headers")

    if not is_valid_mac(mac):
        abort(400, "Invalid MAC address")

    devices[mac] = devices.get(mac, {'FW Version': None})
    devices[mac]['Last Seen Time'] = datetime.utcnow()

    try:
        if devices[mac]['FW Version'] != fwv:
            devices[mac]['FW Version'] = fwv
            trigger_report(mac, fwv, "Checked")
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        abort(500, "Internal server error")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        abort(500, "Internal server error")

    try:
        return send_file(os.path.join(app.root_path, FW_DIR, FW_VERSION, 'version.txt'))
    except FileNotFoundError as e:
        logger.error(f"FileNotFoundError: {e}")
        abort(404, "File not found")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        abort(500, "Internal server error")


@app.route('/firmware.bin', methods=['GET'])
def firmware():
    logger.info("All headers received for firmware.bin request:")
    for header, value in request.headers.items():
        logger.info(f"{header}: {value}")

    mac = request.headers.get('br-mac')
    fwv = request.headers.get('br-fwv')

    logger.info(f"br-mac: {mac}")
    logger.info(f"br-fwv: {fwv}")

    if not any((mac, fwv)):
        abort(400, "Missing headers")

    if not is_valid_mac(mac):
        abort(400, "Invalid MAC address")

    if mac not in devices:
        devices[mac] = {'FW Version': fwv}

    devices[mac]['Update Time'] = datetime.utcnow()
    devices[mac]['FW Version'] = fwv

    try:
        trigger_report(mac, fwv, "Updated")
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        abort(500, "Internal server error")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        abort(500, "Internal server error")

    try:
        return send_file(os.path.join(app.root_path, FW_DIR, FW_VERSION, 'firmware.bin'))
    except FileNotFoundError as e:
        logger.error(f"FileNotFoundError: {e}")
        abort(404, "File not found")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        abort(500, "Internal server error")