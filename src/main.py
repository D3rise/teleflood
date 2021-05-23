#!/usr/bin/env python
import argparse
import asyncio
import time
import sys
import secrets
from threading import Timer
from functools import partial
from tqdm import tqdm
from dotenv import dotenv_values
from telethon.sync import TelegramClient
from telethon import types, errors

parser = argparse.ArgumentParser(description="Teleflood - Telegram Flood Bot")
parser.add_argument('--config-file', type=str, default="config.txt",
                    help="file with config for the bot in format described on https://github.com/D3rise/teleflood/INSTRUCTIONS.md")
parser.add_argument('--accounts-file', type=str, default="accounts.txt",
                    help="file with credentials for accounts to flood from")
parser.add_argument('--message-count', type=int,
                    help="count of messages to send")
parser.add_argument('--victim-id', type=str,
                    help="a user id to whom the messages will be sent, can be a phone number, username but not actual ID (if you have not yet flooded this victim)")
parser.add_argument('--message', type=str,
                    help="a message that will be sent to victim")

# Parse args and read the config file to log bot in with
args = parser.parse_args()
config = dotenv_values(args.config_file)
loop = asyncio.get_event_loop()
clients = []
waiting_clients = []
waiting_clients_timers = []

message = args.message or config["MESSAGE"]
message_count = args.message_count or int(config["MESSAGE_COUNT"])
victim_id = args.victim_id or config["VICTIM_ID"]
accounts_file_path = args.accounts_file or config["ACCOUNTS_FILE"]


async def start_flood(victim):
    global waiting_clients_timers, waiting_clients, clients, message, message_count

    # Removes client from waiting clients list and adds it to working clients list
    def remove_client_from_waiting_clients(client):
        global waiting_clients_timers
        waiting_clients.remove(client)
        waiting_clients_timers = list(filter(
            lambda timer: timer["client"] == client, waiting_clients_timers))
        clients.append(client)

    # Gets timer from waiting clients timers
    # list with minimum time of required waiting and returns it
    def get_timer_with_min_wait_time():
        return min(waiting_clients_timers, key=lambda timer: timer["seconds"])

    # An actual flood process, tqdm is for progressbar
    for _ in tqdm(range(message_count), desc="Flooding", unit="messages"):
        # Choose client randomly from working clients list
        client = secrets.choice(clients)

        try:
            await client.send_message(victim, message)
        except errors.FloodWaitError as error:
            # If telegram sends us a flood waiting error,
            # we will remove client from working clients and
            # add it to waiting clients until a required number
            # of seconds will pass
            clients.remove(client)
            waiting_clients.append(client)

            timer = Timer(error.seconds, partial(
                remove_client_from_waiting_clients, client))
            waiting_clients_timers.append(
                {"client": client, "timer": timer, "seconds": error.seconds})

            timer.start()

            # If there's no other client to flood from, we
            # will stop the loop until we can get working client
            if len(clients) == 0:
                timer_with_min_time = get_timer_with_min_wait_time()
                time.sleep(timer_with_min_time["seconds"])


async def main():
    # Read and log into all accounts from accounts file
    with open(accounts_file_path, 'r') as accounts_file:
        # Reading file line-by-line to prevent memory troubles
        account = accounts_file.readline()
        line_number = 1

        def go_to_next_line():
            nonlocal line_number, account
            # Go to next line in file
            line_number += 1
            account = accounts_file.readline()

        while account:
            # If line (account) starts with an # (or the
            # line is empty), which means that this line
            # is an comment, we will skip it
            if account.startswith("#") or account == '':
                go_to_next_line()

            # Account credentials need to be in format "phone:password:api_id:api_hash"
            credentials = account.split(':')

            # If the line is empty and it wasn't skipped,
            # which means that file is over, we will stop
            # reading it.
            if credentials == ['']:
                break

            phone_number = credentials[0]
            password = credentials[1]
            api_id = credentials[2]
            api_hash = credentials[3]

            # A subfunction that will request an auth code for number that bot currently logging into
            def code_callback():
                return input(f"Enter the code for {phone_number}: ")

            # Using phone_number[1:] to prevent saving "+" in phone number too
            client = TelegramClient(
                f"client_{phone_number[1:]}",
                api_id,
                api_hash)

            await client.start(
                phone_number,
                password,
                code_callback=code_callback)

            # Add client to working clients list
            clients.append(client)

            go_to_next_line()

        if len(clients) == 0:
            print(
                f"Error: there isn't any account credentials in {accounts_file_path}!")
            exit(1)

    # Get victim account using victim_id
    victim = await clients[0].get_entity(victim_id)

    # If victim is actually a user or a chat
    if isinstance(victim, types.User) or isinstance(victim, types.Chat):
        flood_prompt = input(
            f"Found account/chat with id {victim.id}. Start flooding with {message_count} messages? Y/n: ").lower()
        if flood_prompt == "" or flood_prompt == "y":
            await start_flood(victim)
            print(
                f"Sent {message_count} messages with content \"{message}\" to account/chat with id {victim.id}")
        else:
            print("Aborted.")

# Start event loop and main function in it
loop.run_until_complete(main())
