import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma
from supplier import SuppliersSchema

class Products(db.Model):
  __tablename__='Products'
  product_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = db.Column(db.String())
  upc = db.Column(db.String(), nullable=False, unique=True)
  supplier_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Suppliers.supplier_id'), nullable = False)
  active = db.Column(db.Boolean(), default=True)
  supplier = db.relationship('Suppliers', back_populates='products')

  inventory = db.relationship('Inventory', back_populates='products', lazy=True)

  def __init__(self, name, upc, supplier_id, active):
    self.name = name
    self.upc = upc
    self.supplier_id = supplier_id
    self.active = active

class ProductsSchema(ma.Schema):

  class Meta:
    fields = ['product_id','name', 'supplier', 'upc','active']
  
  supplier = ma.fields.Nested(SuppliersSchema())

product_schema = ProductsSchema()
products_schema = ProductsSchema( many=True )