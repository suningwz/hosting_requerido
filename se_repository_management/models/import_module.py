import time
import datetime
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo import api, fields, models, tools, _
import zipfile
import os
import base64

import shutil

nlist_path = []
list_of_addons_paths = tools.config['addons_path'].split(",")
for path in list_of_addons_paths:
    nlist_path.append((path, path))


class upload_module(models.Model):
    _name = 'upload.module'

    name = fields.Char(string='Name')
    panel_id = fields.Many2one(
        comodel_name='panel.tool',
        string='Panel_id',
        required=False)
    addons_paths = fields.Selection(nlist_path,
                                    string="Add-ons Paths", help="Please choose one of these directories to put "
                                                                 "your module in",
                                    required=True)
    data_file = fields.Binary('Detail')
    datas_fname = fields.Char('File Name')
    dir = fields.Char('Dir Name')

    @api.model
    def create(self, values):
        try:
            directory_to_extract_to = values['addons_paths']
            values['name'] = values['datas_fname']
            file_content = base64.b64decode(values['data_file'])
            file_path = os.path.join(directory_to_extract_to, values['datas_fname'])
            with open(file_path, "wb") as f:
                f.write(file_content)

            zip_ref = zipfile.ZipFile(file_path, 'r')
            zip_ref.extractall(directory_to_extract_to)
            dirs = list(set([os.path.dirname(x) for x in zip_ref.namelist()]))
            values['dir'] = dirs[0].split('/')[0]
            zip_ref.close()
            self.deleteFile(file_path)

        except Exception as e:
            print(e)
        return super(upload_module, self).create(values)

    def unlink(self):
        try:
            shutil.rmtree(os.path.join(self.addons_paths, self.dir))
        except:
            print('Error while deleting directory')
        return super(upload_module, self).unlink()

    def deleteDir(self, dirPath):
        deleteFiles = []
        deleteDirs = []
        for root, dirs, files in os.walk(dirPath):
            for f in files:
                deleteFiles.append(os.path.join(root, f))
            for d in dirs:
                deleteDirs.append(os.path.join(root, d))
        for f in deleteFiles:
            os.remove(f)
        for d in deleteDirs:
            os.rmdir(d)
        os.rmdir(dirPath)

    def deleteFile(self, file_path):
        ## If file exists, delete it ##
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:  ## Show an error ##
            print("Error: %s file not found" % file_path)

