import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma
from type import TypesSchema

class Suppliers(db.Model):
  __tablename__ = 'Suppliers'
  supplier_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  type_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Types.type_id'), nullable = False)
  name = db.Column(db.String(), nullable=False)
  active = db.Column(db.Boolean(), default=True)
  # var name = db.relationship('pk table pulling from', back_populates='fk table')
  type = db.relationship('Types', back_populates='suppliers')

  products = db.relationship('Products', back_populates='supplier', lazy=True)

  def __init__(self, type_id, name, active):
    self.type_id = type_id
    self.name = name
    self.active = active

class SuppliersSchema(ma.Schema):

  class Meta:
    fields = ['supplier_id', 'name', 'type', 'active']

  type = ma.fields.Nested(TypesSchema(only=('type_id', 'category', 'size', 'active')))

supplier_schema = SuppliersSchema()
suppliers_schema = SuppliersSchema( many=True )