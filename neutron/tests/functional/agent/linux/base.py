# Copyright 2014 Cisco Systems, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from debtcollector import moves
import testscenarios

from neutron.common import utils
from neutron.tests.functional import base


MARK_VALUE = '0x1'
MARK_MASK = '0xffffffff'
ICMP_MARK_RULE = ('-j MARK --set-xmark %(value)s/%(mask)s'
                  % {'value': MARK_VALUE, 'mask': MARK_MASK})
MARKED_BLOCK_RULE = '-m mark --mark %s -j DROP' % MARK_VALUE
ICMP_BLOCK_RULE = '-p icmp -j DROP'


get_rand_name = moves.moved_function(
    utils.get_rand_name, 'get_rand_name', __name__,
    message='use "neutron.common.utils.get_rand_name" instead',
    version='Newton', removal_version='Ocata')


# Regarding MRO, it goes BaseOVSLinuxTestCase, WithScenarios,
# BaseSudoTestCase, ..., UnitTest, object. setUp is not defined in
# WithScenarios, so it will correctly be found in BaseSudoTestCase.
class BaseOVSLinuxTestCase(testscenarios.WithScenarios, base.BaseSudoTestCase):
    scenarios = [
        ('vsctl', dict(ovsdb_interface='vsctl')),
        ('native', dict(ovsdb_interface='native')),
    ]

    def setUp(self):
        super(BaseOVSLinuxTestCase, self).setUp()
        self.config(group='OVS', ovsdb_interface=self.ovsdb_interface)
