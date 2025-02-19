#!/bin/env python3
"""
MLflow user credentials setup utility

This program initializes your mlflow configuration and can update your password.
"""
#
# ---------------------------------------------------------------
# Copyright (C) 2004-2025, DWD, MPI-M, DKRZ, KIT, ETH, MeteoSwiss
# Contact information: icon-model.org
#
# Author: Marek Jacob (DWD)
#
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------

import configparser
from getpass import getpass
import os
import sys
import pathlib

from mlflow.server import get_app_client

# Configure you ml flow server
tracking_uri = "http://mlflow.dwd.de:5000/"
tracking_uri = "http://localhost:5000/"


def setup_config(config_file):
    """
    """
    print(f"{config_file} does not exist...")
    print("    ... create a new one")

    config_file.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    user = input(f"Please enter your mlflow username for server {tracking_uri}:\n")
    password = getpass(f"Please enter your mlflow (initial) password:\n")

    # create empty file
    open(config_file, "w").close()

    # set permissions to user read/write only
    config_file.chmod(0o600)

    with open(config_file, "a") as f:
        f.write("[mlflow]\n")
        f.write(f"mlflow_tracking_username = {user}\n")
        f.write(f"mlflow_tracking_password = {password}\n")

    try:
        print(f"    ... testing user {user}")
        test_connection(user)
    except Exception as e:
        print(e)
        print("Wrong username or password.")
        os.remove(config_file)
        print(f"    ... deleting {config_file}")
        sys.exit(1)


def test_connection(user):
    auth_client = get_app_client("basic-auth", tracking_uri=tracking_uri)
    auth_client.get_user(user)

def change_password(user, parser, config_file):
    password = getpass(f"Please enter a new password for mlflow on {tracking_uri}:\n")
    password2 = getpass(f"Please repeat that password:\n")
    if password != password2:
        print("Error passwords mismatch.")
        sys.exit(1)

    auth_client = get_app_client("basic-auth", tracking_uri=tracking_uri)
    auth_client.update_user_password(user, password)
    parser.set("mlflow", "mlflow_tracking_password", password)

    with open(config_file, 'w') as configfile:
        parser.write(configfile)
    print(f"    ... password updated in {config_file}")

    user = parser.get("mlflow", "mlflow_tracking_username")
    try:
        test_connection(user)
    except Exception:
        raise
    else:
        print(f"    ... an successfully tested on {tracking_uri}")


def main():
    config_file = pathlib.Path.home() / ".mlflow" / "credentials"

    if not config_file.exists():
        setup_config(config_file)

    # set permissions to user read/write only
    config_file.chmod(0o600)

    parser = configparser.ConfigParser()
    assert parser.read(config_file)
    user = parser.get("mlflow", "mlflow_tracking_username")

    print(f"    ... testing user {user}")
    try:
        test_connection(user)
    except Exception as e:
        print(f"Error while trying to access user {user}")
        print(e)
        sys.exit(1)

    change_password(user, parser, config_file)

if __name__ == '__main__':
    main()
