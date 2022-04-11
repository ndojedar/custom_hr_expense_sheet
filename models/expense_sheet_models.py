# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CustomHrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    pre_pagado = fields.Boolean(
        string="PRE Pagado"
    )

    cost_expected = fields.Monetary(
        string="Expected cost"
    )

    ap_amount_total = fields.Monetary(
        string="Asiento Producción",
        compute="_get_ap_amount_total",
        readonly=True
    )
    
    gva_amount_total = fields.Monetary(
        string="Gasto VA",
        compute="_get_gva_amount_total",
        readonly=True
    )

    prod_estimado = fields.Monetary(
        string="Producción estimada", 
        compute="_calc_prod_estimado", 
        readonly=True
    )

    pva_estimado = fields.Monetary(
        string="Producción VA estimada", 
        compute="_calc_prodva_estimado", 
        readonly=True
    )

    ap_fecha = fields.Date(
        string="Fecha Producción",
        compute="_get_ap_fecha",
        readonly=True
    )

   
    def _get_ap_fecha(self):
        for rec in self:
            vdate = self.env['account.move'].search([
                ('move_type', '=', 'entry'), 
                ('expense_sheet_id', '=', rec.id)
            ])
            rec.ap_fecha = vdate.date if vdate else None
    
    
    def _get_ap_amount_total(self):
        for rec in self:
            val = 0.0
            vamount = self.env['account.move'].search([
                ('move_type', '=', 'entry'), 
                ('expense_sheet_id', '=', rec.id)
            ])
            rec.ap_amount_total = vamount.amount_total_signed if vamount else val


    def _get_gva_amount_total(self):
        for rec in self:
            val = 0.0
            if rec.project_id:
                if rec.ap_amount_total and rec.ap_amount_total > 0:
                    rec.gva_amount_total =  rec.ap_amount_total - rec.base_imponible
                else:
                    rec.gva_amount_total = val - rec.base_imponible
            else:
                rec.gva_amount_total = val


    def _calc_prod_estimado(self):
        for rec in self:
            val = 0.0
            vforecast = self.env['project.task'].search([('id', '=', rec.forecast_id.id)])
            if rec.forecast_id:
                rec.prod_estimado = rec.cost_expected * 1.5 * vforecast.sales_factor if vforecast else val
            else:
                rec.prod_estimado = val


    def _calc_prodva_estimado(self):
        for rec in self:
            val = 0.0
            if rec.forecast_id:
                if rec.prod_estimado and rec.prod_estimado > 0:
                    rec.pva_estimado = rec.prod_estimado - rec.cost_expected
                else:
                    rec.pva_estimado = val - rec.cost_expected
            else:
                rec.pva_estimado = val

    
    @api.constrains('cost_expected')
    def _validate_cost_expected(self):
        for rec in self:
            val = 0.0
            if rec.project_id or rec.travel_agency == True:
                if rec.cost_expected <= 0:
                    raise ValidationError(_('El valor de Expected cost debe ser mayor a cero.'))
            else:
                rec.cost_expected = val

