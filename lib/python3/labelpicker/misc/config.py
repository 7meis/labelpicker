#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2023 PL Automation Monitoring GmbH <pl@automation-monitoring.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# This file is part of the Checkmk Labelpicker project (https://labelpicker.mk)

import os
import base64
import zlib
import sys
import yaml


class Config:
    """Read config data."""

    def __init__(self, config_file):
        if config_file is True:
            # Use default config file
            omd_root = os.environ["OMD_ROOT"]
            self.config_file = os.path.join(omd_root, "etc", "labelpicker.yml")
        else:
            self.config_file = config_file

    def get_cfg(self):
        """Read config file."""
        # if file ends with .yaml or .yml use yaml loader
        if self.config_file.endswith(".yaml") or self.config_file.endswith(".yml"):
            with open(self.config_file) as f:
                return yaml.safe_load(f)
        else:
            print(f"Unknown config file format: {self.config_file}")
            sys.exit(1)

    def init_cfg(self):
        """Initialize LabelPicker default configuration file."""
        init_cfg = "eJyNVNtu2zAMfc9XEMhD2iHObXsKtmJFV2zB1jWoh+6hKQxNZhyhtiRIctJi3b+PshznurUKEFjk4eFNZBsg+vdpteEZvrFfmE8Ff0ADF0rORVYa5oSS8Ez6F8wnkqtCE/xXjuAU8OIBlmisNx/1hj09GkB0BjeX8Q84n05gYm2JLTI8pPqMEg3LgVcxVM73QYw7sWQOk7kyKDKZ8AWTGdoxOEO0nFlMyLwOYNwCyH1yY8jVCo3PZsnyEtf3fQ90/8Qcs6o0HO1hBLUe4gCIYseMw0wQlgIKvnRVyFa64fFhbBOP4eLqazShKKVT5om0X5hJV8xgFKu5qz4arTcGKFRa5j5sndpksbIrZxArTduThRbCB3hfhZBog3PxeNYP17MaePnICk1dChjJCiL0XH1lq1sF2yYI6hAA01rILERDbyLgAse2uT8+tjHcrXPpwrVG/6BkBvGTdVh04Tvh7307wimY44skM6rUyVzkjto33mi9u7vOleBGWeKEn0KmamUhRkONhtFgOIKbEVAzZEqF7HShcy65oPqtIddx5/7VfCe9N6eeg8Rr0Wz4P/uTXYJTOJmlv9/9OW2YZkOYjeAyFdVQRTB7S3RHCqkNtZm7/UKuX0e3Kd80AO9bx1jorWD+MseVh9WNOEbDNOMLTOpR2uVrbt5m3ecd4ZTxB0aDuSM8ryhHrdbBQNwWngGWsV4gMfk55dQ/NINhIjaj0D6YhaVtLPbf7o7qYDPU3azXQ6l1WA9AeYukNCRbOKftuN8fDmiN0a9v0LotjEVDhvT/MVUFE7Ln8nSj1szSVmJpIeRhuhfxrUdyu0wwDOWx3Eh9LK9G/PqcmrW3JfPOadZwM2kR9F2h+14RPNax9bzHv6yT3KI="

        # if config file does not exists, create it
        if not os.path.exists(self.config_file):
            # Decode the base64-encoded content
            decoded_content = base64.b64decode(init_cfg)
            decompressed_content = zlib.decompress(decoded_content).decode()

            # Write the decompressed content to a new file
            with open(self.config_file, "w") as file:
                file.write(decompressed_content)

            print(f"Config file {self.config_file} created.")
        else:
            print(f"Config file {self.config_file} already exists. Skipping init.")
        sys.exit(0)
