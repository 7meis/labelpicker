#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2023 PL Automation Monitoring GmbH <pl@automation-monitoring.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# This file is part of the Checkmk Labelpicker project (https://labelpicker.mk)

"""Class for label Util functions."""

class LabelHelper:
    """Label Utils."""
    def _case_conversion(label_definitions, params, prefix) -> dict:
        """Function handles case conversions."""
        converted = {}
        for host, data in label_definitions.items():
            converted[host] = {}
            for k, v in data.items():
                if "label" in params:
                    k = k.split(prefix)[1]
                    k = getattr(k, params["label"])()
                if "value" in params:
                    v = getattr(v, params["value"])()

                converted[host].update({f"{prefix}{k}": v})
        return converted
