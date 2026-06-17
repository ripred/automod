#!/usr/bin/env python3
"""Push the repository AutoModerator configuration to Reddit."""

from __future__ import annotations

import os
from pathlib import Path

from reddit_auth import configured_subreddit_name, reddit_client


def update_automod_config() -> None:
    """Update Reddit AutoModerator wiki content from this repository."""
    reddit = reddit_client()
    subreddit = reddit.subreddit(configured_subreddit_name())
    automod_config = Path("automod/automoderator.yml").read_text(encoding="utf-8")

    committer = os.environ.get("GITHUB_ACTOR", "local")
    commit_id = os.environ.get("GITHUB_SHA", "unknown")
    commit_reason = f"Changes by {committer} on {commit_id}"

    subreddit.wiki["config/automoderator"].edit(automod_config, reason=commit_reason)


if __name__ == "__main__":
    update_automod_config()
