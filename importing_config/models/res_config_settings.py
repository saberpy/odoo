# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models



class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    max_import_size = fields.Integer("Max Import Size (MB)",default=64)



    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('importing_config.max_import_size',self.max_import_size)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()

        max_import = self.env['ir.config_parameter'].sudo().get_param('importing_config.max_import_size')

        res.update({
            'max_import_size' : max_import,
        })

        return res
