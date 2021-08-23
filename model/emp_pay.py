from docutils.nodes import field_name
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class PayModel(models.Model):
    _name = "emp.pay"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Salary Employee"

    resource_id = fields.Many2one('resource.resource')
    employee_id = fields.Many2one('hr.employee', string='Employee', tracking=True)
    contracts_id = fields.Many2one('hr.contract', string='Hợp Đồng', tracking=True)
    user_id = fields.Many2one(related='employee_id.user_id', store=True, readonly=True,
                              string='Account')
    department_id = fields.Many2one('hr.department', compute='_compute_employee_salary', store=True, readonly=True,
                                    string="Department")
    job_id = fields.Many2one('hr.job', compute='_compute_employee_salary', store=True, readonly=True,
                             string='Job Position')
    job_title = fields.Char('Job Title', related='employee_id.job_title', readonly=False, related_sudo=False)
    wage = fields.Many2one('hr.contract', compute='_compute_contract_salary', store=True, readonly=True,
                           string="Mức lương hiện tại")
    req = fields.Date(string="Ngày Điều Chỉnh Lương Gần Nhất ")
    numa = fields.Integer(string='Mức Lương Đề Xuất ', default=0, required=True)
    ly_do = fields.Text(string='Lý do điều chỉnh ', required=True)
    # name_contract = fields.Many2one('hr.contract',)

    # wage = fields.Monetary(string="Lương hiện tại", readonly=True)

    # @api.onchange('employee_id')
    # def _compute_wage(self):
    #     contract = self.env['hr.contract'].sudo().search(
    #         [('contracts_id', '=', self.contracts_id.id), ('state', '=', 'open')])
    #     if contract:
    #         self.wage = contract[0].wage

    # draft,dl,bod
    state = fields.Selection(selection=[
        ('reject', 'Reject'),
        ('draft', 'Draft'),
        ('dl', 'DL Review'),
        ('bod', 'BOD Review'),
        ('approve', 'Approve')
    ], default='draft', string='Status', track_visibility='onchange')

    @api.depends('contracts_id')
    def _compute_contract_salary(self):
        for d in self.filtered('contracts_id'):
            d.wage = d.contracts_id.wage

    @api.depends('employee_id')
    def _compute_employee_salary(self):
        for d in self.filtered('employee_id'):
            d.job_id = d.employee_id.job_id
            # d.job_title = d.employee_id.job_title
            d.department_id = d.employee_id.department_id
            # d.wage_agreement = d.employee_id.wage_agreement

    def emp_submit(self):
        for record in self:
            record.state = 'dl'

    def std_emp_submit(self):
        for record in self:
            record.state = 'draft'

    def dl_submit(self):
        for record in self:
            record.state = 'bod'

    def reject_dl_submit(self):
        for record in self:
            record.state = 'reject'

    def bod_submit(self):
        for record in self:
            record.state = 'approve'

    def reject_bod_submit(self):
        for record in self:
            record.state = 'reject'
