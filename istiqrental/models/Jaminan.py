from odoo import fields, models, api

class Jaminan(models.Model):
    _name = 'istiqrental.jaminan'
    _description = 'Description'

    name = fields.Char(string='Kode Jaminan')
    nama_jaminan = fields.Char(
        string='Nama Jaminan',
        required=False)
    jenis_jaminan = fields.Char(
        string='Jenis Jaminan',
        required=False)
    keterangan = fields.Char(
        string='Keterangan',
        required=False)
    sewadetail_ids = fields.One2many(
        comodel_name='istiqrental.sewadetail',
        inverse_name='jaminan_id',
        string='Sewa Detail',
        required=False)
    sewa_id = fields.Many2one(
        comodel_name='istiqrental.sewa',
        string='No Faktur Sewa',
        required=False)
    penyewa_id = fields.Many2one(
        comodel_name='istiqrental.penyewa',
        string='Penyewa',
        required=False)
