#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# SPDX-FileCopyrightText: © 2023 PL Automation Monitoring GmbH <pl@automation-monitoring.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# This file is part of the Checkmk Labelpicker project (https://labelpicker.mk)


from misc.abstract_strategy import Strategy


class LabelDataProcessor:
    """Primary class to handle label data sourcing & processing strategies"""

    def __init__(self, strategy: Strategy = None) -> None:
        if strategy is not None:
            self.strategy = strategy
        else:
            # default strategy
            pass

    def get(self, **kwargs):
        """Get source data"""
        return self.strategy.source_algorithm(**kwargs)

    def process(self, source_data, **kwargs):
        """Process source data
        Returns dict with host as key and labels as value
        Example:

        {'localhost': {'csv/tester': 'Mustermann',
                       'csv/Building': 'A',
                       'csv/Owner': 'Internal-IT',
                       'csv/Room': '305'},
         'testhost1': {'csv/Building': 'A',
                       'csv/Owner': 'Test-Automation',
                       'csv/Room': '305'},
         'testhost2': {'csv/Building': 'B',
                       'csv/Owner': 'Test-Automation',
                       'csv/Room': '104'}}
        """
        return self.strategy.process_algorithm(source_data, **kwargs)
