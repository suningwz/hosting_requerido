from psycopg2 import ProgrammingError, OperationalError, InterfaceError, DatabaseError, DataError, IntegrityError, \
    InternalError, NotSupportedError
from odoo import models, fields, api, _,service,tools
from odoo.exceptions import UserError, Warning, ValidationError
import re
import os,subprocess,shutil

class PanelTool(models.Model):
    _name = 'panel.tool'
    _description = 'Tools'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    repository_ids = fields.Many2many(
        comodel_name='repository.repository',
        string='Repositorios')

    module_upload = fields.One2many(
        comodel_name='upload.module',
        inverse_name='panel_id',
        string='Subir Modulos')


    command_exe = fields.Char(
        string='Command Server',
        required=False)

    msg_cmd = fields.Html(string=' ', readonly=True)

    sql_instruction = fields.Text(
        string="SQL Instruction",
        default="select * from res_partner;",
        track_visibility='onchange')

    msg_sql = fields.Char(string=' ', readonly=True)

    html_field = fields.Html(
        string='sql result',
        readonly=True,
        help="Enter an sql statement to execute in the Postgres database")

    alias_id = fields.Many2one('mail.alias', string='Alias', ondelete="restrict", required=False,
                               help=_(
                                   "Internal email associated with this project. Incoming emails are automatically synchronized "
                                   "with Tasks (or optionally Issues if the Issue Tracker module is installed)."))
    odoo_log = fields.Html(
        string='Odoo Log', 
        required=False,compute='compute_error_log')

    def excute_select(self):
        try:
            result_row = self.env.cr.dictfetchall()
            thead = "<tr>"
            tds = ""
            table = """
                <div  class="table-responsive"  style="height:400px; overflow-y:hidden; overflow: scroll;">
                <table class="table table-hover">
                    %s
                    <tbody >
                    %s
                    </tbody>
                    </table>
                """
            cant = len(result_row)
            if cant:
                check_query = True
                thead += "<thead><tr><th scope='col'>#</th>"
                theadkeys = result_row[0].keys()
                for key in theadkeys:
                    thead += """
                    <th scope="col">%s</th>
                    """ % key
                thead += "</tr></thead>"
            self.msg_sql = cant
            cant = 1
            for row in result_row:
                tds += "<tr><td>%s</td>" % cant
                cant += 1
                for value in row:
                    tds += "<td>%s</td>" % row[value]
                tds += "</tr>"
            table_out = table % (thead, tds)
            self.html_field = table_out
        except (ProgrammingError, OperationalError, InterfaceError,
                DatabaseError, DataError, IntegrityError, InternalError,
                NotSupportedError) as e:
            raise UserError(e.pgerror)

    def capture_sql_field(self):
        if self.sql_instruction:
            query = "%s" % self.sql_instruction
            lower_query = query.lower()
            convert_lower_query = lower_query.split(' ')
            try:
                self._cr.execute(query)
            except (ProgrammingError, OperationalError, InterfaceError,
                    DatabaseError, DataError, IntegrityError, InternalError,
                    NotSupportedError) as e:
                code_error = 'Code Error: %s' % e.pgcode
                error = e.pgerror
                error_message = """%s
                %s""" % (code_error, error)
                raise UserError(error_message)
                return
            for i in convert_lower_query:
                if i == 'select':
                    self.excute_select()
                    return
            self.message()

    def message(self):
        convert_lower_list_query = (self.sql_instruction.lower()).split(' ')
        for i in convert_lower_list_query:
            if i == 'insert':
                type_query = 'Insert'

            elif i == 'update':
                type_query = 'Update'

            elif i == 'delete':
                type_query = 'Delete'

        msg_sql = _('%s - successful consultation!') % type_query
        self.html_field = '<div class="alert alert-success">%s</div>' % msg_sql

    def execute_on_shell(self):
        try:
            res = subprocess.check_output(self.command_exe, stderr=subprocess.STDOUT, shell=True)

            self.msg_cmd=res.decode().rstrip()

        except Exception as e:
            self.msg_cmd=str(e)
            return False


    def reboot_server_odoo(self):
        service.server.restart()


    def compute_error_log(self):
        for rec in self:
            log_path=tools.config['logfile']
            if os.path.exists(log_path):
                with open(log_path, encoding="utf8") as f:
                    lines = f.readlines()
                error_content = """<div  style=" width: 100%; height: 600px;  overflow-y: auto;color:rgb(255,255,255);  background: black;">"""
                for line in lines:
                    error_content += '<p>'
                    error_content += line
                    error_content += '</p>'
                error_content += '</div>'
                rec.odoo_log=error_content
            else:
                rec.odoo_log = "No se encontrò el archivo del Log"
