import os
from flask import request, send_file, abort
from datetime import datetime

from app import app
from app.utils import log_device_info, trigger_report

devices = {}


@app.route('/version.txt', methods=['GET'])
def version():
    print("All headers received for version.txt request:")
    for header, value in request.headers.items():
        print(f"{header}: {value}")

    mac = request.headers.get('br-mac')
    fwv = request.headers.get('br-fwv')

    print(f"br-mac: {mac}")
    print(f"br-fwv: {fwv}")

    if not mac or not fwv:
        abort(400, "Missing headers")

    devices[mac] = devices.get(mac, {'FW Version': None})
    devices[mac]['Last Seen Time'] = datetime.utcnow()

    if devices[mac]['FW Version'] != fwv:
        devices[mac]['FW Version'] = fwv
        trigger_report(mac, fwv, "Checked")

    print(
        f"Device {mac} checked version at {devices[mac]['Last Seen Time']}. "
        f"Current FW Version: {fwv}"
    )

    return send_file(os.path.join(app.root_path, 'version.txt'))


@app.route('/firmware.bin', methods=['GET'])
def firmware():
    print("All headers received for firmware.bin request:")
    for header, value in request.headers.items():
        print(f"{header}: {value}")

    mac = request.headers.get('br-mac')
    fwv = request.headers.get('br-fwv')

    print(f"br-mac: {mac}")
    print(f"br-fwv: {fwv}")

    if not mac or not fwv:
        abort(400, "Missing headers")

    if mac not in devices:
        devices[mac] = {'FW Version': fwv}

    devices[mac]['Update Time'] = datetime.utcnow()
    devices[mac]['FW Version'] = fwv
    trigger_report(mac, fwv, "Updated")

    # Логирование данных устройства
    print(
        f"Device {mac} updated firmware at {devices[mac]['Update Time']}. "
        f"New FW Version: {fwv}"
    )

    return send_file(os.path.join(app.root_path, 'firmware/firmware.bin'))
