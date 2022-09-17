from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Pengembalian(models.Model):
    _name = 'istiqrental.pengembalian'
    _description = 'Description'

    name = fields.Char(string='No Pengembalian')
    tgl_fakturkembali = fields.Date(default=fields.Date.today(),
        string='Tgl.Faktur Pengembalian',
        required=False)
    pengembaliandetail_ids = fields.One2many(
        comodel_name='istiqrental.pengembaliandetail',
        inverse_name='pengembalian_id',
        string='Pengembaliandetail_ids',
        required=False)
    sewadetail_ids = fields.One2many(
        comodel_name='istiqrental.sewadetail',
        inverse_name='pengembalian_id',
        string='Sewa Detail',
        required=False)

class PengembalianDetail(models.Model):
    _name = 'istiqrental.pengembaliandetail'
    _description = 'Pengembalian Detail'

    name = fields.Char(string='Pengembalian Detail')
    kendaraan_id = fields.Many2one(
        comodel_name='istiqrental.kendaraan',
        string='Nopol',
        required=False)
    detailkendaraan_id = fields.Many2one(
        comodel_name='istiqrental.detailkendaraan',
        string='Merek',
        required=False)
    biaya_denda = fields.Integer(compute='_onchange_biaya_denda',
        string='Biaya Denda',
        required=False)
    pengembalian_id = fields.Many2one(
        comodel_name='istiqrental.pengembalian',
        string='No.Pengembalian',
        required=False)
    sewadetail_id = fields.Many2one(
        comodel_name='istiqrental.sewadetail',
        string='Kode Sewa',
        required=False)
    tgl_selesai = fields.Date(
        string='Tgl.Selesai',
        required=False)
    tgl_kembali = fields.Date(
        string='Tgl.Kembali',
        required=False)
    tgl_sekarang = fields.Date(default=fields.Date.today(),
        string='Tgl_sekarang',
        required=True)

    jml_hari_keterlambatan = fields.Integer(compute='_compute_jml_hari_keterlambatan',
                                            string='Jml.Hari Keterlambatan',
                                            required=False)
    total_denda = fields.Integer(compute='_compute_total_denda',
                                 string='Total Denda',
                                 required=False)
    jml_unit = fields.Integer(
        string='Jml.Unit',
        required=False)

    @api.onchange('sewadetail_id')
    def _compute_tgl_selesai(self):
        self.tgl_selesai = self.sewadetail_id.tgl_selesai

    @api.depends('tgl_selesai', 'tgl_kembali')
    def _compute_jml_hari_keterlambatan(self):
        for record in self:
            if record.tgl_selesai and record.tgl_kembali:
                record.jml_hari_keterlambatan = (record.tgl_kembali - record.tgl_selesai).days
            else:
                record.jml_hari_keterlambatan = 0

    @api.onchange('kendaraan_id')
    def _onchange_biaya_denda(self):
        self.biaya_denda = self.kendaraan_id.biaya_denda

    @api.depends('jml_hari_keterlambatan', 'biaya_denda')
    def _compute_total_denda(self):
        for record in self:
            if record.jml_hari_keterlambatan <= 0:
                record.total_denda = 0
            else:
                record.total_denda = record.jml_hari_keterlambatan * record.biaya_denda
    @api.model
    def create(self, values):
        record = super(PengembalianDetail, self).create(values)
        if record.jml_unit:
            self.env['istiqrental.kendaraan'].search([('id', '=', record.kendaraan_id.id)]).write(
                {'banyak_unit': record.kendaraan_id.banyak_unit + record.jml_unit})
        return record

    @api.constrains('jml_unit')
    def _checkQuantity(self):
        for rec in self:
            if rec.jml_unit <= 0:
                raise ValidationError('Jumlah unit isi dengan 1')
            elif rec.jml_unit > 1:
                raise ValidationError('Jumlah unit isi dengan 1')

    @api.constrains('tgl_selesai', 'tgl_kembali')
    def _checkTimeRange(self):
        for rec in self:
            if rec.tgl_selesai > rec.tgl_kembali:
                raise ValidationError('Tanggal tidak berlaku')
            elif rec.tgl_kembali < rec.tgl_sekarang:
                raise ValidationError('Tanggal Tidak Berlaku')


