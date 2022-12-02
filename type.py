import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma

class Types(db.Model):
  __tablename__ = 'Types'
  type_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  category = db.Column(db.String(), nullable=False)
  size = db.Column(db.String(), nullable=False, unique=True)
  active = db.Column(db.Boolean(), default=True)

  #var name = db.relationship('table going to', back_populates='var name on table going to') 
  suppliers = db.relationship('Suppliers', back_populates='type', lazy=True)

  def __init__(self, category, size, active):
    self.category = category
    self.size = size
    self.active = active

class TypesSchema(ma.Schema):

  class Meta:
    fields = ['type_id', 'category', 'size', 'active']

type_schema = TypesSchema()
types_schema = TypesSchema( many=True )