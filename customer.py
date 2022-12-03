# build out customers table similar to type
import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma 

class Customers(db.Model):
  __tablename__ = 'Customers'
  customer_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = db.Column(db.String(), nullable=False, unique=True)
  phone = db.Column(db.String())
  address = db.Column(db.String())
  city = db.Column(db.String())
  state = db.Column(db.String())
  zip_code = db.Column(db.String())
  active = db.Column(db.Boolean(), default=True)

  jobs = db.relationship('Jobs', back_populates='customer', lazy=True)

  def __init__(self, name, phone, address, city, state, zip_code, active):
    self.name = name
    self.phone = phone
    self.address = address
    self.city = city
    self.state = state
    self.zip_code = zip_code
    self.active = active

class CustomersSchema(ma.Schema):
  
  class Meta:
    fields = ['customer_id', 'name', 'phone', 'address', 'city', 'state', 'zip_code', 'active']

customer_schema = CustomersSchema()
customers_schema = CustomersSchema( many=True )