# use this style of table when additonal information is needed on an association table

import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma

from inventory import InventorySchema

class JobInventory(db.Model):
  __tablename__ = 'JobInventory'
  job_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Jobs.job_id'), primary_key=True)
  inventory_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Inventory.inventory_id'), primary_key=True)
  quantity = db.Column(db.Numeric(), primary_key=True)

  job = db.relationship('Jobs', back_populates='quantity')
  inventory = db.relationship('Inventory', back_populates='quantity')

  def __init__(self, job_id, inventory_id, quantity):
    self.job_id = job_id
    self.inventory_id = inventory_id
    self.quantity = quantity

class JobInventorySchema(ma.Schema):
  class Meta:
    fields = ['inventory', 'job_id', 'quantity']
  inventory = ma.fields.Nested(InventorySchema())

jobiventory_schema = JobInventorySchema()
jobinventories_schema = JobInventorySchema( many=True )