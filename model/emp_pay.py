from odoo import fields, models,api
from odoo.exceptions import ValidationError

class PayModel(models.Model):
    _name = "emp.pay"
    _description = "Pay"

    name = fields.Many2one('emp.emplyee', string = "Name",required=True)
    department = fields.Char(string="Department ")
    account = fields.Char(string = 'Account ')
    numb = fields.Integer(string='Mức Lương Hiện Tại ', default=0)
    req = fields.Date(string="Ngày Điều Chỉnh Lương Gần Nhất ", default=fields.Date.today())
    numa = fields.Integer(string='Mức Lương Đề Xuất ', default=0,required=True)
    ly_do = fields.Text(string = 'Lý do điều chỉnh ',required=True)


    @api.constrains('req')
    def _check_date(self):
        for i in self:
            if i.req > fields.Date.today():
                raise ValidationError("Ngày chưa tồn tại")