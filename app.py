# MIT License

# Copyright (c) 2021 Netherlands Film Academy

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
        self.handler.add_callbacks()


    def destroy_app(self):
        """
        Called when the app is unloaded/destroyed
        """
        self.log_debug("Destroying tk-nuke-template app")

        # Remove any callbacks that were registered by the handler
        self.handler.remove_callbacks()
