
# We add custom fields in exiting model of stock that is stock.move.line from here

from random import randint
from odoo import models, api, fields
from odoo.exceptions import ValidationError
from datetime import datetime
import json


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"
    _order = 'date'

    moves_in = fields.Char()
    moves_out = fields.Char()

    # move_in=fields.Selection(selection=[('in','IN'),('','')],compute="_compute_move_in",string="IN")
    # move_out=fields.Selection(selection=[('out','OUT'),('','')],compute="_compute_move_out",string="OUT")

    doc_type = fields.Char(compute="_compute_doc_type", string="Document Type")
    # sum_qty_done = fields.Float(compute="_compute_sum_qty",
    #                                 string="Sum Qty"
    #                                 )
    sum_qty_done = fields.Float(default=0)
    sum_price_unit = fields.Float(string="Sum of Price Unit")
    price_rate = fields.Float()

    @api.depends('reference')
    def _compute_doc_type(self):
        for rec in self:
            if rec.picking_id.picking_type_id.name:
                rec.doc_type = rec.picking_id.picking_type_id.name
            else:
                rec.doc_type = ''

    # override search_read func for disable sorting in this model !
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):

        res = super(StockMoveLine, self.sudo()).search_read(
            domain, fields, offset, limit, order='date')
        return res

    # show wizard function
    def return_cardex_view(self):
        return {
            "name": "Creat Cardex",
            "type": "ir.actions.act_window",
            "res_model": "creat.cardex.wizard",
            "context": {},
            "view_mode": "form",
            "target": "new"
        }

    # ===========================================================================================================

    # function for add custom data in database for test :D !
    # def generate_demo_data(self):
    #     records=self.search([])
    #     for rec in records:
    #         if rec.qty_done==0:
    #             rec.qty_done=randint(50,200)
        # custom_records={
        #     'company_id':rec.company_id.id,
        #     'consume_line_ids':rec.consume_line_ids.ids,
        #     'date':rec.date,
        #     'description_picking':rec.description_picking,
        #     'display_name':rec.display_name,
        #     'doc_type':rec.doc_type,
        #     'location_dest_id':rec.location_dest_id.id,
        #     'location_id':rec.location_id.id,
        #     'lot_id':rec.lot_id.id,
        #     'owner_id':rec.owner_id.id,
        #     'package_id':rec.package_id.id,
        #     'package_level_id':rec.package_level_id.id,
        #     'picking_code':rec.picking_code,
        #     'picking_id':rec.picking_id.id,
        #     'picking_type_entire_packs':rec.picking_type_entire_packs,
        #     'picking_type_use_create_lots':rec.picking_type_use_create_lots,
        #     'picking_type_use_existing_lots':rec.picking_type_use_existing_lots,
        #     'produce_line_ids':rec.produce_line_ids.ids,
        #     'product_id':rec.product_id.id,
        #     'product_uom_category_id':rec.product_uom_category_id.id,
        #     'product_uom_id':rec.product_uom_id.id,
        #     'product_uom_qty':rec.rec.product_uom_qty,
        #     'qty_done':rec.qty_done,
        #     'reference':rec.reference,
        #     'state':rec.state,
        # }
        # self.create(custom_records)
