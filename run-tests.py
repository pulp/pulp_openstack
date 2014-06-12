#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

from pulp.devel.test_runner import run_tests

# Find and eradicate any existing .pyc files, so they do not eradicate us!
PROJECT_DIR = os.path.dirname(__file__)
subprocess.call(['find', PROJECT_DIR, '-name', '*.pyc', '-delete'])

config_file = os.path.join(PROJECT_DIR, 'flake8.cfg')
retval = subprocess.call(['flake8', '--config', config_file, PROJECT_DIR])

if retval != 0:
    sys.exit(retval)

# the warn ignore codes should be a subset of the fail codes
# GOAL: remove all ignores, always fail if these exist
pep257_warn_ignore_codes = 'D100,D103,D200,D202,D203,D205,D400,D401,D402'
pep257_fail_ignore_codes = 'D100,D102,D103,D200,D202,D203,D205,D400,D401,D402'

print "checking pep257 for warnings, ignoring %s" % pep257_warn_ignore_codes
subprocess.call(['pep257', '--ignore=' + pep257_warn_ignore_codes])

print "checking pep257 for failures, ignoring %s" % pep257_fail_ignore_codes
retval = subprocess.call(['pep257', '--ignore=' + pep257_fail_ignore_codes])

if retval != 0:
    sys.exit(retval)

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

run_tests(PACKAGES, dir_safe_all_platforms, dir_safe_non_rhel5)
