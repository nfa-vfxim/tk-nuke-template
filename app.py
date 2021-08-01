# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import nuke
from sgtk.platform import Application


class NukeTemplateGenerator(Application):
    """
    The app entry point. This class is responsible for initializing and tearing down
    the application, handle menu registration etc.
    """

    def init_app(self):
        """
        Initialisation for tk-nuke-template
        """

        self.tk_nuke_template = self.import_module("tk_nuke_template")
        self.handler = self.tk_nuke_template.NukeTemplateHandler()

        # Add callbacks
        self.handler.addCallbacks()


    def destroy_app(self):
        """
        Called when the app is unloaded/destroyed
        """
        self.log_debug("Destroying tk-nuke-template app")

        # Remove any callbacks that were registered by the handler
        self.handler.removeCallbacks()
