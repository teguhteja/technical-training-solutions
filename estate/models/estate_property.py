from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_compare

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = 'id desc'
    
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.'),
        ('unique_property_tag_name', 'UNIQUE(name)', 'The property tag name must be unique.')
    ]
    
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        required=True,
        default='new',
        copy=False
    )

    name = fields.Char(required=True, string="Property Name")
    expected_price = fields.Float(required=True, string="Expected Price")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    availability_date = fields.Date(default=lambda self: fields.Date.today() + timedelta(days=90), copy=False)
    
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    seller_id = fields.Many2one("res.users", string="Seller", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")


    living_area = fields.Float(string="Living Area")
    garden_area = fields.Float(string="Garden Area")
    total_area = fields.Float(string="Total Area", compute="_compute_total_area")

    @api.depends('living_area', 'garden_area', 'garden')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area * record.garden
            
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)
            
    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold property cannot be cancelled")
            record.state = 'cancelled'
        return True

    def action_set_sold_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled property cannot be sold")
            record.state = 'sold'
        return True
    
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_compare(record.selling_price, record.expected_price * 0.9, precision_rounding=0.01) == -1:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")