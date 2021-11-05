# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk
import os
import sys
import threading
import nuke

# standard toolkit logger
logger = sgtk.platform.get_logger(__name__)


class NukeTemplateHandler:
    """
    Main application
    """

    def __init__(self):
        """
        Constructor
        """

        self.app = sgtk.platform.current_bundle()

    def check_for_placeholder(self):
        logger.info("Checking for placeholder node.")
        # Checks if script contains the placeholder node
        placeholder_found = False

        for node in nuke.allNodes("ModifyMetaData"):
            if node.name() == "createTemplatePlaceholder":
                placeholder_found = True

        if placeholder_found:
            # If node is found, initiate template generation
            logger.info("Placeholder node found. Initiating template generation...")
            self.generate_template()

    def generate_template(self):
        # Script to process nodes
        # nuke.message("Current Context: %s" % self._app.context)
        all_nodes = nuke.allNodes()

        # Creating variable
        write_node = ""

        # Handling for when no viewer node exists
        viewer_node = False

        # Delete unnecessary nodes
        for node in all_nodes:
            if node.Class() == "Group":
                if node["isShotGridWriteNode"]:
                    write_node = nuke.toNode(node.name())
            if node.name() == "ShotGridWriteNodePlaceholder":
                write_node = nuke.toNode(node.name())
            if node.Class() == "Viewer":
                viewer_node = nuke.toNode(node.name())

            if (
                not node.Class()
                in [
                    "Read",
                    "WriteTank",
                    "Group",
                    "ShotgunWriteNodePlaceholder",
                    "createTemplatePlaceholder",
                    "Merge",
                    "TimeOffset",
                    "Viewer",
                ]
                and not node.name() == "ShotGridWriteNodePlaceholder"
            ):
                nuke.delete(node)

        ### Replacing nodes
        # Calculating ShotGrid template paths
        template_path = self.app.get_template("template_nuke_script")
        current_path = nuke.root().name()
        template_path = template_path.apply_fields(current_path)
        template_path = template_path.replace(os.sep, "/")

        # Pasting template file
        nuke.nodePaste(template_path)
        template = nuke.selectedNodes()

        # Get current location of read node
        read_node = nuke.toNode("Read1")
        read_node_x = read_node["xpos"].value()
        read_node_y = read_node["ypos"].value()

        # Get current location of dot
        plate_noop = nuke.toNode("plateNoOp")
        xplate_no_op = plate_noop["xpos"].value()
        yplate_no_op = plate_noop["ypos"].value()

        # Calculate postion adjustment
        x_difference = xplate_no_op - read_node_x
        y_difference = yplate_no_op - read_node_y

        # Replace pasted nodes
        for node in template:
            x_pos = node["xpos"].value()
            y_pos = node["ypos"].value()
            node["xpos"].setValue(x_pos - x_difference)
            node["ypos"].setValue(y_pos - y_difference + 25)

        ### Reconnecting nodes
        # Connect read node
        plate_noop.setInput(0, read_node)
        nuke.delete(plate_noop)

        # Reposition write node
        write_no_op = nuke.toNode("writeNoOp")
        x_write_no_op = write_no_op["xpos"].value()
        y_write_no_op = write_no_op["ypos"].value()

        if not write_node == "":
            write_node.setInput(0, write_no_op)
            write_node["xpos"].setValue(x_write_no_op)
            write_node["ypos"].setValue(y_write_no_op)

        nuke.delete(write_no_op)

        # Reposition viewer node
        if viewer_node:
            viewer_node["xpos"].setValue(x_write_no_op)
            viewer_node["ypos"].setValue(y_write_no_op + 200)

        # Unselect all nodes
        for node in nuke.selectedNodes():
            node["selected"].setValue(False)

    def add_callbacks(self):
        # Add callbacks when changing context
        nuke.addOnScriptLoad(self.check_for_placeholder, nodeClass="Root")

    def remove_callbacks(self):
        nuke.removeOnScriptLoad(self.check_for_placeholder, nodeClass="Root")
