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

from utils import get_driver


def geocontrib_edit_project(project_name, project_edition):
    get_driver().find_element_by_class_name("button-hover-orange").click()
    # modify title
    title_input_elt = get_driver().find_element_by_id("title")
    title_input_elt.click()
    title_input_elt.clear()
    title_input_elt.send_keys("{}{}".format(project_name, project_edition))

    # modify description
    get_driver().find_element_by_name("description").click()
    get_driver().find_element_by_name("description").clear()
    get_driver().find_element_by_name("description").send_keys(project_edition)

    # click on dropdown "Visibilité des signalements publiés" to open it
    get_driver().find_element_by_xpath(
        "//form[@id='form-project-edit']/div[5]/div/div"
    ).click()
    # click on dropdown "Visibilité des signalements publiés" to select an option
    get_driver().find_element_by_xpath(
        "//form[@id='form-project-edit']/div[5]/div/div/div[2]/div[2]"
    ).click()

    # click on dropdown "Visibilité des signalements archivés" to open it
    get_driver().find_element_by_xpath(
        "//form[@id='form-project-edit']/div[5]/div[2]/div"
    ).click()
    # click on dropdown "Visibilité des signalements archivés" to select an option
    get_driver().find_element_by_xpath(
        "//form[@id='form-project-edit']/div[5]/div[2]/div/div[2]/div[2]"
    ).click()

    # toggle moderation
    get_driver().find_element_by_css_selector("label[for=moderation]").click()
    # toggle is_project_type
    get_driver().find_element_by_css_selector("label[for=is_project_type]").click()
    # toggle generate_share_link
    get_driver().find_element_by_css_selector("label[for=generate_share_link]").click()

    # submit the form
    get_driver().find_element_by_id("send-project").click()


def geocontrib_edit_featuretype(featuretypename, added_text):
    # got to first feature type edition page    
    get_driver().find_element_by_css_selector("a[data-tooltip*='Éditer le type de signalement']").click()
    # modify feature type title
    title_input_elt = get_driver().find_element_by_id("title")
    title_input_elt.click()
    title_input_elt.clear()
    title_input_elt.send_keys("{}{}".format(featuretypename, added_text))
    # todo: add an option to change geometry when we can test more than points
    optionnal_title_input_elt = get_driver().find_element_by_id("title_optional")
    optionnal_title_input_elt.click
    # submit the form
    get_driver().find_element_by_id("send-feature_type").click()


def geocontrib_edit_feature(feature_name, added_text):
    # go to edition page
    get_driver().find_element_by_css_selector("a[href*=editer]").click()
    # modify the name
    name_input_elt = get_driver().find_element_by_id("name")
    name_input_elt.click()
    name_input_elt.clear()
    name_input_elt.send_keys("{}{}".format(feature_name, added_text))
    # modify description
    description_input_elt = get_driver().find_element_by_name("description")
    description_input_elt.click()
    description_input_elt.clear()
    description_input_elt.send_keys(added_text)
    # modify status
    ## open the status dropdown
    get_driver().find_element_by_css_selector("#form-feature-edit div.required:nth-child(2)>div[id*='dropdown']").click()
    ## select second status option
    get_driver().find_element_by_css_selector("#form-feature-edit div.required:nth-child(2)>div[id*='dropdown'] div.menu > div.item:nth-child(2)").click()

def geocontrib_access_featuretype_symbology(featureTypeName):
    # got to first feature type edition page
    get_driver().find_element_by_css_selector(
        "#" + featureTypeName + " " + "a[data-tooltip*='Éditer la symbologie du type de signalement']"
    ).click()

def geocontrib_edit_featuretype_symbology(featuretypename, colorcode, opacity):
    color_input_elt = get_driver().find_element_by_id("couleur")
    color_input_elt.click()
    color_input_elt.clear()
    color_input_elt.send_keys(colorcode)
    # edit default symbology color
    opacity_input_elt = get_driver().find_element_by_id("opacity")
    opacity_input_elt.click()
    opacity_input_elt.clear()
    opacity_input_elt.send_keys(opacity)
    # valider le formulaire
    get_driver().find_element_by_id("save-symbology").click()
