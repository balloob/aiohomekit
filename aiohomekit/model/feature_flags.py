#
# Copyright 2019 aiohomekit team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


class _FeatureFlags(object):
    """
    Data taken form table 5-8 Bonjour TXT Record Feature Flags on page 69.
    """

    def __init__(self) -> None:
        self._data = {0: "No support for HAP Pairing", 1: "Supports HAP Pairing"}

    def __getitem__(self, item: int) -> str:
        bit_value = item & 0x01
        if bit_value in self._data:
            return self._data[bit_value]

        raise KeyError("Item {item} not found".format(item=item))


FeatureFlags = _FeatureFlags()
