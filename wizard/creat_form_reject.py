from odoo import fields, models,api
from odoo.exceptions import ValidationError

class CreatRejectModel(models.TransientModel):
    _name = "creat.reject"
    _description = "Pay"

    reject = fields.Text()



