#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2023 PL Automation Monitoring GmbH <pl@automation-monitoring.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# This file is part of the Checkmk Labelpicker project (https://labelpicker.mk)

"""Implementation of vSphere strategy."""

# Thanks to:
# Abraxas Informatik AG: This Datasource Plugin was developed in cooperation with the "Abraxas Informatik AG".

from labelpicker.misc.abstract_strategy import Strategy
from integration.vsphere import VSphereAPI


class LPDSvSphere(Strategy):
    """vSphere strategy."""

    def source_algorithm(self, **kwargs) -> dict:
        """Return dict of source data."""
        verify_ssl = kwargs.get("verify_ssl", True)
        api_url = kwargs.get("api_url", None)
        api_user = kwargs.get("api_user", None)
        api_pass = kwargs.get("api_pass", None)
        # Authenticate on vCenter
        vsphere_api = VSphereAPI(api_url, api_user, api_pass, verify_ssl)

        vm_cache = {}
        tag_cache = {}

        for vm in vsphere_api.get_all_vms():
            vm_cache[vm["name"]] = {}
            vm_tags = vsphere_api.get_vm_tags(vm["vm"])
            for vm_tag in vm_tags["value"]:
                if vm_tag not in tag_cache:
                    tag = vsphere_api.get_vsphere_tag(vm_tag)
                    tag_value = tag["value"]["name"]
                    category = vsphere_api.get_tag_category(tag["value"]["category_id"])
                    tag_cache[vm_tag] = (category["value"]["name"], tag_value)
                tag_id, tag_val = tag_cache[vm_tag]
                vm_cache[vm["name"]].update({tag_id: tag_val})

        return vm_cache

    def process_algorithm(self, source, **kwargs) -> dict:
        """Process source data and return dict."""
        collected_labels = {}
        label_prefix = kwargs.get("label_prefix", None)
        for host, tags in source.items():
            collected_labels[host] = {}
            for tag, value in tags.items():
                if label_prefix:
                    tag = f"{label_prefix}/{tag}"
                collected_labels[host].update({tag.strip(): value.strip()})
        return collected_labels
