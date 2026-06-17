#!/usr/bin/env python3
"""Obtain a Reddit OAuth refresh token for the AutoMod sync workflows."""

from __future__ import annotations

import random
import socket
import sys
import os
from urllib.parse import parse_qs, urlparse

import praw

from reddit_auth import client_secret, required_env


DEFAULT_REDIRECT_URI = "http://localhost:8080"
DEFAULT_SCOPES = ("identity", "modconfig", "wikiedit", "wikiread")


def receive_redirect(redirect_uri: str) -> dict[str, str]:
    """Wait for Reddit to redirect back to localhost and return query parameters."""
    parsed = urlparse(redirect_uri)
    if parsed.hostname not in {"localhost", "127.0.0.1"} or not parsed.port:
        raise RuntimeError("REDDIT_REDIRECT_URI must point to localhost with an explicit port")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((parsed.hostname, parsed.port))
    server.listen(1)
    client, _address = server.accept()
    server.close()
    request = client.recv(4096).decode("utf-8", errors="replace")
    path = request.split(" ", 2)[1]
    query = parse_qs(urlparse(path).query)
    message = "Refresh token received. You can close this browser tab."
    client.send(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n{message}".encode())
    client.close()
    return {key: values[0] for key, values in query.items() if values}


def main() -> int:
    """Run the interactive refresh-token flow."""
    redirect_uri = os.environ.get("REDDIT_REDIRECT_URI", DEFAULT_REDIRECT_URI)
    reddit = praw.Reddit(
        client_id=required_env("REDDIT_CLIENT_ID"),
        client_secret=client_secret(),
        redirect_uri=redirect_uri,
        user_agent=required_env("REDDIT_USER_AGENT"),
    )
    state = str(random.randint(100000, 999999))
    scopes = [scope.strip() for scope in ",".join(DEFAULT_SCOPES).split(",") if scope.strip()]
    url = reddit.auth.url(duration="permanent", scopes=scopes, state=state)
    print("Open this URL while logged into the Reddit account that should own the token:")
    print(url)
    params = receive_redirect(redirect_uri)
    if params.get("state") != state:
        raise RuntimeError("OAuth state mismatch")
    if "error" in params:
        raise RuntimeError(f"Reddit authorization failed: {params['error']}")
    refresh_token = reddit.auth.authorize(params["code"])
    print("Set this repository Actions secret:")
    print(f"REDDIT_REFRESH_TOKEN={refresh_token}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
