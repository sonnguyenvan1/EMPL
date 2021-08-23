from odoo import api, fields, models
from odoo.osv import expression


class Employee(models.Model):
    _inherit = "hr.contract"


    wage_agreement = fields.Integer(string = 'Lương thỏa thuận',required = True)