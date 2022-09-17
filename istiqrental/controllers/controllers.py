
from odoo import http, models, fields
from odoo.http import request
import json


class Istiqrental(http.Controller):
    @http.route('/istiqrental/get_kendaraan', auth='public', method=['GET'])
    def getKendaraan(self, **kw):
        Kendaraan = request.env['istiqrental.kendaraan'].search([])
        isi = []
        for rec in Kendaraan:
            isi.append({
                'name' : rec.name,
                'tipe_kendaraan' : rec.tipe_kendaraan,
                'kode_kendaraan' : rec.kode_kendaraan,
                'biaya_sewa' : rec.biaya_sewa,
                'biaya_denda' : rec.biaya_denda,
                'banyak_unit' : rec.banyak_unit
            })
        return json.dumps(isi)