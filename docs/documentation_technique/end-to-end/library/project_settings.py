# Copyright (c) 2017-2021 Neogeo-Technologies.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import datetime


def get_variables():
    variables = {
                "RANDOMPROJECTNAME":            "Tests automatisés",#"projet - {}".format(datetime.datetime.now()),
                "RANDOMFEATURETYPENAME":        "TypeAuto", #"type - {}".format(datetime.datetime.now()),
                "RANDOMFEATURENAME":            "SignalementAuto",#"signalement - {}".format(datetime.datetime.now()),
                "PROJECTEDITION":               "-projet édité",
                "MARKDOWNDESCRIPTION":          "# Description en h1\n## Description en h2",
                "FEATURETYPEEDITION":           "-type édité",
                "FEATUREEDITION":               "-signalement édité",
                "SYMBOLCOLORCODE":              "#a24ae3",
                "SYMBOLOPACITY":                "0.31",
                "SYMBONAMELIST":                "list",
                "SYMBONAMECHAR":                "char",
                "SYMBONAMEBOOL":                "boolean",
                "SYMBOPTIONLIST":               ["option-1", "option-2"],
                "SYMBOPTIONCOLORLIST":          ["#84e26d", "#f38e25"],
                "SYMBOPTIONOPACITYLIST":        ["0.15", "0.69"],
                "FASTFEATURENAME":              "FastFeature",
                "FASTFEATUREDESCRIPTION":       "FastDescription",
                "MULTIGEOMFILENAME":            "multipoint",
                "MULTICHOICESLISTNAME":         "typeVegetation",
                "MULTICHOICESLISTOPTIONS":      ["persistant", "exotique", "feuillu", "arbustif", "envahissant"],
                "MULTICHOICEFEATURETYPENAME":   "Type de végétation",
                "MULTICHOICEFEATURENAME":       "SEMIARUNDINARIA yashadake 'Kimmei",
                }
    return variables
