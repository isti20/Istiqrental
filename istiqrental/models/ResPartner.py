from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Description'

    is_admin = fields.Boolean(
        string='Admin',
        required=False)
    is_kasir = fields.Boolean(
        string='Kasir',
        required=False)
    no_ktp = fields.Char(
        string='No.KTP',
        required=False)
    gender = fields.Selection(
        string='Gender',
        selection=[('male', 'Male'),
                   ('female', 'Female')],
        required=True)
    status_pegawai = fields.Selection(
        string='Status Pegawai',
        selection=[('kontrak', 'Pegawai Kontrak'),
                   ('tetap', 'Pegawai Tetap'),
                   ('magang', 'Pegawai Magang')],
        required=False)