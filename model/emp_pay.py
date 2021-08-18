from odoo import fields, models,api
from odoo.exceptions import ValidationError

class PayModel(models.Model):
    _name = "emp.pay"
    _description = "Pay"

    name = fields.Many2one('emp.contracts', string = "Employee",required=True)
    id_user = fields.Many2one('res.users', string='USER Related',default = lambda seft:seft.env.user,required=True)
    department = fields.Selection(string="Department ",related = 'name.depart')
    account = fields.Many2one(string = 'Account ',related = "name.account")
    numb = fields.Integer(string='Mức Lương Hiện Tại ',related = 'name.num_pay', default=0)
    req = fields.Date(string="Ngày Điều Chỉnh Lương Gần Nhất ", default=fields.Date.today())
    numa = fields.Integer(string='Mức Lương Đề Xuất ', default=0,required=True)
    ly_do = fields.Text(string = 'Lý do điều chỉnh ',required=True)
    active = fields.Boolean('Active', default=True, tracking=True)
    # thong tin hop dong
    hop_dong = fields.Char("Hợp Đồng")
    # date_ky = fields.Date("Start Date",related = 'name.date_ky')
    date_start = fields.Date("Start Date", related='name.date_start')

    @api.constrains('req')
    def _check_date(self):
        for i in self:
            if i.req > fields.Date.today():
                raise ValidationError("Ngày chưa tồn tại")

    # , required = True, readonly = True, copy = False, tracking = True
    #draft,dl,bod
    status = fields.Selection(selection=[
        ('reject', 'Reject'),
        ('draft', 'Draft'),
        ('dl', 'DL Review'),
        ('bod', 'BOD Review'),
        ('approve','Approve')
    ], default='draft')


    def emp_submit(self):
        for record in self:
            record.status = 'dl'

    def cancel_emp_submit(self):
        for record in self:
            record.status = 'draft'

    def dl_submit(self):
        for record in self:
            record.status = 'bod'



    def bod_submit(self):
        for record in self:
            record.status = 'approve'