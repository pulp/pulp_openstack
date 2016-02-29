#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

from pulp.devel import doc_check
from pulp.devel.test_runner import run_tests


# Find and eradicate any existing .pyc files, so they do not eradicate us!
PROJECT_DIR = os.path.dirname(__file__)
subprocess.call(['find', PROJECT_DIR, '-name', '*.pyc', '-delete'])

config_file = os.path.join(PROJECT_DIR, 'flake8.cfg')
retval = subprocess.call(['flake8', '--config', config_file, PROJECT_DIR])

if retval != 0:
    sys.exit(retval)

print "done, checking sphinx param docs.."

# Ensure that all doc strings are present
doc_check.recursive_check(PROJECT_DIR)

print "done"

PACKAGES = ['pulp_openstack',
            'pulp_openstack.common',
            'pulp_openstack.extensions',
            'pulp_openstack.plugins']

PACKAGES = ['pulp_openstack', 'pulp_openstack.common', 'pulp_openstack.extensions']

TESTS = [
    'common/test/unit/',
    'extensions_admin/test/unit/',
]

PLUGIN_TESTS = ['plugins/test/unit/']

dir_safe_all_platforms = [os.path.join(os.path.dirname(__file__), x) for x in TESTS]
dir_safe_non_rhel5 = [os.path.join(os.path.dirname(__file__), x) for x in PLUGIN_TESTS]

sys.exit(run_tests(PACKAGES, dir_safe_all_platforms, dir_safe_non_rhel5))
