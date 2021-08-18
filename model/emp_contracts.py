from odoo import fields, models,api
from odoo.exceptions import ValidationError

class ContractModel(models.Model):
    _name = "emp.contracts"
    _description = "Employee"

    name = fields.Char(string = "Employee",required=True,translate=True)
    account = fields.Many2one('res.users', string='Account',default = lambda seft:seft.env.user,required=True)
    address = fields.Char('Địa Chỉ')
    num_tele = fields.Char('SĐT', required=True)
    active = fields.Boolean('Active', default=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender", tracking=True)
    depart = fields.Selection([
        ('vms', 'VTI.VMS'),
        ('d1', 'VTI.D1'),
        ('ga', 'VTI.GA'),
        ('rec', 'VTI.REC'),
        ('d2', 'VTI.D2')
    ], string = "Department", tracking=True)
    email = fields.Char('Email ', default="abc@xyz.com", required=True)
    num_pay = fields.Integer(string = 'Lương Thỏa Thuận',required=True)
    date_ky = fields.Date("Ngày Ký",default=fields.Date.today())
    date_start = fields.Date("Ngày Bắt Đầu Làm Việc",default=fields.Date.today())


