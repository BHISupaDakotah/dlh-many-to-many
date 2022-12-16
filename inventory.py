import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma
from product import ProductsSchema

class Inventory(db.Model):
  __tablename__='Inventory'
  inventory_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Products.product_id'), nullable=False)
  active = db.Column(db.Boolean(), default=True)

  products = db.relationship('Products', back_populates='inventory')
  onsite_quantity = db.relationship('JobInventory', back_populates='inventory')

  def __init__(self, product_id, active):
    self.product_id = product_id
    self.active = active

class InventorySchema(ma.Schema):

  class Meta: 
    fields = ['inventory_id', 'products','active']

  products = ma.fields.Nested(ProductsSchema())


inventory_schema = InventorySchema()
inventories_schema = InventorySchema( many=True )