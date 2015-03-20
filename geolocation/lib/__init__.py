#
# Geolocation Plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2015 Daniele Pantaleone <fenix@bigbrotherbot.net>
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

import imp
import sys
import os
import os.path


def import_module(name):
    """
    Import a module from this directory.
    Will modify sys.modules so it will be available system wide
    :param name: The module name
    :raise ImportError: If the module can't be found
    """
    f, p, d = imp.find_module(name, [os.path.dirname(os.path.realpath(__file__))])
    try:
        sys.modules['Cookie'] = imp.load_module(name, f, p, d)
    finally:
        if f:
            f.close()


if not 'Cookie' in sys.modules:
    import_module('Cookie')