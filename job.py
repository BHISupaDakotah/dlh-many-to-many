import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma
from customer import CustomersSchema
from jobinventoryxref import JobInventorySchema


class Jobs(db.Model):
  __tablename__ = 'Jobs'
  job_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  description = db.Column(db.String(), nullable = False, unique=True)
  location = db.Column(db.String(), nullable=False)
  customer_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Customers.customer_id'), nullable = False)
  active = db.Column(db.Boolean(), default=True)

  customer = db.relationship('Customers', back_populates='jobs')
  onsite_quantity = db.relationship('JobInventory', back_populates='jobs')

  def __init__(self, description, location, customer_id, active):
    
    self.description = description
    self.location = location
    self.customer_id = customer_id
    self.active = active


class JobsSchema(ma.Schema):
  class Meta:
    fields = ['job_id', 'description', 'location', 'customer', 'onsite_quantity', 'active']

  customer = ma.fields.Nested(CustomersSchema())  
  onsite_quantity = ma.fields.Nested(JobInventorySchema(), many=True )

job_schema = JobsSchema()
jobs_schema = JobsSchema( many=True )

# test