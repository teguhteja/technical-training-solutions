from odoo import api, models, fields
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.')
    ]

    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    offer_amount = fields.Float()
    property_id = fields.Many2one('estate.property', string='Property')
    # property_id = fields.Many2one("estate.property", required=True)
    
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    create_date = fields.Datetime(string="Create Date", default=fields.Datetime.now)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else date.today()
            record.validity = (record.date_deadline - create_date).days if record.date_deadline else 0
            
    def action_accept_offer(self):
        for record in self:
            record.property_id.write({
                'buyer_id': record.partner_id.id,
                'selling_price': record.offer_amount,
                'state': 'sold'
            })
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True
