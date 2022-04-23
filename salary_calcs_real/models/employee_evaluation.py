# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning,ValidationError
import datetime
QUESTIONS = [
    {
        'question_title':'منظم (يضع خطة لأعماله حتى لا يكون عنده أعمال مستعجلة أو مفاجية)',
        'full_mark':10,
        'employee_mark':0
    },
        {
        'question_title':'متابع للمهام الموكلة إليه من مدرائه',
        'full_mark':15,
        'employee_mark':0
    },
        {
        'question_title':'لا يهمل المشكلات بل يتخذ الإجراءات المبكرة لحلها جذرياً وليس مؤقتاً',
        'full_mark':10,
        'employee_mark':0
    },
        {
        'question_title':'القدرة على الابداع (يبحث عن الطرق الأفضل للعمل ولا يقتصر على الطرائق السابقة)',
        'full_mark':10,
        'employee_mark':0
    },
        {
        'question_title':'يفهم الفوائد والميزات التي تقدمها تقانة المعلومات ويشجعها',
        'full_mark':15,
        'employee_mark':0
    },
        {
        'question_title':'جاهز لتحمل مسؤولية عمله الشخصي والعمل الموكل إليه',
        'full_mark':10,
        'employee_mark':0
    },    {
        'question_title':'يعطي التقارير الفنية بشكل منتظم ودقيق وواضح',
        'full_mark':10,
        'employee_mark':0
    },
    {
        'question_title':"""يتشارك بالمعلومات والأفكار مع الآخرين
(يفهم أمانة نشر العلم ويعمل بها)
""",
        'full_mark':15,
        'employee_mark':0
    },
    {
        'question_title':'يسعى لتقليل الهدر بكل أشكاله ( وقت – مواد - مياه - كهرباء)',
        'full_mark':15,
        'employee_mark':0
    },
    {
        'question_title':'يقدم اقتراحات بناءة',
        'full_mark':20,
        'employee_mark':0
    },
]

class EvalutionQuestionsType(models.Model):
    _name = 'evaluation.questions.type'

    name = fields.Char('Type')
    question_ids = fields.One2many('evaluation.questions.lines','type_id','Questions')

class EvalutionQuestionsLines(models.Model):
    _name = 'evaluation.questions.lines'

    question_title = fields.Char()
    full_mark = fields.Float()
    type_id = fields.Many2one('evaluation.questions.type')

class HREmployeesEvalution(models.Model):
    _name = 'hr.employee.evaluation'
    name = fields.Char(compute='_set_name')
    contract_id = fields.Many2one('hr.contract',string='Employee Contract',required=True,domain=[('state','=','open')])
    line_ids = fields.One2many('hr.employee.evaluation.questions', 'evaluation_id', "Questions")
    # ,default=lambda self:self.prepare_lines()
    other_month = fields.Boolean(compute="_compute_perc")
    percentage = fields.Float()
    notes = fields.Text()
    evaluation_questions_type = fields.Many2one('evaluation.questions.type', required=True)
    date_from = fields.Date()
    date_to = fields.Date()

    @api.onchange('date_from','date_to')
    def _check_only_month(self):
        if self.date_from and self.date_to:
            if self.date_from.month != self.date_to.month or self.date_from.year != self.date_to.year:
                raise ValidationError(_("Please choose the same month"))

    @api.onchange('evaluation_questions_type')
    def prepare_lines(self):
        if self.evaluation_questions_type:
            lines = []
            for qs in self.evaluation_questions_type.question_ids:
                qst = {
                'question_title':qs.question_title,
                'full_mark':qs.full_mark
                }
                lines.append((0,0,qst))
            self.line_ids = [(5,0,0)]
            self.write({'line_ids':lines})


    @api.depends('line_ids','contract_id')
    def _compute_perc(self):
        for rec in self:
            if rec.date_from and rec.date_to:
                if rec.date_from <= datetime.datetime.now().date() <= rec.date_to:
                    rec.other_month = False
                else:
                    rec.other_month = True

                if len(rec.line_ids) == 0:
                    rec.percentage = 100
                    pass
                total_mark = 0
                employee_got = 0
                for line in rec.line_ids:
                    total_mark += line.full_mark
                    employee_got += line.employee_mark
                rec.percentage = ( employee_got / total_mark) * 100 if employee_got > 0 else 0
                if rec.contract_id:
                    if rec.date_from and rec.date_to:
                        if rec.date_from <= datetime.datetime.now().date() <= rec.date_to:
                            rec.contract_id.survey_percentage = rec.percentage
            else:
                rec.other_month = True
    def compute_sheet_other_month(self):
        if self.contract_id:
            if self.date_from and self.date_to:
                self.contract_id.survey_percentage = self.percentage
    def clear_marks(self):
        for line in self.line_ids:
            line.employee_mark = 0

    # @api.constrains('contract_id')
    # def survey_id_constrains(self):
    #     if self.contract_id:
    #         same_contract_count = self.env['hr.employee.evaluation'].search_count([('contract_id','=',self.contract_id.id)])
    #         if same_contract_count > 1:
    #             raise ValidationError(_('Contract must be unique'))


    @api.depends('contract_id')
    def _set_name(self):
        for rec in self:
            if rec.contract_id:
                rec.name = rec.contract_id.employee_id.name + "'s Evaluation"
            else:
                rec.name = ''



class HREmployeesEvalutionQuestions(models.Model):
    _name = 'hr.employee.evaluation.questions'

    evaluation_id = fields.Many2one('hr.employee.evaluation')
    question_title = fields.Char(required=True)
    full_mark = fields.Float(required=True)
    employee_mark = fields.Float("Employee's Mark")

    @api.onchange('employee_mark','full_mark')
    def check_emploee_mark(self):
        if self.employee_mark > self.full_mark:
            raise ValidationError("the employee's mark cannot be greater than the full mark")
