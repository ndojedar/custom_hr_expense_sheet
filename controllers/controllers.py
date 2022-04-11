# -*- coding: utf-8 -*-
# from odoo import http


# class CustomHrExpenseSheet(http.Controller):
#     @http.route('/custom_hr_expense_sheet/custom_hr_expense_sheet/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_hr_expense_sheet/custom_hr_expense_sheet/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_hr_expense_sheet.listing', {
#             'root': '/custom_hr_expense_sheet/custom_hr_expense_sheet',
#             'objects': http.request.env['custom_hr_expense_sheet.custom_hr_expense_sheet'].search([]),
#         })

#     @http.route('/custom_hr_expense_sheet/custom_hr_expense_sheet/objects/<model("custom_hr_expense_sheet.custom_hr_expense_sheet"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_hr_expense_sheet.object', {
#             'object': obj
#         })
