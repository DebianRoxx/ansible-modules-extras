#!/usr/bin/python
#coding: utf-8 -*-

# (c) 2016, Sylvain DEROSIAUX <sylvain.derosiaux@univ-lille3.fr>
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

DOCUMENTATION = '''
---
module: apache2_config
version_added: 2.0
author: "Sylvain DEROSIAUX"
short_description: enables/disables a configuration of the Apache2 webserver
description:
   - Enables or disables a specified configuration of the Apache2 webserver.
options:
   name:
     description:
        - name of the configuration to enable/disable
     required: true
   state:
     description:
        - indicate the desired state of the resource
     choices: ['present', 'absent']
     default: present

requirements: ["a2enconf","a2disconf"]
'''

EXAMPLES = '''
# enables the Apache2 configuration "php5-fpm"
- apache2_config: state=present name=php5-fpm

# disables the Apache2 configuration "php5-fpm"
- apache2_config: state=absent name=php5-fpm
'''

import re

def _disable_config(module):
    name = module.params['name']
    a2disconf_binary = module.get_bin_path("a2disconf")
    if a2disconf_binary is None:
        module.fail_json(msg="a2disconf not found. Perhaps this system does not use a2disconf to manage apache configuration.")

    result, stdout, stderr = module.run_command("%s %s" % (a2disconf_binary, name))

    if re.match(r'.*\b' + name + r' already disabled', stdout, re.S|re.M):
        module.exit_json(changed = False, result = "Success")
    elif result != 0:
        module.fail_json(msg="Failed to disable config %s: %s" % (name, stdout))
    else:
        module.exit_json(changed = True, result = "Disabled")

def _enable_config(module):
    name = module.params['name']
    a2enconf_binary = module.get_bin_path("a2enconf")
    if a2enconf_binary is None:
        module.fail_json(msg="a2enconf not found. Perhaps this system does not use a2enconf to manage apache configuration.")

    result, stdout, stderr = module.run_command("%s %s" % (a2enconf_binary, name))

    if re.match(r'.*\b' + name + r' already enabled', stdout, re.S|re.M):
        module.exit_json(changed = False, result = "Success")
    elif result != 0:
        module.fail_json(msg="Failed to enable config %s: %s" % (name, stdout))
    else:
        module.exit_json(changed = True, result = "Enabled")

def main():
    module = AnsibleModule(
        argument_spec = dict(
            name  = dict(required=True),
            state = dict(default='present', choices=['absent', 'present'])
        ),
    )

    if module.params['state'] == 'present':
        _enable_config(module)

    if module.params['state'] == 'absent':
        _disable_config(module)

# import module snippets
from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
