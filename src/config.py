import cli
from dotenv import dotenv_values

parser = cli.get_parser_with_arguments()

# Parse args and read the config file
args = parser.parse_args()
config = dotenv_values(args.config_file)

# Create aliases for config values,
# CLI args have higher priority
message = args.message or config.get("MESSAGE")
message_count = args.message_count or int(config.get("MESSAGE_COUNT"))
victim_id = args.victim_id or config.get("VICTIM_ID")
accounts_file_path = args.accounts_file or config.get(
    "ACCOUNTS_FILE") or "accounts.txt"

# Create aliases for proxy config values and
# check if they are valid (proxy_type can only be
# MTPROXY, HTTP, SOCKS4 or SOCKS5, read https://docs.telethon.dev/en/latest/basic/signing-in.html#signing-in-behind-a-proxy)
available_proxy_types = ["MTPROTO", "SOCKS5", "SOCKS4", "HTTP"]
proxy_type = args.proxy_type or config.get("PROXY_TYPE")

# If proxy type is not None, we will
# uppercase it to prevent code duplication
if proxy_type != None:
    proxy_type = proxy_type.upper()

proxy_addr = args.proxy_addr or config.get("PROXY_ADDR")
proxy_port = args.proxy_port or int(config.get("PROXY_PORT") or 0)
proxy_rdns = args.proxy_rdns or config.get("PROXY_RDNS")
proxy_username = args.proxy_username or config.get("PROXY_USERNAME")
proxy_password = args.proxy_password or config.get("PROXY_PASSWORD")

# Check if proxy type is present and it's
# valid (equal to one of available proxy types)
if proxy_type != None and available_proxy_types.count(proxy_type) == 0:
    print(
        f"Fatal: PROXY_TYPE must be one of: {', '.join(available_proxy_types)}")
    exit(1)

# If we use MTPROTO proxy and user doesn't
# provide port for it, we will use default port
if proxy_port == None and proxy_type == "MTPROTO":
    proxy_port = 443
