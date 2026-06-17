#!/usr/bin/env python3
"""Shared Reddit authentication helpers for AutoMod sync scripts."""

from __future__ import annotations

import os

import praw


DEFAULT_USER_AGENT = "automod-sync/1.0 by u/ripred"


def required_env(name: str) -> str:
    """Return a required environment variable."""
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def client_secret() -> str:
    """Return the standard or legacy Reddit client secret value."""
    value = os.environ.get("REDDIT_CLIENT_SECRET", "").strip()
    if value:
        return value
    legacy_value = os.environ.get("REDDIT_SECRET", "").strip()
    if legacy_value:
        return legacy_value
    raise RuntimeError("Missing REDDIT_CLIENT_SECRET or legacy REDDIT_SECRET")


def reddit_client() -> praw.Reddit:
    """Create a Reddit API client using refresh-token auth when available."""
    options = {
        "client_id": required_env("REDDIT_CLIENT_ID"),
        "client_secret": client_secret(),
        "user_agent": os.environ.get("REDDIT_USER_AGENT", "").strip() or DEFAULT_USER_AGENT,
    }
    refresh_token = os.environ.get("REDDIT_REFRESH_TOKEN", "").strip()
    if refresh_token:
        options["refresh_token"] = refresh_token
        return praw.Reddit(**options)

    username = os.environ.get("REDDIT_USERNAME", "").strip()
    password = os.environ.get("REDDIT_PASSWORD", "").strip()
    if not username or not password:
        raise RuntimeError(
            "Set REDDIT_REFRESH_TOKEN, or set both REDDIT_USERNAME and REDDIT_PASSWORD "
            "for legacy script-app authentication."
        )
    options["username"] = username
    options["password"] = password
    return praw.Reddit(**options)


def configured_subreddit_name() -> str:
    """Return the configured subreddit name."""
    return required_env("SUBREDDIT_NAME")
