# AWS Security Group Rules Updater
Update AWS EC2 security group rules with your public IP address.
Run as a cron job (for example every minute) and when an IP address change is detected the rules specified in `rules.yml` will be updated with your new IP.

## Requirements
* Python 3 (not tested on Python 2)
* Python modules in `requirements.txt`
* AWS CLI configured with your AWS profiles

## Usage
Clone the repository:
```
git clone https://github.com/shugyosha89/aws-sg-updater.git
```

Copy `.env.example` to `.env` and change `SGR_DESCRIPTION` to the description you want to set for updated rules.
Optionally change the log file location.

Copy `rules.yml.example` to `rules.yml` and fill it with the AWS profiles, security group IDS, security group rule IDs and ports of the rules you want to update.

Set up a cron job to run `update.py` at regular intervals.
Example: Add the below to `crontab -e` to run every minute:
```
* * * * * python3 /path/to/aws-sg-updater/update.py
```

## Troubleshooting
To force an IP update, change the contents of `ip.txt`.
