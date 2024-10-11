from collections import defaultdict
from odoo import fields, models

class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'

    def _prepare_report_data(self):
        xml_id, data = super()._prepare_report_data()

        if self.picking_quantity == 'picking' and self.move_line_ids:
            qties = defaultdict(int)
            custom_barcodes = defaultdict(list)
            for line in self.move_line_ids:
                if line.product_id.barcode and line.move_id.product_qty:
                    if (line.lot_id or line.lot_name) and int(line.product_qty):
                        custom_barcodes[line.product_id.id].append((line.lot_id.name or line.lot_name, int(line.product_qty)))
                        continue
                    qties[line.product_id.id] += line.move_id.product_qty
            data['quantity_by_product'] = {p: int(q) for p, q in qties.items() if q}
            data['custom_barcodes'] = custom_barcodes
        return xml_id, data