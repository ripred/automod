
---

# AutoMod Version Control Template for Reddit Communities

[![License](https://flat.badgen.net/github/license/ripred/automod)](https://github.com/ripred/automod/blob/main/LICENSE)
[![Stars](https://flat.badgen.net/github/stars/ripred/automod)](https://github.com/ripred/automod/stargazers)
[![Forks](https://flat.badgen.net/github/forks/ripred/automod)](https://github.com/ripred/automod/network/members)

This repository provides a template for managing and syncing Reddit AutoMod configurations using GitHub workflows and Python scripts.

## Overview

This template allows automatic syncing of AutoMod configurations between GitHub and Reddit. It includes workflows and scripts to:

- **Automatically update AutoMod on Reddit** when changes are pushed to the repository.
- **Fetch the current AutoMod configuration** from Reddit and update the repository.

## Repository Structure

- **`automod/automoderator.yml`**: Main AutoModerator configuration file in YAML format.
- **`update_automod.py`**: Python script that updates the AutoMod configuration on Reddit.
- **`fetch_automod.py`**: Python script that fetches the current AutoMod configuration from Reddit and updates the repository.
- **`.github/workflows/update-automod.yml`**: GitHub Actions workflow that updates the AutoMod configuration on Reddit when changes are made to the repository.
- **`.github/workflows/fetch-automod.yml`**: GitHub Actions workflow that fetches the current AutoMod configuration from Reddit.

## Workflows

### AutoMod Update Workflow

This workflow automatically pushes changes to Reddit whenever a commit is made to `automod/automoderator.yml`.

**Trigger**: On push to the `automod/automoderator.yml` file.

### Fetch AutoMod Configuration Workflow

This manual workflow fetches the current AutoMod configuration from Reddit and updates the repository.

**Trigger**: Manual trigger via GitHub Actions.

## How to Use

### Updating AutoMod Configuration

1. Edit `automod/automoderator.yml` to modify the AutoMod configuration.
2. Push the changes to the `main` branch. The update will automatically be pushed to Reddit via the `update-automod.yml` workflow.

### Fetching Current AutoMod Configuration

1. Trigger the "Fetch AutoMod Configuration" workflow manually from the GitHub Actions tab.
2. The workflow will fetch the current configuration from Reddit, update the repository, and push the changes.

## Environment Setup

Ensure the following secrets are set up in your GitHub repository under **Settings > Secrets and variables > Actions**:

- `REDDIT_CLIENT_ID` 
- `REDDIT_CLIENT_SECRET`
- `REDDIT_REFRESH_TOKEN`
- `REDDIT_USER_AGENT`
- `SUBREDDIT_NAME` 

These secrets are used by the Python scripts to interact with Reddit’s API. `REDDIT_REFRESH_TOKEN` is preferred so GitHub Actions does not need to store a Reddit account password.

For compatibility with older deployments, the scripts still accept `REDDIT_SECRET` instead of `REDDIT_CLIENT_SECRET`, and `REDDIT_USERNAME` plus `REDDIT_PASSWORD` instead of `REDDIT_REFRESH_TOKEN`.

To generate a refresh token, create a Reddit web application with redirect URI `http://localhost:8080`, export `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, and `REDDIT_USER_AGENT` locally, then run:

```bash
python obtain_reddit_refresh_token.py
```

Store the printed value as the `REDDIT_REFRESH_TOKEN` Actions secret.

---

In this setup, the **AutoMod Update Workflow** triggers automatically when there are changes to the `automod/automoderator.yml` file. When you push changes to this file, the `update-automod.yml` workflow will take care of syncing the configuration with Reddit. 

For fetching the current configuration from Reddit, you can trigger the **Fetch AutoMod Configuration Workflow** manually through GitHub Actions if your repo loses sync with your subreddit automod code.
