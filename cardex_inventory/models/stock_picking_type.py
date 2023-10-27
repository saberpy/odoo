from odoo import models, api, fields

class PickingType(models.Model):
    _inherit = "stock.picking.type"

    

    type=fields.Selection(selection=[('in','IN'),('out','OUT')], required=True)