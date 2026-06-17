#!/usr/bin/env python3
"""Fetch the live Reddit AutoModerator configuration into this repository."""

from __future__ import annotations

from pathlib import Path

from reddit_auth import configured_subreddit_name, reddit_client


def fetch_automod_config() -> None:
    """Fetch AutoModerator wiki content from Reddit."""
    reddit = reddit_client()
    subreddit = reddit.subreddit(configured_subreddit_name())
    automod_config = subreddit.wiki["config/automoderator"].content_md
    Path("automod/automoderator.yml").write_text(automod_config, encoding="utf-8")


if __name__ == "__main__":
    fetch_automod_config()
