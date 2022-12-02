import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma

# from jobinventory import JobInventorySchema

class Jobs(db.Model):
  __tablename__ = 'Jobs'
  job_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  description = db.Column(db.String(), nullable = False, unique=True)
  project_manager = db.Column(db.String())  # fk in future to users table user_id
  location = db.Column(db.String(), nullable=False)
  customer_id = db.Column(db.String()) #fk in future customer_id
  active = db.Column(db.Boolean(), default=True)

  # quantity = db.relationship('JobInventory', back_populates='job')

  def __init__(self, description, project_manager, location, customer_id, active):
    
    self.description = description
    self.project_manager = project_manager
    self.location = location
    self.customer_id = customer_id
    self.active = active


class JobsSchema(ma.Schema):
  class Meta:
    fields = ['job_id', 'description', 'project_manager', 'location', 'customer_id', 'quantity', 'active']
  # quantity = ma.fields.Nested( JobInventorySchema(), many=True)

job_schema = JobsSchema()
jobs_schema = JobsSchema( many=True )