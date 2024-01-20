#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2023 PL Automation Monitoring GmbH <pl@automation-monitoring.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# This file is part of the Checkmk Labelpicker project (https://labelpicker.mk)

"""Implements coloring for console output."""

class bgcolor:
    """Class who make Admin's life more colorful."""
    def __init__(self):
        """Used for coloring outputs."""
        self.H1 = "\033[1;30;43m"
        self.H2 = "\033[1;30;47m"
        self.H3 = "\033[1;97;44m"
        self.GREEN = "\033[37;5;82m"
        self.WARNING = "\033[93m"
        self.FAIL = "\033[91m"
        self.END_C = "\033[0m"
        self.BOLD = "\033[1m"
        self.UNDERLINE = "\033[4m"

    def h1(self, text, width=50):
        """H1 font definition."""
        width = width - len(text)
        space = " " * (int(width / 2))
        return f"{self.H1}{space}{text}{space}{self.END_C}"

    def h2(self, text, width=41, indent=2):
        """H2 font definition."""
        width = width - len(text)
        space = " " * (int(width - indent))
        return f"{self.H2}  {text}{space}{self.END_C}"

    def h3(self, text, width=20, indent=4):
        """H3 font definition."""
        width = width - len(text)
        space = " " * (int(width - indent))
        return f"{self.H3}{' '*4}{text}{space}{self.END_C}"
