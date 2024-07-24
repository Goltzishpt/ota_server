import datetime


def log_device_info(devices):
    pass


def trigger_report(mac, fwv, action):
    print(
        f"Report Triggered: MAC={mac}, FW Version={fwv}, Action={action}, "
        f"Time={datetime.datetime.utcnow()}"
    )
