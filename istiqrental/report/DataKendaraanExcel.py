from odoo import models, fields


class DaftarKendaraanExcel(models.AbstractModel):
    _name = 'report.istiqrental.report_kendaraan_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    tgl_laporan = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, kendaraan):
        sheet = workbook.add_worksheet('Data Kendaraan')
        bold = workbook.add_format({'bold': True})
        italic = workbook.add_format({'italic': True})
        row = 1
        col = 0
        sheet.write(0, 0, str(self.tgl_laporan))
        sheet.write(row, col, 'Nopol Kendaraan', bold)
        sheet.write(row, col+1, 'Biaya sewa', bold)
        sheet.write(row, col+2, 'Banyak Unit', bold)
        for obj in kendaraan:
            row += 1
            col = 0
            sheet.write(row, col, obj.name)
            sheet.write(row, col+1, obj.biaya_sewa)
            sheet.write(row, col+2, obj.banyak_unit)
