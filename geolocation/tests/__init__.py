# coding=utf-8
#
# Location Plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2013 Daniele Pantaleone <fenix@bigbrotherbot.net>
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

import time
import logging
import unittest2
import sys

from mock import Mock
from mockito import unstub
from nose.plugins.attrib import attr
from b3.config import MainConfig
from b3.config import CfgConfigParser
from geolocation import GeolocationPlugin
from geolocation.location import Location


class logging_disabled(object):
    """
    Context manager that temporarily disable logging.
    USAGE:
        with logging_disabled():
            # do stuff
    """
    DISABLED = False

    def __init__(self):
        self.nested = logging_disabled.DISABLED

    def __enter__(self):
        if not self.nested:
            logging.getLogger('output').propagate = False
            logging_disabled.DISABLED = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.nested:
            logging.getLogger('output').propagate = True
            logging_disabled.DISABLED = False


class GeolocationTestCase(unittest2.TestCase):

    def setUp(self):
        # create a FakeConsole parser
        parser_ini_conf = CfgConfigParser()
        parser_ini_conf.loadFromString(r'''''')
        self.parser_main_conf = MainConfig(parser_ini_conf)

        with logging_disabled():
            from b3.fake import FakeConsole
            self.console = FakeConsole(self.parser_main_conf)

        self.console.screen = Mock()
        self.console.time = time.time
        self.console.upTime = Mock(return_value=3)
        self.console.cron.stop()

        self.p = GeolocationPlugin(self.console)
        self.p.onLoadConfig()
        self.p.onStartup()

        with logging_disabled():
            from b3.fake import FakeClient

        self.mike = FakeClient(console=self.console, name="Mike", guid="MIKEGUID", groupBits=1)

    def tearDown(self):
        unstub()

    ####################################################################################################################
    #                                                                                                                  #
    #  TEST GEOLOCATION RETRIEVAL                                                                                      #
    #                                                                                                                  #
    ####################################################################################################################

    @attr('slow')
    def test_event_client_geolocation_success(self):
        # GIVEN
        self.mike.ip = '8.8.8.8'
        # WHEN
        self.mike.connects("1")
        time.sleep(6)  # give a chance to the thread to do its job, so retrieve data and create the event
        # THEN
        self.assertEqual(True, hasattr(self.mike, 'location'))
        self.assertIsNotNone(self.mike.location)
        self.assertIsInstance(self.mike.location, Location)
        print >> sys.stderr, "IP: %s : %r" % (self.mike.ip, self.mike.location)

    @attr('slow')
    def test_event_client_geolocation_failure(self):
        # GIVEN
        self.mike.ip = '--'
        # WHEN
        self.mike.connects("1")
        time.sleep(6)  # give a chance to the thread to do its job, so retrieve data and create the event
        # THEN
        self.assertIsNone(self.mike.location)
        print >> sys.stderr, "IP: %s : %r" % (self.mike.ip, self.mike.location)

    @attr('slow')
    def test_event_client_geolocation_success_maxmind(self):
        # GIVEN
        self.p._geolocators.pop(0)
        self.p._geolocators.pop(0)
        self.p._geolocators.pop(0)
        self.mike.ip = '8.8.8.8'
        # WHEN
        self.mike.connects("1")
        time.sleep(2)  # give a chance to the thread to do its job, so retrieve data and create the event
        # THEN
        self.assertGreaterEqual(len(self.p._geolocators), 1)
        self.assertIsNotNone(self.mike.location)
        self.assertIsNone(self.mike.location.isp)
        print >> sys.stderr, "IP: %s : %r" % (self.mike.ip, self.mike.location)

    @attr('slow')
    def test_event_client_geolocation_success_maxmind_using_event_client_update(self):
        # GIVEN
        self.p._geolocators.pop(0)
        self.p._geolocators.pop(0)
        self.p._geolocators.pop(0)
        self.mike.ip = ''
        self.mike.connects("1")
        # WHEN
        self.mike.ip = '8.8.8.8'
        self.mike.save(self.console)
        time.sleep(4)  # give a chance to the thread to do its job, so retrieve data and create the event
        # THEN
        self.assertGreaterEqual(len(self.p._geolocators), 1)
        self.assertEqual(True, hasattr(self.mike, 'location'))
        self.assertIsNotNone(self.mike.location)
        self.assertIsInstance(self.mike.location, Location)
        print >> sys.stderr, "IP: %s : %r" % (self.mike.ip, self.mike.location)