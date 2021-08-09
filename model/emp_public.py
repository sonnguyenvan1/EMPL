from odoo import fields, models,api
from odoo.exceptions import ValidationError

class EmployeeModel(models.Model):
    _name = "emp.emplyee"
    _description = "Employee"

    name = fields.Char('Employee Name: ', default="Enter Name ", required=True, translate=True)
    description = fields.Char(string="Description")
    num_tele = fields.Integer('SĐT', required=True)
    active = fields.Boolean('Active', default=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string = "Gender", tracking=True)
