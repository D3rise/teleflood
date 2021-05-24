import argparse


def get_parser_with_arguments():
    """Returns argparse.ArgumentParser with added arguments for it."""

    parser = argparse.ArgumentParser(
        description="Teleflood - Telegram Flood Bot")

    parser.add_argument('--config-file', type=str, default="config.txt",
                        help="file with config for the bot in format "
                        "described on https://github.com/D3rise/teleflood/README.md.")

    parser.add_argument('--accounts-file', type=str,
                        help="file with credentials for accounts to flood from. "
                        "Config file key name: ACCOUNTS_FILE")

    parser.add_argument('--message-count', type=int,
                        help="count of messages to send. "
                        "Config file key name: MESSAGE_COUNT")

    parser.add_argument('--victim-id', type=str,
                        help="a user id to whom the messages will be sent, can "
                        "be a phone number, username but not actual ID (if you "
                        "have not yet flooded this victim). "
                        "Config file key name: VICTIM_ID")

    parser.add_argument('--message', type=str,
                        help="a message that will be sent to victim. "
                        "Config file key name: MESSAGE")

    # Proxy CLI config values
    parser.add_argument('--proxy-type', type=str,
                        help="type of proxy to be used by client. "
                        "Config file key name: PROXY_TYPE")

    parser.add_argument('--proxy-addr', type=str,
                        help="the IP address or DNS name of the proxy server. "
                        "Config file key name: PROXY_ADDR")

    parser.add_argument('--proxy-port', type=int,
                        help="the port of proxy server, defaults to 1080 for "
                        "SOCKS, 8080 for HTTP and 443 for MTPROTO. "
                        "Config file key name: PROXY_PORT")

    parser.add_argument('--proxy-rdns', type=bool,
                        help="modifies DNS resolving behavior. If set to yes, "
                        "DNS resolving will be performed remotely, on the server. "
                        "If it is set to no, DNS resolving will be performed locally. "
                        "Config file key name: PROXY_RDNS")

    parser.add_argument('--proxy-username', type=str,
                        help="for SOCKS5 servers, this allows simple username/password "
                        "auth with the server. For SOCKS4 servers, this parameter will "
                        "be sent as userid. This parameter will be ignored if using HTTP and MTPROTO proxy. "
                        "Config file key name: PROXY_USERNAME")

    parser.add_argument('--proxy-password', type=str,
                        help="this parameter is only valid for SOCKS5 and MTPROTO servers "
                        "and specifies the respective password for username (for SOCKS5 "
                        "servers) provided. "
                        "Config file key name: PROXY_PASSWORD")

    return parser
