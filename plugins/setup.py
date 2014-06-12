from setuptools import setup, find_packages

setup(
    name='pulp_openstack_plugins',
    version='0.1.0',
    packages=find_packages(),
    url='http://www.pulpproject.org',
    license='GPLv2+',
    author='Pulp Team',
    author_email='pulp-list@redhat.com',
    description='plugins for openstack image support in pulp',
    entry_points={
        'pulp.importers': [
            'importer = pulp_openstack.plugins.importers.importer:entry_point',
        ],
        'pulp.distributors': [
            'web_distributor = pulp_openstack.plugins.distributors.distributor_web:entry_point',
        ]
    }
)
