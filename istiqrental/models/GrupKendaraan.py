from odoo import fields, models, api


class GrupKendaraan(models.Model):
    _name = 'istiqrental.grupkendaraan'
    _description = 'Description'

    name = fields.Char(string='Nama Grup')
    kode_grup = fields.Char(
        string='Kode Grup',
        required=False)
    jml_unit = fields.Integer(
        string='Jml.Unit',
        required=False)
    total_unit = fields.Integer(
        string='Total Unit',
        required=False)
    kendaraan_ids = fields.One2many(
        comodel_name='istiqrental.kendaraan',
        inverse_name='grupkendaraan_id',
        string='Kendaraan',
        required=False)
    kendaraan_id = fields.Many2one(
        comodel_name='istiqrental.kendaraan',
        string='Kendaraan_id',
        required=False)
