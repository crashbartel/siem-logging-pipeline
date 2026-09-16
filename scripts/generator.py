#!/usr/bin/env python3
"""
Synthetic authentication event generator for SIEM pipeline testing.
Supports both normal and brute-force modes.

This script generates synthetic authentication events that can be used to test
SIEM pipeline capabilities, including normal authentication flows and brute-force
attack detection scenarios.
"""

import json
import random
import time
from datetime import datetime, timedelta
import uuid
from pathlib import Path
import argparse

def generate_auth_event(mode: str = "normal") -> dict:
    """Generate a synthetic authentication event.

    Args:
        mode: Either "normal" or "brute-force" to determine the type of event

    Returns:
        Dictionary containing an authentication event with all required fields
    """
    # Fictional usernames and IP addresses (RFC 5737)
    usernames = ['alice', 'bob', 'charlie', 'diana', 'eve', 'frank', 'grace', 'henry']
    ip_addresses = [
        '192.0.2.10',   # RFC 5737 documentation IP
        '192.0.2.11',
        '198.51.100.20', # RFC 5737 documentation IP
        '198.51.100.21',
        '203.0.113.30',  # RFC 5737 documentation IP
        '203.0.113.31'
    ]

    outcomes = ['success', 'failure']

    # Generate timestamp with slight variation for realistic time distribution
    timestamp = datetime.utcnow()

    # For brute-force mode, we want to create events within a 5-minute window for the same IP
    if mode == "brute-force":
        ip_address = random.choice(ip_addresses)
        username = random.choice(usernames)
        outcome = random.choice(outcomes)

        # Add scenario field for detection logic
        event = {
            "timestamp": timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "event_id": str(uuid.uuid4()),
            "username": username,
            "ip_address": ip_address,
            "outcome": outcome,
            "type": "authentication",
            "scenario": "brute-force" if mode == "brute-force" else "normal"
        }
    else:
        # Normal mode - generate a single normal event
        event = {
            "timestamp": timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "event_id": str(uuid.uuid4()),
            "username": random.choice(usernames),
            "ip_address": random.choice(ip_addresses),
            "outcome": random.choice(outcomes),
            "type": "authentication",
            "scenario": "normal"
        }

    return event

def generate_brute_force_scenario() -> list:
    """Generate a brute-force scenario with at least 10 failed attempts.

    Returns:
        List of authentication events representing a brute-force attack scenario
    """
    # Pick a single IP and username for this scenario
    ip_address = '192.0.2.10'  # RFC 5737 documentation IP
    usernames = ['alice', 'bob', 'charlie', 'diana', 'eve']
    username = random.choice(usernames)

    # Generate at least 10 failed attempts
    events = []

    # Create multiple failure events (at least 10)
    for i in range(15): # Generate more than 10 to ensure enough failures
        timestamp = (datetime.utcnow() - timedelta(minutes=random.randint(0, 4)))  # Within 5-minute window

        event = {
            "timestamp": timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "event_id": str(uuid.uuid4()),
            "username": username,
            "ip_address": ip_address,
            "outcome": "failure",
            "type": "authentication",
            "scenario": "brute-force"
        }
        events.append(event)

    # Add one success attempt (optional)
    if random.choice([True, False]):
        timestamp = datetime.utcnow()
        event = {
            "timestamp": timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "event_id": str(uuid.uuid4()),
            "username": username,
            "ip_address": ip_address,
            "outcome": "success",
            "type": "authentication",
            "scenario": "brute-force"
        }
        events.append(event)

    return events

def main() -> None:
    """Generate authentication events and write to stdout and log file.

    This is the entry point of the script that handles command-line arguments
    and orchestrates event generation based on the specified mode.
    """
    parser = argparse.ArgumentParser(description='Synthetic authentication event generator')
    parser.add_argument('--mode', choices=['normal', 'brute-force'], default='normal',
                       help='Generation mode: normal or brute-force')

    args = parser.parse_args()

    print(f"Starting synthetic authentication event generator in {args.mode} mode...")

    log_path = Path("/var/log/siem/auth.jsonl")
    log_path.parent.mkdir(parents=True, exist_ok=True)

    if args.mode == "brute-force":
        # Generate a complete brute-force scenario (at least 10 failures)
        events = generate_brute_force_scenario()

        for event in events:
            line = json.dumps(event)

            print(line, flush=True)

            with log_path.open("a", encoding="utf-8") as log_file:
                log_file.write(line + "\n")

            time.sleep(0.5)  # Add small delay between events
    else:
        # Normal mode (generate 5 events as before)
        for i in range(5):
            event = generate_auth_event("normal")
            line = json.dumps(event)

            print(line, flush=True)

            with log_path.open("a", encoding="utf-8") as log_file:
                log_file.write(line + "\n")

            time.sleep(1)

    print(f"Finished generating {args.mode} events.")


if __name__ == "__main__":
    main()