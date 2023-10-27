odoo.define('importing_config.basic_fields', function (require) {
"use strict";

var utils = require('web.utils');
var BasicFields = require('web.basic_fields').AbstractFieldBinary;
var rpc = require('web.rpc')


BasicFields.include({
    init: async function (parent, name, record) {
        this._super.apply(this, arguments);
        var importSize = await rpc.query({
            model: 'res.config.settings',
            method: 'get_values',
            args: [],
        }).then(function (res) {
            return res
        });
        this.fields = record.fields;
        this.useFileAPI = !!window.FileReader;
        this.max_upload_size = parseInt(importSize.max_import_size) * 1024 * 1024; // import from system parameter
        this.accepted_file_extensions = (this.nodeOptions && this.nodeOptions.accepted_file_extensions) || this.accepted_file_extensions || '*';
        if (!this.useFileAPI) {
            var self = this;
            this.fileupload_id = _.uniqueId('o_fileupload');
            $(window).on(this.fileupload_id, function () {
                var args = [].slice.call(arguments).slice(1);
                self.on_file_uploaded.apply(self, args);
            });
        }
    },
    
});


});
