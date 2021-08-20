from odoo import fields, models,api
from odoo.exceptions import ValidationError

class CreatRejectWizard(models.TransientModel):
    _name = "creat.reject.wizard"
    _inherit = ['emp.pay']
    _description = "Pay wizard"

    reject = fields.Text(required=True,tracking=True)
    id_user = fields.Many2one('res.users', string='USER Related', default=lambda seft: seft.env.user, required=True)



