#!/usr/bin/env python3
"""
Script to update AWS security groups with one's current public IP address.
"""

__author__ = "Matthew Bowen"
__version__ = "0.1.0"
__license__ = "MIT"

from boto3 import Session
from dotenv import load_dotenv
import logzero
from logzero import logger
import requests
import os
import pathlib
import yaml

SCRIPT_DIR = pathlib.Path(__file__).parent.absolute()

def configure_logging():
    if log_file := os.environ.get('LOG_FILE'):
        logzero.logfile(log_file)

def update(ip):
    with open('rules.yml', 'r') as file:
        rules = yaml.safe_load(file)
    for profile, regions in rules.items():
        for region, groups in regions.items():
            session = Session(profile_name=profile, region_name=region)
            client = session.client('ec2')
            for sg_id, sg_rules in groups.items():
                rules = [
                    {
                        'SecurityGroupRuleId': rule_id,
                        'SecurityGroupRule': {
                            'IpProtocol': rule['protocol'],
                            'FromPort': rule['port'],
                            'ToPort': rule['port'],
                            'CidrIpv4': f'{ip}/32',
                            'Description': os.environ.get('DESCRIPTION', ''),
                        }
                    }
                    for rule_id, rule in sg_rules.items()
                ]
                try:
                    client.modify_security_group_rules(GroupId=sg_id, SecurityGroupRules=rules)
                except Exception as e:
                    logger.error(f'Failed to update SG {sg_id} on {profile}: {e}')

def main():
    ip = requests.get(os.environ.get('IP_SERVER')).text.strip()
    with open(f'{SCRIPT_DIR}/ip.txt', 'r') as f:
        old_ip = f.read().strip()

    if ip == old_ip:
        logger.info('No change')
        exit(0)

    logger.info(f'IP changed from {old_ip} to {ip}')
    with open(f'{SCRIPT_DIR}/ip.txt', 'w') as f:
        f.write(ip)

    update(ip)
    logger.info('Done')

if __name__ == "__main__":
    load_dotenv()
    configure_logging()
    main()
