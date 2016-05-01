########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

from setuptools import setup, find_packages
import os
import codecs

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()


setup(
    name='spuc',
    version='0.0.1',
    author='Gigaspaces',
    author_email='cosmo-admin@gigaspaces.com',
    license='LICENSE',
    platforms='All',
    description='Creates users in different platforms.',
    long_description=read('README.rst'),
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'spuc = spuc.spuc:main',
        ]
    },
    install_requires=[
        "apiclient==1.0.2",
        "boto3==1.3.1",
        "botocore==1.4.13",
        "click===6.6",
        "google-api-python-client==1.5.0",
        "httplib2==0.9.2",
        "jira==1.0.3",
        "oauth2client==2.0.2",
        "requests==2.9.1",
        "urllib3==1.15.1",
        "PyYAML==3.11"
    ]
)
