# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-2016 Smile (<http://www.smile.fr>). All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "Source Code Management",
    "depends": ["mail"],
    'version': "13.0.1.2",
    'author': "SoftwareEscarlata",
    "description": """Source Code Management
    
    """,
    "summary": "",
    "website": "http://www.softwareescarlata.com",
    "category": 'Tools',
    "sequence": 19,
    "data": [
        "security/scm_security.xml",
        "security/ir.model.access.csv",
        "data/scm.vcs.csv",
        "data/scm.version.csv",
        "data/scm.repository.tag.csv",
        "data/ir_cron.xml",
        "views/scm_vcs_view.xml",
        "views/scm_version_view.xml",
        "views/scm_repository_tag_view.xml",
        "views/scm_repository_view.xml",
        "views/scm_repository_branch_view.xml",
        "views/scm_dashboard.xml",
        "views/scm_menu.xml",

    ],
    'autoinstall': True,
    "installable": True,
    "application": False,
}
