from db import db
import marshmallow as ma

association_table = db.Table(
  "InventoryJobAssociation",
  db.Model.metadata,
  db.Column('inventory_id', db.ForiegnKey('Inventory.inventory_id'), primary_key=True),
  db.Column('job_id', db.ForiegnKey('Jobs.job_id'), primary_key=True)
)