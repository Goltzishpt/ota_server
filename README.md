# OTA Server
This is a simple HTTP server for checking and downloading device firmware.

## Installation
- Clone the repository: 
``` Copy code
git clone https://github.com/Goltzishpt/ota_server
```

- Navigate to the project directory: 
``` bash Copy code
cd ota_server
```

## Usage
- Enter the command below into the terminal or run it by clicking on the arrows on the left.
``` bash Copy code
sudo ./run.sh run
```

- Check firmware version request:
``` bash Copy code
curl -X GET http://localhost:777/version.txt -H "cache-control: no-cache" -H "Connection: close" -H "br-mac: 00:11:22:33:44:55" -H "br-fwv: v1.0.0" 
```

- Download firmware binary request:
``` bash Copy code
curl -X GET http://localhost:777/firmware.bin -H "cache-control: no-cache" -H "Connection: close" -H "br-mac: 00:11:22:33:44:55" -H "br-fwv: v1.0.0"
```

## Test
- Enter the command below into the terminal or run it by clicking on the arrows on the left.
``` bash Copy code
sudo ./run.sh test
```