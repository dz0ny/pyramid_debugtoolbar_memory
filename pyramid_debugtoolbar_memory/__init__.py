# -*- coding: utf-8 -*-
"""Debug toolbar."""

from .panels.pyramid_memory import MemoryDebugPanel


def includeme(config):
    config.registry.settings['debugtoolbar.panels'].append(MemoryDebugPanel)
