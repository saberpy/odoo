from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # move_types = fields.Selection(selection=[('in','IN'),('out','OUT')], required=True)





