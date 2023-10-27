from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import json
import datetime

# cardex wizard model


class CreatCardexWizard(models.TransientModel):
    _name = 'creat.cardex.wizard'
    _description = 'Create Criterion Date Wizard'

    criterion_date = fields.Date(default=fields.Datetime.now().date().replace(month=1, day=1), required=True)
    product_ids = fields.Many2one('product.product', required=True)
    # filter_pr=fields.Char()
    inv_location = fields.Many2one('stock.location', required=True)
    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    # pre_product_move=fields.Float(readonly=True,default=0)
    # add new view in reload exiting model, function

    def reload_move_line(self):
        fiscal_year_products = self.env['stock.move.line'].sudo().search(['&', '&', '&', '&', '|', '&', '&', '&', '&', 
                                                                          ('product_id', '=', self.product_ids.id),
                                                                          ('date', '>', self.criterion_date),
                                                                          ('date', '<', self.from_date),
                                                                          ('state', '=', 'done'),
                                                                          ('location_id', '=', self.inv_location.id),
                                                                          ('location_dest_id', '=', self.inv_location.id),
                                                                          ('product_id', '=', self.product_ids.id),
                                                                          ('date', '>', self.criterion_date),
                                                                          ('date', '<', self.from_date),
                                                                          ('state', '=', 'done')])

        sum_qty_in_fiscal = 0
        sum_unit_price_in_fiscal = 0.0
        for pr in fiscal_year_products:
            if pr.move_id.location_id == self.inv_location:
                sum_qty_in_fiscal -= pr.qty_done
                sum_unit_price_in_fiscal -= (pr.product_id.standard_price) * (pr.qty_done)
            elif pr.move_id.location_dest_id == self.inv_location:
                sum_qty_in_fiscal += pr.qty_done
                sum_unit_price_in_fiscal += (pr.product_id.standard_price) * (pr.qty_done)

        model_obj = self.env['ir.model.data']
        treeview_data_id = model_obj._get_id(
            'cardex_inventory', 'view_move_line_tree_reload')
        treeview_id = model_obj.browse(treeview_data_id).res_id
        formview_data_id = model_obj._get_id(
            'cardex_inventory', 'view_move_line_form_reload')
        formview_id = model_obj.browse(formview_data_id).res_id
        cardex_domain = ['&', '&', '&', '&', '|', '&', '&', '&', '&', 
                         ('product_id', '=', self.product_ids.id),
                         ('date', '>=', self.from_date),
                         ('date', '<=', self.to_date),
                         ('state', '=', 'done'),
                         ('location_id', '=', self.inv_location.id),
                         ('location_dest_id', '=', self.inv_location.id),
                         ('product_id', '=', self.product_ids.id),
                         ('date', '>=', self.from_date),
                         ('date', '<=', self.to_date),
                         ('state', '=', 'done')]

        cardex_product_moves = self.env['stock.move.line'].search(
            cardex_domain, order=('date'))

        for _move in cardex_product_moves:
            _move.sum_qty_done = sum_qty_in_fiscal
            _move.sum_price_unit = sum_unit_price_in_fiscal
            _move.price_rate = 0.0
            if _move.location_id.id == self.inv_location.id:
                _move.moves_in = ''
                _move.moves_out = 'OUT'
            elif _move.location_dest_id.id == self.inv_location.id:
                _move.moves_in = 'IN'
                _move.moves_out = ''            

        for index, obj in enumerate(cardex_product_moves):
            move_price = self.env['account.move'].sudo().search([('id','=',obj.move_id.account_move_ids.id)])
            previuos_move = cardex_product_moves[index-1]
            obj.price_rate = (move_price.amount_total / obj.qty_done)
            if obj.moves_in == 'IN':
                obj.sum_qty_done = obj.qty_done + previuos_move.sum_qty_done
                obj.sum_price_unit = move_price.amount_total if move_price else 0.0
            elif obj.moves_out == 'OUT':
                obj.sum_qty_done = previuos_move.sum_qty_done - obj.qty_done
                obj.sum_price_unit = move_price.amount_total if move_price else 0.0

        return {
            'type': 'ir.actions.act_window',
            'name': _('cardex'),
            'res_model': 'stock.move.line',
            'view_mode': 'tree,form',
            'view_type': 'tree',
            'views': [(treeview_id, 'list'), (formview_id, 'form')],
            'domain': cardex_domain,
            'context': {
                'inv_ctx': str(self.inv_location.complete_name),
                'sum_qty_in_fiscal': sum_qty_in_fiscal,
                'sum_price_unit_in_fiscal': sum_unit_price_in_fiscal,
                'product_count': len(cardex_product_moves),
            },
            'target': 'current',
        }
