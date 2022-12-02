import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma

# from jobinventory import JobInventorySchema

class Inventory(db.Model):
  __tablename__='Inventory'
  inventory_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = db.Column(db.String(), nullable=False, unique=True)
  quantity = db.Column(db.Numeric(), default=0)
  # product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Job.job_id'), nullable=False)
  # quantity = db.relationship('JobInventory', back_populates='inventory')
  active = db.Column(db.Boolean(), default=True)
  

  def __init__(self, name, quantity, active):
    self.name = name
    self.quantity = quantity
    self.active = active

class InventorySchema(ma.Schema):

  class Meta: 
    fields = ['inventory_id','name', 'quantity', 'active']



inventory_schema = InventorySchema()
inventories_schema = InventorySchema( many=True )