from odoo import fields, models,api
from odoo.exceptions import ValidationError

class PayModel(models.Model):
    _name = "emp.pay"
    _inherit = ['mail.thread','mail.activity.mixin']
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
    state = fields.Selection(selection=[
        ('reject', 'Reject'),
        ('draft', 'Draft'),
        ('dl', 'DL Review'),
        ('bod', 'BOD Review'),
        ('approve','Approve')
    ], default='draft', string = 'Status',tracking = True)


    def emp_submit(self):
        self.state = 'dl'
        # for record in self:
        #     record.state = 'dl'

    def std_emp_submit(self):
        self.state = 'draft'
        # for record in self:
        #     record.state = 'draft'

    def dl_submit(self):
        self.state = 'bod'
        # for record in self:
        #     record.state = 'bod'

    def reject_dl_submit(self):
        self.state = 'reject'
        # for record in self:
        #     record.state = 'reject'

    def bod_submit(self):
        self.state = 'approve'
        # for record in self:
        #     record.state = 'approve'

    def reject_bod_submit(self):
        self.state = 'reject'
        # for record in self:
        #     record.state = 'reject'