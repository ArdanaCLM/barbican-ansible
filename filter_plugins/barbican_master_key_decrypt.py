#
# (c) Copyright 2015-2016 Hewlett Packard Enterprise Development LP
# (c) Copyright 2017 SUSE LLC
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

import base64
import imp
import os.path


path = os.path.dirname(os.path.realpath(__file__))

ardanaencrypt = imp.load_source('ardanaencrypt', path + '/../ardanaencrypt.py')

encryption_class = 'openssl'

ardanaencrypt_class = getattr(ardanaencrypt, encryption_class)

# Method to decrypt the Customer defined encrypted key
# It will only decrypt the key with prefix @ardana@
# Customer define this key, barbican_customer_master_key, in
# roles/barbican-common/vars/barbican_deploy_config.yml


def barbican_master_key_decrypt(value, *args, **kw):
    prefix = None
    if value.startswith(ardanaencrypt_class.prefix):
        prefix = ardanaencrypt_class.prefix
    # For upgrade cases, need to support existing encrypted values which may
    # have legacy prefix in-use.
    elif value.startswith(ardanaencrypt_class.legacy_prefix):
        prefix = ardanaencrypt_class.legacy_prefix

    if prefix is None:
        return value
    else:
        obj = ardanaencrypt_class()
        return obj.decrypt(base64.urlsafe_b64decode(
            value.encode('ascii', 'ignore')[len(prefix):]))


class FilterModule(object):
    def filters(self):
        return {'barbican_master_key_decrypt': barbican_master_key_decrypt}
