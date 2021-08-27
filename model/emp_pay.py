from docutils.nodes import field_name
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class PayModel(models.Model):
    _name = "emp.pay"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Salary Employee"

    resource_id = fields.Many2one('resource.resource')
    employee_id = fields.Many2one('hr.employee', string='Employee', tracking=True,
                                  default=lambda self: self.env.user.employee_id,
                                  domain="['|', ('department_id', '=', False), ('department_id', '=', department_id)]")
    name = fields.Char(string='Hợp Đồng', store=True, readonly=True)
    work_email = fields.Char(string='Email', related='employee_id.work_email', store=True, readonly=True)
    user_id = fields.Many2one(related='employee_id.user_id', store=True,
                              string='Account')
    department_id = fields.Many2one('hr.department', compute='_compute_employee_salary', store=True, readonly=True,
                                    string="Department")
    manager_id = fields.Many2one('hr.employee', related='employee_id.parent_id.parent_id', store=True, readonly=True,
                                 string="Manager")
    job_id = fields.Many2one('hr.job', compute='_compute_employee_salary', store=True, readonly=True,
                             string='Job Position')
    job_title = fields.Char('Job Title', related='employee_id.job_title', store=True)
    parent_id = fields.Many2one('hr.employee', related='employee_id.parent_id')
    company_id = fields.Many2one('res.company', string='Company', related='employee_id.company_id', related_sudo=True,
                                 store=True, readonly=True)
    numa = fields.Integer(string='Mức Lương Đề Xuất ',default = 0 ,required=True, tracking=True)
    ly_do = fields.Text(string='Lý do điều chỉnh ', required=True, tracking=True)
    start_date = fields.Date(string="Ngày bắt đầu", store=True, readonly=True)
    end_date = fields.Date(string="Ngày kết thúc", store=True, readonly=True)
    resource_calendar_id = fields.Many2one(related='employee_id.resource_calendar_id', string='Working Schedule',
                                           readonly=True, store=True)
    structure_type_id = fields.Many2one('hr.payroll.structure.type', string="Salary Structure", store=True,
                                        readonly=True)
    currency_id = fields.Many2one('res.currency', string="Currency")
    wage = fields.Integer(string="Mức lương hiện tại", readonly=True, store=True)
    child_ids = fields.One2many('hr.employee', 'parent_id')
    notes = fields.Text()

    ratio = fields.Float(string="Tỉ lệ điều chỉnh",compute='_compute_ratio',readonly=True, store=True)
    req = fields.Date(string="Ngày điều chỉnh lương gần nhất ", store=True, readonly=True)

    state = fields.Selection(selection=[
        ('reject', 'Reject'),
        ('draft', 'Draft'),
        ('dl', 'DL Review'),
        ('bod', 'BOD Review'),
        ('approve', 'Approve')
    ], default='draft', string='Status', track_visibility='onchange')

    permission_view_action = fields.Char(string="Check view action", compute='_compute_view_action')

    def _compute_view_action(self):
        for record in self:
            if self.env.user.has_group('EMPL.group_bod_user'):
                record.permission_view_action = 'True'
            elif self.env.user.has_group('EMPL.group_dl_user') \
                    and self.env.uid == record.employee_id.department_id.manager_id.user_id.id \
                    and record.state == 'dl':
                record.permission_view_action = 'True'
            else:
                record.permission_view_action = 'False'

    @api.onchange('employee_id')
    def _onchange_employee(self):
        data = self.env['emp.pay'].sudo().search([('employee_id', '=', self.employee_id.id)], order="id desc", limit=1)
        if data:
            self.req = data.create_date

    def unlink(self):
        for r in self:
            if r.state != 'draft':
                raise ValidationError(_("Ban chi duoc xoa ban ghi o draft"))
        return super(PayModel, self).unlink()

    @api.depends('wage', 'numa')
    def _compute_ratio(self):
        for d in self:
            d.ratio = (abs(d.numa - d.wage) * 100) / d.wage

    @api.onchange('employee_id')
    def _onchange_contract_id(self):
        contract = self.env['hr.contract'].sudo().search([('employee_id', '=', self.employee_id.id),
                                                          ('state', '=', 'open')])
        if contract:
            self.start_date = contract[0].date_start
            self.end_date = contract[0].date_end
            self.name = contract[0].name
            self.structure_type_id = contract[0].structure_type_id
            self.wage = contract[0].wage


    @api.depends('employee_id')
    def _compute_employee_salary(self):
        for d in self.filtered('employee_id'):
            d.job_id = d.employee_id.job_id
            d.department_id = d.employee_id.department_id


    def action_submit(self):
        if self.env.user.has_group('EMPL.group_bod_user'):
            self.bod_submit()
        elif self.env.user.has_group('EMPL.group_dl_user'):
            self.dl_submit()
        else:
            self.emp_submit()

    def action_approved(self):
        if self.env.user.has_group('EMPL.group_bod_user'):
            self.bod_submit()
        elif self.env.user.has_group('EMPL.group_dl_user') \
                and self.env.uid == self.employee_id.department_id.manager_id.user_id.id:
            if self.state != 'dl':
                raise ValidationError(_("Bản ghi không còn ở bước bạn revew\n Nên bạn không thể approved"))
            self.dl_submit()
        else:
            raise ValidationError(_("Ban khong co quyen thuc hien hanh dong"))

    def action_reject(self):
        if self.env.user.has_group('EMPL.group_bod_user'):
            form_view = self.env.ref('EMPL.reject_bod_view_form')
            return {
                'name': 'Reject',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': form_view.id,
                'res_model': 'emp.pay',
                'type': 'ir.actions.act_window',
                'res_id': self.id,
                'target': 'new'
            }
        elif self.env.user.has_group('EMPL.group_dl_user') \
                and self.env.uid == self.employee_id.department_id.manager_id.user_id.id:
            if self.state != 'dl':
                raise ValidationError(_("Bản ghi không còn ở bước bạn revew\n Nên bạn không thể reject"))
            form_view = self.env.ref('EMPL.reject_dl_view_form')
            return {
                'name': 'Reject',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': form_view.id,
                'res_model': 'emp.pay',
                'type': 'ir.actions.act_window',
                'res_id': self.id,
                'target': 'new'
            }
        else:
            raise ValidationError(_("Bạn không có quyen"))

    def emp_submit(self):
        for record in self:
            record.state = 'dl'
        template_id = self.env.ref("EMPL.mail_template_dl_rev").id
        print(template_id)
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    def std_emp_submit(self):
        for record in self:
            if self.env.uid not in [record.employee_id.user_id.id, record.create_uid.id]:
                raise ValidationError(_("Bạn không có quyền set to draft!!!"))
            record.state = 'draft'

    def dl_submit(self):
        for record in self:
            record.state = 'bod'
        template_id = self.env.ref("EMPL.mail_template_bod_rev").id
        print(template_id)
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    def reject_dl_submit(self):
        for record in self:
            record.state = 'reject'
        template_id = self.env.ref("EMPL.mail_template_emp_rej").id
        print(template_id)
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    def bod_submit(self):
        for record in self:
            record.state = 'approve'
        template_id = self.env.ref("EMPL.mail_template_emp_app").id
        print(template_id)
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        template_id = self.env.ref("EMPL.mail_template_hr_app").id
        print(template_id)
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    def reject_bod_submit(self):
        for record in self:
            record.state = 'reject'
        template_id = self.env.ref("EMPL.mail_template_emp_rej").id
        print(template_id)
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    def action_dl_reject(self):
        form_view = self.env.ref('EMPL.reject_dl_view_form')
        return {
            'name': 'Reject',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': form_view.id,
            'res_model': 'emp.pay',
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'new'
        }

    def action_bod_reject(self):
        form_view = self.env.ref('EMPL.reject_bod_view_form')
        return {
            'name': 'Reject',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': form_view.id,
            'res_model': 'emp.pay',
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'new'
        }
