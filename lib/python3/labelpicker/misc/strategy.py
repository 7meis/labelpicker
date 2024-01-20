#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2023 PL Automation Monitoring GmbH <pl@automation-monitoring.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# This file is part of the Checkmk Labelpicker project (https://labelpicker.mk)

"""Abstract Source Strategy Interface."""

from abc import ABC, abstractmethod


class Strategy(ABC):
    """Source Strategy Interface."""

    @abstractmethod
    def source_algorithm(self) -> dict:
        """Abstract Function."""
        pass

    @abstractmethod
    def process_algorithm(self) -> dict:
        """Abstract Function."""
        pass
