from odoo import fields, models,api
from odoo.exceptions import ValidationError

class EmployeeModel(models.Model):
    _name = "emp.emplyee"
    _description = "Employee"

    name = fields.Char('Employee Name', default="Enter Name ", required=True, translate=True)


