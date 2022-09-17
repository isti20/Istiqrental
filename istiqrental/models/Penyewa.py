from odoo import fields, models, api

class Penyewa(models.Model):
    _name = 'istiqrental.penyewa'
    _description = 'Description'

    name = fields.Char(string='Kode Penyewa')
    nama_penyewa = fields.Char(
        string='Nama Penyewa',
        required=False)
    no_ktp = fields.Char(
        string='No.KTP',
        required=False)
    alamat = fields.Char(
        string='Alamat',
        required=False)
    no_tlp = fields.Char(
        string='No.Telepon',
        required=False)
    gender = fields.Selection(
        string='Gender',
        selection=[('male', 'Male'),
                   ('female', 'Female')],
        required=True)
        
    sewadetail_ids = fields.One2many(
        comodel_name='istiqrental.sewadetail',
        inverse_name='penyewa_id',
        string='Sewa Detail',
        required=False)
    kendaraan_id = fields.Many2one(
        comodel_name='istiqrental.kendaraan',
        string='No Faktur Sewa',
        required=False)
