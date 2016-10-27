# miele-notifier
Small python program to send Pushbullet notifications when Miele laundry machines are done.
It polls the laundry website every 60 seconds and checks if the machine is in use, if not a Pushbullet note is sent

## Installation & configuration
1. Clone the repo `git clone https://github.com/torrottum/miele-notifier`
1. Create an [access token/API key for Pushbullet](https://www.pushbullet.com/#settings/account)
1. Configure settings
```
cd miele-notifier
cp config.example.json config.json
vim config.json
```
1. Install the requirements
```
pip3 install -r requirements.txt
```

## Usage

### List available machines:
```
$ ./miele-notifier.py list

  ID  Type    In use
----  ------  --------
  13  Washer  No
   4  Dryer   No
   7  Washer  No
   6  Dryer   No
   9  Washer  No
   1  Washer  No
   3  Washer  No
   5  Washer  No
  14  Dryer   Yes
  12  Dryer   No
  11  Washer  No
   8  Dryer   No
  10  Dryer   No
```

### Watch machine 14 and 1

```
$ ./miele-notifier.py 14 1
Checking machines ...
Dryer 14 is in use
Washer 1 is in use
Waiting 60s before next check ...
Dryer 14 is in use
Washer 1 not in use, sending notification
Waiting 60s before next check ...
```
