from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Sewa(models.Model):
    _name = 'istiqrental.sewa'
    _description = 'Description'

    name = fields.Char(string='Kode Sewa')
    tgl_sewa = fields.Date(default=fields.Date.today(),
        string='Tgl.Sewa',
        required=False)
    penyewa_id = fields.Many2one(
        comodel_name='istiqrental.penyewa',
        string='Kode Penyewa',
        required=False)
    gender = fields.Selection(
        string='Gender',
        selection=[('male', 'Male'),
                   ('female', 'Female')],
        required=False)
    kendaraan_id = fields.Many2one(
        comodel_name='istiqrental.kendaraan',
        string='Kendaraan_id',
        required=False)
    sewadetail_ids = fields.One2many(
        comodel_name='istiqrental.sewadetail',
        inverse_name='sewa_id',
        string='Sewadetail_ids',
        required=False)
    pengembalian_id = fields.Many2one(
        comodel_name='istiqrental.pengembalian',
        string='Pengembalian_id',
        required=False)
    total_bayar = fields.Integer(compute='_compute_total_bayar',
        string='Total Pembayaran',
        required=False)
    jaminan_id = fields.Many2one(
        comodel_name='istiqrental.jaminan',
        string='Kode Jaminan',
        required=False)
    jaminan_ids = fields.One2many(
        comodel_name='istiqrental.jaminan',
        inverse_name='sewa_id',
        string='Jaminan ids',
        required=False)

    @api.onchange('penyewa_id')
    def onchange_penyewa(self):
        if self.penyewa_id.gender:
            self.gender = self.penyewa_id.gender
        else:
            self.gender = ''

    @api.depends('sewadetail_ids')
    def _compute_total_bayar(self):
        for rec in self:
            a = sum(self.env['istiqrental.sewadetail'].search([('sewa_id', '=', rec.id)]).mapped('subtotal'))
            rec.total_bayar = a

    def unlink(self):
        if self.sewadetail_ids:
            a=[]
            for rec in self:
                a = self.env['istiqrental.sewadetail'].search([('sewa_id', '=', rec.id)])
                print(a)
                for i in a:
                    print(str(i.kendaraan_id.name) + '' + str(i.jml_unit))
                    i.kendaraan_id.banyak_unit += i.jml_unit
            record = super(Sewa, self).unlink()

    def write(self, values):
        for rec in self:
            a = self.env['istiqrental.sewadetail'].search([('sewa_id', '=', rec.id)])
            print(a)
            for data in a:
                print(str(data.kendaraan_id.name) + " " + str(data.jml_unit) + ' ' + str(data.kendaraan_id.banyak_unit))
                data.kendaraan_id.banyak_unit = data.kendaraan_id.banyak_unit + data.jml_unit
        record = super(Sewa, self).write(values)
        for rec in self:
            b = self.env['istiqrental.sewadetail'].search([('sewa_id', '=', rec.id)])
            print(a)
            print(b)
            for databaru in b:
                if databaru in a:
                    print(str(databaru.kendaraan_id.name) + " " + str(databaru.jml_unit) + " " + str(databaru.kendaraan_id.banyak_unit))
                    databaru.kendaraan_id.banyak_unit -= databaru.jml_unit
                else:
                    pass
        return record

    state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'),
                   ('confirm', 'Confirm'),
                   ('cancel', 'Cancel'),
                   ('done', 'done')
                   ],
        required=False, default='draft')

    def action_confirm(self):
        self.write({'state': 'confirm'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_draft(self):
        self.write({'state': 'draft'})

    # _sql_constraints = [
    #     ('no_faktur_sewa_unik','unique(name)','No Faktur Sewa Harus unik')
    # ]


class SewaDetail(models.Model):
    _name = 'istiqrental.sewadetail'
    _description = 'Sewa Detail'
    _rec_name = 'sewa_id'

    name = fields.Char(string='Nama')
    sewa_id = fields.Many2one(
        comodel_name='istiqrental.sewa',
        string='Kode Sewa',
        required=False)
    satuan = fields.Char(
        string='Satuan',
        required=False)
    kendaraan_id = fields.Many2one(
        comodel_name='istiqrental.kendaraan',
        string='Nopol',
        required=False)
    biaya_sewa = fields.Integer(compute='_compute_biaya_sewa',
        string='Biaya Sewa',
        required=False)
    tgl_mulai = fields.Date(
        string='Tgl.Mulai',
        required=False)
    tgl_selesai = fields.Date(
        string='Tgl.Selesai',
        required=False)
    tgl_sekarang = fields.Date(default=fields.Date.today(),
        string='Tgl.Sekarang',
        required=True)
    detailkendaraan_id = fields.Many2one(
        comodel_name='istiqrental.detailkendaraan',
        string='Merek',
        required=False)
    jml_unit = fields.Integer(
        string='Jml.Unit',
        required=True)
    subtotal = fields.Integer(compute='_compute_subtotal',
        string='Subtotal',
        required=False)
    pengembalian_id = fields.Many2one(
        comodel_name='istiqrental.pengembalian',
        string='Pengembalian',
        required=False)
    jml_hari = fields.Integer(compute='_compute_jml_hari',
                              string='Jml.Hari',
                              required=False)
    penyewa_id = fields.Many2one(
        comodel_name='istiqrental.penyewa',
        string='Penyewa',
        required=False)
    jaminan_id = fields.Many2one(
        comodel_name='istiqrental.jaminan',
        string='Kode Jaminan',
        required=False)

    @api.constrains('tgl_mulai','tgl_selesai')
    def _checkTimeRange(self):
        for rec in self:
            if rec.tgl_selesai < rec.tgl_mulai:
                raise ValidationError('Tanggal selesai tidak berlaku')
            elif rec.tgl_mulai < rec.tgl_sekarang:
                raise ValidationError('Tanggal mulai tidak berlaku')

    @api.depends('tgl_mulai', 'tgl_selesai')
    def _compute_jml_hari(self):
        for record in self:
            if record.tgl_mulai and record.tgl_selesai:
                record.jml_hari = (record.tgl_selesai - record.tgl_mulai).days
            else:
                record.jml_hari = 0

    @api.onchange('kendaraan_id')
    def _compute_biaya_sewa(self):
        self.biaya_sewa = self.kendaraan_id.biaya_sewa


    @api.depends('jml_hari', 'biaya_sewa')
    def _compute_subtotal(self):
        for record in self:
            if record.jml_hari <= 0:
                record.subtotal = record.biaya_sewa
            else:
                record.subtotal = record.jml_hari * record.biaya_sewa * record.jml_unit

    @api.model
    def create(self, values):
        record = super(SewaDetail, self).create(values)
        if record.jml_unit:
            self.env['istiqrental.kendaraan'].search([('id', '=', record.kendaraan_id.id)]).write(
                {'banyak_unit': record.kendaraan_id.banyak_unit - record.jml_unit})
        return record

    @api.constrains('jml_unit')
    def _checkQuantity(self):
        for rec in self:
            if rec.jml_unit <= 0:
                raise ValidationError('Jumlah unit isi dengan 1')
            elif rec.jml_unit > 1:
                raise ValidationError('Jumlah unit isi dengan 1')