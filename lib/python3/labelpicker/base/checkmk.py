#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# SPDX-FileCopyrightText: © 2023 PL Automation Monitoring GmbH <pl@automation-monitoring.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# This file is part of the Checkmk Labelpicker project (https://labelpicker.mk)


import requests
import json
import os


class CMKInstance:
    """Interact with checkmk instance"""

    def _get_automation_secret(username="automation"):
        """Get automation secret for the given user.
        Default user is automation"""

        omd_root = os.environ["OMD_ROOT"]

        # If automationsecret file for user exists, read credentials from there
        secret_file = f"{omd_root}/var/check_mk/web/{username}/automation.secret"
        if os.path.exists(secret_file):
            secret = open(secret_file).read().strip()
            return secret
        else:
            return False

    def __init__(self, url=None, username="automation", password=None):
        """Initialize a REST-API instance. URL, User and Secret can be automatically taken from local site if running as site user.

        Args:
            site_url: the site URL
            api_user: username of automation user account
            api_secret: automation secret

        Returns:
            instance of Checkmk REST-API
        """
        if not url:
            # site_url = _site_url()
            api_version = "1.0"
            # use local site_url from $HOME/etc/apache/conf.d/listen-port.conf
            omd_root = os.environ["OMD_ROOT"]
            omd_site = os.environ["OMD_SITE"]
            f = open(f"{omd_root}/etc/apache/listen-port.conf", "r").readlines()
            for line in f:
                if line.startswith("Listen"):
                    cmk_local_apache = line.split(" ")[1].strip()
            site_url = f"http://{cmk_local_apache}/{omd_site}"

            self._api_url = f"{site_url}/check_mk/api/{api_version}"
        else:
            self._api_url = url

        if not password:
            secret = self._get_automation_secret(username)
        else:
            secret = password

        self.headers = {
            "Content-Type": "application/json",
        }

        self._session = requests.session()
        self._session.headers["Authorization"] = f"Bearer {username} {secret}"
        self._session.headers["Accept"] = "application/json"

    def _trans_resp(self, resp):
        try:
            data = resp.json()
        except json.decoder.JSONDecodeError:
            data = resp.text
            print(f"JSONDecodeError for data: {data}")
        return data, resp

    def _request_url(self, method, endpoint, data={}, etag=None):
        headers = self.headers
        if etag is not None:
            headers["If-Match"] = etag

        url = f"{self._api_url}/{endpoint}"
        request_func = getattr(self._session, method.lower())

        return self._trans_resp(
            request_func(
                url,
                json=data,
                headers=headers,
                allow_redirects=False,
            )
        )

    def _get_url(self, endpoint, data={}):
        return self._request_url("GET", endpoint, data)

    def _put_url(self, endpoint, etag, data={}):
        return self._request_url("PUT", endpoint, data, etag)

    def _post_url(self, endpoint, data={}, etag=None):
        return self._request_url("POST", endpoint, data, etag)

    def activate(self, sites=[], force=False):
        """Activates pending changes

        Args:
            sites: On which sites the configuration shall be activated.
            An empty list means all sites which have pending changes.

        """
        post_data = {"redirect": False, "sites": sites, "force_foreign_changes": force}

        data, resp = self._post_url(
            "domain-types/activation_run/actions/activate-changes/invoke",
            etag="*",
            data=post_data,
            etag="*",
        )
        if resp.status_code == 200:
            return data
        else:
            resp.raise_for_status()

    def get_all_hosts(self, effective_attr=False, attributes=True):
        """Gets all hosts from the CheckMK configuration.

        Args:
            effective_attr: Show all effective attributes, which affect this host, not just the attributes which were set on this host specifically. This includes all attributes of all of this host's parent folders.
            attributes: If False do not fetch hosts' data

        Returns:
            hosts: Dictionary of host data or dict of hostname -> URL depending on attributes parameter
        """
        data, resp = self._get_url(
            "domain-types/host_config/collections/all",
            data={"effective_attributes": "true" if effective_attr else "false"},
        )
        if resp.status_code != 200:
            resp.raise_for_status()
        hosts = {}
        for host_info_dict in data.get("value", []):
            try:
                id = host_info_dict["id"]
                hosts[id] = host_info_dict["extensions"]
            except KeyError:
                pass
        return hosts

    def get_host(self, hostname):
        """Get current host configuration

        Args:
            hostname: cmk hostname

        Return:
            data: {host_config}
        """
        data, resp = self._get_url(
            f"objects/host_config/{hostname}", data={"effective_attributes": "false"}
        )
        if resp.status_code == 200:
            return data
        resp.raise_for_status()

    # Etag identifies the current state of the object in checkmk
    def get_etag(self, hostname):
        """Get current etag value for host"""
        data, resp = self._get_url(
            f"objects/host_config/{hostname}", data={"effective_attributes": "false"}
        )
        if resp.status_code == 200:
            return resp.headers["etag"]
        resp.raise_for_status()

    def edit_host(
        self, hostname, etag=None, set_attr={}, update_attr={}, unset_attr=[]
    ):
        """Edit a host in the CheckMK configuration.

        Args:
            hostname: name of the host
            etag: (optional) etag value, if not provided the host will be
            looked up first using get_host().

            update_attr: Just update the hosts attributes with these
            attributes. The previously set attributes will not be touched.

        Returns:
            (data, etag)
            data: host's data
            etag: current etag value
        """

        if set_attr:
            data = {"attributes": set_attr}
        elif update_attr:
            data = {"update_attributes": update_attr}
        elif unset_attr:
            data = {"remove_attributes": unset_attr}

        if not etag:
            etag = self.get_etag(hostname)
        data, resp = self._put_url(
            f"objects/host_config/{hostname}",
            etag,
            data=data,
        )
        if resp.status_code == 200:
            return data, etag
        resp.raise_for_status()

    def host_exists(self, hostname):
        """Check if host exists"""
        host = self.get_host(hostname)
        return host

    def get_labels(self, hostname, object="host"):
        """Get currently defined labels of a host or service object from checkmk"""
        if object == "host":
            host = self.get_host(hostname)
            labels = host["extensions"]["attributes"].get("labels", {})
        elif object == "service":
            # maybe implemented in future
            pass
        return labels

    def set_host_labels(self, hostname, labels):
        """Set host labels on checkmk"""
        self.edit_host(hostname, update_attr={"labels": labels})

    def update_labels(
        self, orig_labels, labels, label_prefix="hwsw/", enforce_cleanup=False
    ) -> dict:
        """Compare current / original labels
        with new labels and update if necessary"""

        updated_labels = orig_labels.copy()
        # {'hwsw/os_vendor': 'Ubuntu', 'hwsw/os_version': '20.04', 'test': 'xy'}
        # Cleanup: remove all labels with known prefix from original labels
        for label in orig_labels:
            if enforce_cleanup:
                if label.lower().startswith(label_prefix.lower()):
                    del updated_labels[label]
            else:
                if label.startswith(label_prefix):
                    del updated_labels[label]

        # Update dict with new labels
        updated_labels.update(labels)
        return updated_labels
