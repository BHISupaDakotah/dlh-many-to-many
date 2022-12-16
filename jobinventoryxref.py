import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma

from inventory import InventorySchema

class JobInventory(db.Model):
  __tablename__='JobInventory'
  inventory_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Inventory.inventory_id'), primary_key=True)
  job_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Jobs.job_id'), primary_key=True)
  onsite_quantity = db.Column(db.Numeric(), default=0)
  active = db.Column(db.Boolean(), default=True)

  jobs = db.relationship('Jobs', back_populates='onsite_quantity')
  inventory = db.relationship('Inventory', back_populates='onsite_quantity')

  def __init__(self, inventory_id, job_id, onsite_quantity, active):
    self.inventory_id = inventory_id
    self.job_id = job_id
    self.onsite_quantity = onsite_quantity
    self.active = active

class JobInventorySchema(ma.Schema):
  class Meta:
    fields = ['job_id', 'inventory_id', 'inventory','onsite_quantity', 'active']
  inventory = ma.fields.Nested(InventorySchema(), exclude=['inventory_id'])

jobinventory_schema = JobInventorySchema()
jobinventories_schema = JobInventorySchema( many=True )
