#!/usr/bin/env python
import asyncio
import time
import secrets
import config
from threading import Timer
from functools import partial
from tqdm import tqdm
from telethon.sync import TelegramClient
from telethon import types, errors, connection

# Lists for working clients, waiting clients and timers for them
clients = []
waiting_clients = []
waiting_clients_timers = []


async def start_flood(victim):
    """
    Starts the flood process.

    ----------
    Parameters:
        victim (telethon.types.User|telethon.types.Chat): A victim (user/chat) entity to flood

    """
    global waiting_clients_timers, waiting_clients, clients

    def remove_client_from_waiting_clients(client):
        """
        Removes client from waiting clients list 
        and adds it to working clients list
        """
        global waiting_clients_timers

        waiting_clients.remove(client)
        waiting_clients_timers = list(filter(
            lambda timer: timer["client"] != client, waiting_clients_timers))

        clients.append(client)

    def get_timer_with_min_wait_time():
        """
        Gets timer from waiting clients timers list with
        minimum time of required waiting and returns it
        """
        return min(waiting_clients_timers, key=lambda timer: timer["seconds"])

    # An actual flood process, tqdm is for progressbar
    for _ in tqdm(range(config.message_count), desc="Flooding", unit="messages"):
        # Choose client randomly from working clients list
        client = secrets.choice(clients)

        try:
            await client.send_message(victim, config.message)
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
    with open(config.accounts_file_path, 'r') as accounts_file:
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
            session_id = f"client_{phone_number[1:]}"

            # If proxy isn't None and it equals to MTPROTO, we
            # will config client to work with MTPROTO proxy,
            # and if it's not MTPROTO, we will config client to
            # work with PySocks (HTTP, SOCKS4 or SOCKS5) proxy
            if config.proxy_type != None:

                # If proxy type is MTPROTO
                if config.proxy_type == "MTPROTO":
                    proxy = (config.proxy_addr, config.proxy_port,
                             config.proxy_password)

                    client = TelegramClient(
                        session_id,
                        api_id,
                        api_hash,
                        connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
                        proxy=proxy)

                # If proxy type is HTTP, SOCKS4 or SOCKS5
                else:
                    proxy = {
                        "proxy_type": config.proxy_type,
                        "addr": config.proxy_addr,
                        "port": config.proxy_port,
                        "rdns": config.proxy_rdns,
                        "username": config.proxy_username,
                        "password": config.proxy_password
                    }

                    client = TelegramClient(
                        session_id,
                        api_id,
                        api_hash,
                        proxy=proxy)
            else:
                # If proxy isn't enabled, we will init
                # standart client instance
                client = TelegramClient(
                    session_id,
                    api_id,
                    api_hash)

            # Starts client (create session and
            # request auth code if required)
            await client.start(
                phone_number,
                password,
                code_callback=code_callback)

            # Add client to working clients list
            clients.append(client)

            # This client is ready, so we will go to next line
            go_to_next_line()

        # If all accounts are not ready to use
        # or there's no accounts in accounts file
        if len(clients) == 0:
            print(
                f"Fatal: there isn't any valid account credentials in {config.accounts_file_path}!")
            exit(1)

    # Get victim account using victim_id
    victim = await clients[0].get_entity(config.victim_id)

    # If victim is actually a user or a chat
    if isinstance(victim, types.User) or isinstance(victim, types.Chat):
        flood_prompt = input(
            f"Found account/chat with id {victim.id}. Start flooding with {config.message_count} messages? Y/n: ").lower()

        # Y (yes) is default value, so if user
        # inputs an empty string, we will
        # use start flooding. If it's not,
        # we will abort the operation
        if flood_prompt == "" or flood_prompt == "y":
            await start_flood(victim)
            print(
                f"Sent {config.message_count} messages with content \"{config.message}\" to account/chat with id {victim.id}")
        else:
            print("Aborted.")

# Start event loop and await main function in it
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
