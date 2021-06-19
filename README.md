<h1 align="center">Teleflood - Telegram Flood Bot<br />
  <a href="https://www.codacy.com/gh/D3rise/teleflood/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=D3rise/teleflood&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/06ca1988cf6141a9b586629bde7e1c99"/></a><br />
  <img src="assets/teleflood_logo.png" width="36%"></img><br />
  <h3 align="center">Telegram bot for flooding to DMs/chats with multiple accounts and proxy support</h3>
</h1>

![Usage](assets/usage.gif)

# ⚠ Achtung

**This bot is used in purposes that are prehibited by Telegram terms of usage.  
Using this may result in banning your account(s) without ability to recover it.**

## Contents

**1.** [Setting up](#setting-up)

- [What do you need](#what-do-you-need)
- [How to setup this bot](#how-to-setup-this-bot)

**2.** [Usage](#usage)

- [How to start this bot](#how-to-start-this-bot)
- [How to setup proxy](#how-to-setup-proxy)

## Setting up
### What do you need

**1.** Your Telegram credentials:

- Phone number
- Password (if you have 2FA)

**2.** API ID and API Hash (you can get it from [here](https://core.telegram.org/api/obtaining_api_id#obtaining-api-id))

### How to setup this bot

**1.** Download this repository (using `git clone` or just click the big green button at the top of this page)  
**2.** Install [Python](https://www.python.org/downloads/) (you may need to restart your computer if you're using Windows)  
**3.** Open directory with bot using `cmd` (on Windows) or terminal (on Mac OS and Linux) and type the following command: `python -m pip install -r requirements.txt`  
**3.** Create file with name `accounts.txt`  
**4.** Put your account credentials in it using following format:

- `phone:password:api_id:api_hash`
- `api_id` and `api_hash` is the lines you received in [What do you need](#what-do-you-need) second paragraph
- Example: `+19005553535:keyboardcat:133721:aiwjerlasidhoaw12312dlnawhiawd`
- You can find more advanced example with multiple accounts in `accounts.example.txt`

**5.** Rename file `config.example.txt` to `config.txt` and configure it using following info:

- `MESSAGE` is the message that will be sent while flooding
- `MESSAGE_COUNT` is the count of messages in total that will be sent to victim (if using multiple accounts, the messages will be split between each account)
- `VICTIM_ID` is the username/tag (not actual id unless you already flooded this victim) of user/chat you want to flood

#### After this, you are ready to go!

## Usage

### How to start this bot

**1.** Open directory with bot using `cmd` (on Windows) or terminal (on Mac OS and Linux)  
**2.** Type the following command: `python src/main.py`

- For more advanced users: if you want to get info about CLI, simply use the command `python src/main.py --help`

### How to setup proxy

**1.** Open your config file  
**2.** Fill it with new values as described here:

```python
# This is your proxy type.
# Can be MTPROTO, SOCKS5, SOCKS4 or HTTP
# Example:
PROXY_TYPE=SOCKS5

# The IP address or DNS name of the proxy server
# Example:
PROXY_ADDR=1.1.1.1

# The port of proxy server, defaults to 1070 for
# SOCKS, 8080 for HTTP and 443 for MTPROTO
# Example:
PROXY_PORT=2002

# This modifies DNS resolving behavior. If set
# to yes, DNS resolving will be performed on
# proxy server. If set to no, DNS resolving
# will be performing locally
# Example:
PROXY_RDNS=yes

# For SOCKS5 servers, this allows simple
# username/password auth with ther server.
# For SOCKS4 servers, this parameter will be
# sent as userid. This parameter will be ignored
# if using HTTP or MTPROTO proxy
# Example:
PROXY_USERNAME=admin

# This parameter is only valid for SOCKS5 and
# MTPROTO servers and specifies the respective
# password for username (on SOCKS5 servers)
# provided.
# IMPORTANT: For MTPROTO this parameter is alias for secret
# Example:
PROXY_PASSWORD=wajdosdpwaiwpojaiwdj
```

**3.** Start bot as usual ([How-to](#how-to-start-this-bot))
