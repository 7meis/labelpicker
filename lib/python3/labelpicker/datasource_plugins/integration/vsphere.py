#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2023 PL Automation Monitoring GmbH <pl@automation-monitoring.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# This file is part of the Checkmk Labelpicker project (https://labelpicker.mk)

"""Integation Class of vSphere module."""

# Thanks to:
# Abraxas Informatik AG: This Datasource Plugin was developed in cooperation with the "Abraxas Informatik AG".
import requests
import json

# from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class VSphereAPI:
    """vSphere Connection."""
    def __init__(self, api_url, api_user, api_pass, verify_ssl=True):
        """Initialize a VSphereAPI Object.

        Args:
            api_url: the api url of vSphere to connect.
            api_user: the user for the login to the api. Need read permissions.
            api_pass: api password for the login.
            verify_ssl: Enable or disable SSL verification.

        Returns:
            None
        """
        self.api_url = api_url
        self.api_user = api_user
        self.api_pass = api_pass
        self.verify_ssl = verify_ssl
        # Disable SSL warnings if verify = false
        if not verify_ssl:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self.sid = self.auth_vcenter()

    def auth_vcenter(self) -> str:
        """Authenticate against vCenter."""
        url = f"{self.api_url}/com/vmware/cis/session"
        resp = requests.post(
            url, auth=(self.api_user, self.api_pass), verify=self.verify_ssl
        )
        if resp.status_code != 200:
            self.print_error(resp, "API authentication failed")
            return None
        return resp.json().get("value")

    def make_request(self, method, url, headers=None, data=None):
        """Generic request function."""
        resp = requests.request(
            method, url, headers=headers, data=data, verify=self.verify_ssl
        )
        if resp.status_code != 200:
            self.print_error(resp, "API request failed")
            return None
        return resp

    def print_error(self, response, message):
        """Generic error printing function."""
        print(f"Error! {message}: {response.status_code}")
        print(f"Error! API responded with Message: {response.text}")

    def get_api_data(self, req_url):
        """Generic funktion to get api data."""
        headers = {"vmware-api-session-id": self.sid}
        resp = self.make_request("GET", req_url, headers=headers)
        return resp.json() if resp else None

    def post_api_data(self, req_url, req_data):
        """Generic funktion to post api data."""
        headers = {
            "vmware-api-session-id": self.sid,
            "content-type": "application/json",
        }
        data = json.dumps(req_data)
        resp = self.make_request("POST", req_url, headers=headers, data=data)
        return resp.json() if resp else None

    def get_all_vms(self):
        """Get all virtual machines."""
        resp = self.get_api_data(f"{self.api_url}/vcenter/vm")
        return resp.get("value") if resp else None

    def get_vm_tags(self, vm_id):
        """Get all tags from virtual machines."""
        url = f"{self.api_url}/com/vmware/cis/tagging/tag-association?~action=list-attached-tags"
        req_data = {"object_id": {"type": "VirtualMachine", "id": vm_id}}
        resp = self.post_api_data(url, req_data)
        return resp if resp else None

    def get_tag_category(self, cat_id):
        """Get all tag categories."""
        url = f"{self.api_url}/com/vmware/cis/tagging/category/id:{cat_id}"
        resp = self.get_api_data(url)
        return resp if resp else None

    def get_vsphere_tag(self, tag_id):
        """Get all vSphere tags."""
        url = f"{self.api_url}/com/vmware/cis/tagging/tag/id:{tag_id}"
        resp = self.get_api_data(url)
        return resp if resp else None
