from odoo import fields, models,api
from odoo.exceptions import ValidationError

class CreatRejectWizard(models.TransientModel):
    _name = "creat.reject.wizard"
    _description = "Pay wizard"

    reject = fields.Text(required=True,tracking=True)
    name = fields.Many2one('emp.pay', string="ABC", required=True)
    id_user = fields.Many2one('res.users', string='USER Related', default=lambda seft: seft.env.user, required=True)
    state = fields.Selection(related = "name.state")

    def reject_dl_submit(self):
        for record in self:
            record.state = 'reject'



