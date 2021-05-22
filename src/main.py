#!/usr/bin/env python
import argparse
import asyncio
from tqdm import tqdm
from dotenv import dotenv_values
from telethon.sync import TelegramClient
from telethon import types

parser = argparse.ArgumentParser(description="Teleflood - Telegram Flood Bot")
parser.add_argument('--config-file', type=str, default="config.txt",
                    required=False, help="file with config for the bot in format described on https://github.com/D3rise/teleflood/INSTRUCTIONS.md")
parser.add_argument('--message-count', type=int, default=1000,
                    required=False, help="count of messages to send")
parser.add_argument('--victim-id', type=str, required=True,
                    help="a user id to whom the messages will be sent, can be a phone number, username but not actual ID (if you have not yet flooded this victim)")
parser.add_argument('--message', type=str,
                    required=True, help="a message that will be sent to victim")

# Parse args and read the credentials file to log bot in with
args = parser.parse_args()
credentials = dotenv_values(args.credentials_file)
loop = asyncio.get_event_loop()
client = TelegramClient(
    'teleflood', credentials["API_ID"], credentials["API_HASH"])


async def main():
    # TODO: add multiple flood account support
    await client.start(credentials["PHONE_NUMBER"], credentials["PASSWORD"])
    victim = await client.get_entity(args.victim_id)

    # A subfunction that actually sends flood messages to a victim
    async def start_flood(message_count: int):
        for i in tqdm(range(message_count), desc="Flooding", unit="messages"):
            await client.send_message(victim, args.message)

    if isinstance(victim, types.User):
        flood_prompt = input(
            f"Found account with username {victim.username} and id {victim.id}. Start flooding with {args.message_count} messages? Y/n: ").lower()
        if flood_prompt == "" or flood_prompt == "y":
            await start_flood(args.message_count)
            print(
                f"Sent {args.message_count} messages with content \"{args.message}\" to user/bot with username {victim.username}")
        else:
            print("Aborted.")

loop.run_until_complete(main())
