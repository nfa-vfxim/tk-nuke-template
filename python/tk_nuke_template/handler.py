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

class NukeTemplateHandler():
    """
    Main application
    """

    def __init__(self):
        """
        Constructor
        """

        # most of the useful accessors are available through the Application class instance
        # it is often handy to keep a reference to this. You can get it via the following method:
        self.app = sgtk.platform.current_bundle()


        # logging happens via a standard toolkit logger
        logger.info("Launching Template Generation Application...")

    def checkForPlaceholder(self):
        logger.info("Checking for placeholder node.")
        # Checks if script contains the placeholder node
        placeholderFound = False

        for node in nuke.allNodes('ModifyMetaData'):
            if node.name() == 'createTemplatePlaceholder':
                placeholderFound = True

        if placeholderFound:
            # If node is found, initiate template generation
            logger.info("Placeholder node found. Initiating template generation...")
            self.generateTemplate()


    def generateTemplate(self):
        # Script to process nodes
        #nuke.message("Current Context: %s" % self._app.context)
        allNodes = nuke.allNodes()

        # Creating variable
        writeNode = ''

        # Handling for when no viewer node exists
        viewerNode = False

        # Delete unnecessary nodes
        for node in allNodes:
            if node.Class() == 'WriteTank':
                writeNode = nuke.toNode(node.name())
            if node.name() == 'ShotgunWriteNodePlaceholder':
                writeNode = nuke.toNode(node.name())
            if node.Class() == 'Viewer':
                viewerNode = nuke.toNode(node.name())

            if not node.Class() in ['Read', 'WriteTank', 'ShotgunWriteNodePlaceholder', 'createTemplatePlaceholder', 'Merge', 'TimeOffset', 'Viewer'] and not node.name() == 'ShotgunWriteNodePlaceholder':
                nuke.delete(node)


        ### Replacing nodes
        # Calculating ShotGrid template paths
        templatePath = self.app.get_template("template_nuke_script")
        currentPath = nuke.root().name()
        templatePath = templatePath.apply_fields(currentPath)
        templatePath = templatePath.replace(os.sep, '/')

        # Pasting template file
        template = nuke.nodePaste(templatePath)
        template = nuke.selectedNodes()

        # Get current location of read node
        readNode = nuke.toNode('Read1')
        readNodeX = readNode['xpos'].value()
        readNodeY = readNode['ypos'].value()

        # Get current location of dot
        plateNoOp = nuke.toNode('plateNoOp')
        XplateNoOp = plateNoOp['xpos'].value()
        YplateNoOp = plateNoOp['ypos'].value()

        # Calculate postion adjustment
        xDifference = XplateNoOp - readNodeX
        yDifference = YplateNoOp - readNodeY

        # Replace pasted nodes
        for node in template:
            xPos = node['xpos'].value()
            yPos = node['ypos'].value()
            node['xpos'].setValue(xPos-xDifference)
            node['ypos'].setValue(yPos-yDifference+25)

        ### Reconnecting nodes
        # Connect read node
        plateNoOp.setInput(0, readNode)
        nuke.delete(plateNoOp)

        # Reposition write node
        writeNoOp = nuke.toNode('writeNoOp')
        xWriteNoOp = writeNoOp['xpos'].value()
        yWriteNoOp = writeNoOp['ypos'].value()

        if not writeNode == '':
            writeNode.setInput(0, writeNoOp)
            writeNode['xpos'].setValue(xWriteNoOp)
            writeNode['ypos'].setValue(yWriteNoOp)

        nuke.delete(writeNoOp)

        # Reposition viewer node
        if viewerNode:
            viewerNode['xpos'].setValue(xWriteNoOp)
            viewerNode['ypos'].setValue(yWriteNoOp+200)


    def addCallbacks(self):
        # Add callbacks when changing context
        nuke.addOnScriptLoad(self.checkForPlaceholder, nodeClass="Root")

    def removeCallbacks(self):
        nuke.removeOnScriptLoad(self.checkForPlaceholder, nodeClass="Root")
