#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# SPDX-FileCopyrightText: © 2023 PL Automation Monitoring GmbH <pl@automation-monitoring.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# This file is part of the Checkmk Labelpicker project (https://labelpicker.mk)

from abc import ABC, abstractmethod


class Strategy(ABC):
    """Source Strategy Interface"""

    @abstractmethod
    def source_algorithm(self) -> None:
        pass

    @abstractmethod
    def process_algorithm(self) -> None:
        pass
