from odoo import fields, models, api


class Kendaraan(models.Model):
    _name = 'istiqrental.kendaraan'
    _description = 'Description'

    name = fields.Char(string='Nopol')
    tipe_kendaraan = fields.Char(
        string='Tipe Kendaraan',
        required=False)
    kode_kendaraan = fields.Char(
        string='Kode Kendaraan',
        required=False)
    detailkendaraan_id = fields.Many2one(
        comodel_name='istiqrental.detailkendaraan',
        string='Merek',
        required=False)
    biaya_sewa = fields.Integer(
        string='Biaya Sewa',
        required=False)
    biaya_denda = fields.Integer(
        string='Biaya Denda',
        required=False)
    sewa_id = fields.Many2one(
        comodel_name='istiqrental.sewa',
        string='Kode Sewa',
        required=False)
    banyak_unit = fields.Integer(
        string='Jml.Unit',
        required=False)
    detailkendaraan_ids = fields.One2many(
        comodel_name='istiqrental.detailkendaraan',
        inverse_name='kendaraan_id',
        string='Detail Kendaraan',
        required=False)
    grupkendaraan_id = fields.Many2one(
        comodel_name='istiqrental.grupkendaraan',
        string='Nama Grup',
        required=False)
    detailkendaraan_ids = fields.Many2many(
        comodel_name='istiqrental.detailkendaraan',
        string='Detail Kendaraan ids')

    @api.onchange('grupkendaraan_id','kode_grup')
    def onchange_grup_kendaraan(self):
        if (self.grupkendaraan_id.kode_grup):
            self.kode_kendaraan = str(self.grupkendaraan_id.kode_grup) + ' ' + str(self.tipe_kendaraan)
        else:
            self.kode_kendaraan = " "

    # _sql_constraints = [
    #     ('nopol_unik','unique(name)','Nopol Harus Unik')
    # ]

class DetailKendaraan(models.Model):
    _name = 'istiqrental.detailkendaraan'
    _description = 'DetailKendaraan'

    name = fields.Char(string='Merek')
    satuan = fields.Char(
        string='Satuan', 
        required=False)
    no_mesin = fields.Char(
        string='No Mesin',
        required=False)
    kapasitas = fields.Integer(
        string='Kapasitas Penumpang',
        required=False)
    kendaraan_id = fields.Many2one(
        comodel_name='istiqrental.kendaraan',
        string='Nopol',
        required=False)
    sewa_id = fields.Many2one(
        comodel_name='istiqrental.sewa',
        string='Kode Sewa',
        required=False)
    kendaraan_ids = fields.Many2many(
        comodel_name='istiqrental.kendaraan',
        string='Kendaraan ids')