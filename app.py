from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from db import *
from sqlalchemy.exc import IntegrityError

from job import Jobs, job_schema, jobs_schema
from inventory import Inventory, inventory_schema, inventories_schema
from product import Products, product_schema, products_schema
from supplier import Suppliers, supplier_schema, suppliers_schema
from type import Types, type_schema, types_schema
from customer import Customers, customer_schema, customers_schema
from jobinventoryxref import JobInventory, jobinventory_schema, jobinventories_schema

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://dakotahholmes@localhost:5432/manytomany"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app, db)
ma = Marshmallow(app)

def create_all():
  with app.app_context():
    print("creating tablers")
    db.create_all()
    print("all done")

def populate_object(obj, data_dictionary):
  fields = data_dictionary.keys()
  for field in fields:
    if getattr(obj, field):   # If the user object has the field 'field'...
        setattr(obj, field, data_dictionary[field])


# Job -------
# create
@app.route('/job/add', methods=['POST'])
def job_add():
  post_data = request.json
  if not post_data:
    post_data = request.form
  
  description = post_data.get('description')
  location = post_data.get('location')
  customer_id = post_data.get('customer_id')
  active = post_data.get('active')

  try:
    response = add_job(description, location, customer_id, active)
    return response
  except IntegrityError:
    return jsonify('duplicated value for unique key'), 400

def add_job(description, location, customer_id, active):
  new_job = Jobs(description, location, customer_id, active)

  db.session.add(new_job)

  db.session.commit()
  return jsonify(job_schema.dump(new_job)), 200

# read
@app.route('/jobs/get', methods=['GET'])
def get_all_active_jobs():
  jobs = db.session.query(Jobs).filter(Jobs.active == True).all()

  return jsonify(jobs_schema.dump(jobs)), 200

@app.route('/job/<job_id>', methods=['GET'])
def get_user_by_id(job_id):
  job = db.session.query(Jobs).filter(Jobs.job_id == job_id).first()

  return jsonify(job_schema.dump(job)), 200

# update
@app.route('/job/update/<job_id>', methods=['POST', 'PUT'])
def job_update(job_id):
  job = db.session.query(Jobs).filter(Jobs.job_id == job_id).first()

  if not job:
    return jsonify('sorry dude no job'), 404

  post_data = request.json
  if not post_data:
    post_data = request.form

  populate_object(job, post_data)

  db.session.commit()

  return jsonify(job_schema.dump(job)), 200

# delete
@app.route('/job/delete/<job_id>', methods=['GET'])
def delete_job(job_id):
  job = db.session.query(Jobs).filter(Jobs.job_id == job_id).first()

  db.session.delete(job)
  db.session.commit()

  return jsonify(job_schema.dump(job)), 201

# deactivate
@app.route('/job/deactivate/<job_id>', methods=['GET'])
def deactivate_job(job_id):
  job = db.session.query(Jobs).filter(Jobs.job_id == job_id).first()

  if not job:
    return(f'no user with {job_id}'), 404

  job.active = False
  db.session.commit()

  return jsonify(job_schema.dump(job)), 200

# activate
@app.route('/job/activate/<job_id>', methods=['GET'])
def activate_job(job_id):
  job = db.session.query(Jobs).filter(Jobs.job_id == job_id).first()

  if not job:
    return(f'no user with {job_id}'), 404

  job.active = True
  db.session.commit()

  return jsonify(job_schema.dump(job)), 200

#--------/
# Inventory --
# create
@app.route('/inventory/add', methods=['POST'])
def inventory_add():
  post_data = request.json
  if not post_data:
    post_data.form

  # inventory_quantity = post_data.get('inventory_quantity')
  product_id = post_data.get('product_id')
  active = post_data.get('active')

  try: 
    response = add_inventory(product_id, active)
    return response
  except IntegrityError:
    return jsonify('duplicate value for unique key')

def add_inventory(product_id, active):
  new_inventory = Inventory(product_id, active)

  db.session.add(new_inventory)
  db.session.commit()

  return jsonify(inventory_schema.dump(new_inventory)), 200

# read
@app.route('/inventories/get', methods=['GET'])
def get_all_active_inventories():
  inventories = db.session.query(Inventory).filter(Inventory.active == True).all()
  
  return(inventories_schema.dump(inventories)), 200

@app.route('/inventory/<inventory_id>')
def get_inventory_by_id(inventory_id):
  inventory = db.session.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()

  return jsonify(inventory_schema.dump(inventory)), 200
  

#update
@app.route('/inventory/update/<inventory_id>', methods=['POST', 'PUT'])
def inventory_update(inventory_id):
  inventory = db.session.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()

  if not inventory:
    return jsonify("sorry dude inventory"), 404
  
  post_data = request.json
  if not post_data:
    post_data.request.form

  populate_object(inventory, post_data)
  db.session.commit()

  return jsonify(inventory_schema.dump(inventory)), 200


#delete -- broken
@app.route('/inventory/delete/<inventory_id>', methods=['DELETE'])
def delete_inventory(inventory_id):
  inventory = db.session.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()

  db.session.delete(inventory)
  db.session.commit()

  return jsonify(inventory_schema.dump(inventory)), 200

#deactivate
@app.route('/inventory/deactivate/<inventory_id>', methods=['GET'])
def deactivate_inventory(inventory_id):
  inventory = db.session.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()

  if not inventory:
    return jsonify("no inventory with that id")

  inventory.active = False
  db.session.commit()
  return jsonify(inventory_schema.dump(inventory)), 200

#activate
@app.route('/inventory/activate/<inventory_id>', methods=['GET'])
def activate_inventory(inventory_id):
  inventory = db.session.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()

  if not inventory:
    return jsonify("no inventory with that id")

  inventory.active = True
  db.session.commit()
  return jsonify(inventory_schema.dump(inventory)), 200

#-------/

# Products --

# create
@app.route('/product/add' , methods=['POST'])
def product_add():
  post_data = request.json
  if not post_data:
    post_data = request.form
  
  name = post_data.get('name')
  upc = post_data.get('upc')
  supplier_id = post_data.get('supplier_id')
  active = post_data.get('active')

  try:
    response = add_product(name, upc, supplier_id, active)
    return response
  except IntegrityError:
    return jsonify('duplicate value for unique key'), 400

def add_product(name, upc, supplier_id, active):
  new_product = Products(name, upc, supplier_id, active)
  
  db.session.add(new_product)

  db.session.commit()
  return jsonify(product_schema.dump(new_product)), 200

# read
@app.route('/products/get', methods=['GET'])
def get_all_active_products():
  products = db.session.query(Products).filter(Products.active == True).all()

  return jsonify(products_schema.dump(products)), 200

@app.route('/product/<product_id>', methods=['GET'])
def get_product_by_id(product_id):
  product = db.session.query(Products).filter(Products.product_id == product_id).first()

  return jsonify(product_schema.dump(product)), 200

@app.route('/products/<material>', methods=['GET']) 
def get_product_by_material(material):
  product = db.session.query(Products).filter(Products.material.match(f'%{material}%')).all()

  return jsonify(products_schema.dump(product)), 200
#update
@app.route('/product/update/<product_id>', methods=['POST', 'PUT'])
def product_update(product_id):
  product = db.session.query(Products).filter(Products.product_id == product_id).first()

  if not product:
    return jsonify("sorry dude no product"), 404

  post_data = request.json
  if not post_data:
    post_data.request.form

  populate_object(product, post_data)
  db.session.commit()

  return jsonify(product_schema.dump(product)), 200

# delete
@app.route('/product/delete/<product_id>', methods=['GET'])
def delete_product(product_id):
  product = db.session.query(Products).filter(Products.product_id == product_id).first()

  db.session.delete(product)
  db.session.commit()

  return jsonify(product_schema.dump(product)), 201

# deactivate
@app.route('/product/deactivate/<product_id>', methods=['GET'])
def deactivate_product(product_id):
  product = db.session.query(Products).filter(Products.product_id == product_id).first()

  if not product:
    return(f'no product with {product_id}'), 404

  product.active = False
  db.session.commit()

  return jsonify(product_schema.dump(product)), 200

# activate
@app.route('/product/activate/<product_id>', methods=['GET'])
def activate_product(product_id):
  product = db.session.query(Products).filter(Products.product_id == product_id).first()

  if not product:
    return(f'no product with {product_id}'), 404

  product.active = True
  db.session.commit()

  return jsonify(product_schema.dump(product)), 200

#----------/
# -- Suppliers
# create
@app.route('/supplier/add', methods=['POST', 'PUT'])
def supplier_add():
  post_data = request.json
  if not post_data:
    post_data = request.form

  type_id = post_data.get('type_id')
  name = post_data.get('name')
  active = post_data.get('active')

  try:
    response = add_supplier(type_id, name, active)
    return response
  except IntegrityError:
    return jsonify('duplicated value for unique key'), 400

def add_supplier(type_id, name, active):
  new_supplier = Suppliers(type_id, name, active)

  db.session.add(new_supplier)

  db.session.commit()
  return jsonify(supplier_schema.dump(new_supplier)), 200

# update
@app.route('/supplier/update/<supplier_id>',  methods=['POST', 'PUT'])
def supplier_update(supplier_id):
  supplier = db.session.query(Suppliers).filter(Suppliers.supplier_id == supplier_id).first()

  if not supplier:
    return jsonify(f"supplier with id {supplier_id} not found") , 404

  post_data = request.json
  if not post_data:
    post_data = request.form

  populate_object(supplier, post_data)
  db.session.commit()

  return jsonify(supplier_schema.dump(supplier)), 200

# read
@app.route('/suppliers/get', methods=['GET'])
def get_all_active_suppliers():
  results = db.session.query(Suppliers).filter(Suppliers.active == True).all()
  
  if results:
    return jsonify(suppliers_schema.dump(results)), 200

  else:
    return jsonify("sorry no suppliers"), 404

@app.route('/supplier/<supplier_id>', methods=['GET'])
def get_supplier_by_id(supplier_id):
  result = db.session.query(Suppliers).filter(Suppliers.supplier_id == supplier_id).first()

  if not result:
    return jsonify("sorry no suppier by {supplier_id} ")

  else: 
    return jsonify(supplier_schema.dump(result)), 200

# delete
@app.route('/supplier/delete/<supplier_id>', methods=['GET'])
def delete_supplier(supplier_id):
  supplier = db.session.query(Suppliers).filter(Suppliers.supplier_id == supplier_id).first()
  
  db.session.delete(supplier)
  db.session.commit()
  return jsonify(supplier_schema.dump(supplier)), 201

# deactivate
@app.route('/supplier/deactivate/<supplier_id>', methods=['GET'])
def deactivate_supplier(supplier_id):
  supplier = db.session.query(Suppliers).filter(Suppliers.supplier_id == supplier_id).first()

  if not supplier:
    return(f'no supplier {supplier_id}'),404

  supplier.active = False
  db.session.commit()

  return jsonify(supplier_schema.dump(supplier)), 200
  
# activate
@app.route('/supplier/activate/<supplier_id>', methods=['GET'])
def activate_supplier(supplier_id):
  supplier = db.session.query(Suppliers).filter(Suppliers.supplier_id == supplier_id).first()

  if not supplier:
    return(f'no supplier {supplier_id}')

  supplier.active = True
  db.session.commit()

  return jsonify(supplier_schema.dump(supplier)), 200

#----------/
# -- Types
# create
@app.route('/type/add', methods=['POST','PUT'])
def type_add():
  post_data = request.json
  if not post_data:
    post_data = request.form
  
  category = post_data.get('category')
  size = post_data.get('size')
  active = post_data.get('active')

  try:
    response = add_type(category, size, active)
    return response
  except IndexError:
    return jsonify('duplcated value for unique key'),400

def add_type(category, type, active):
  new_type = Types(category, type, active)

  db.session.add(new_type)

  db.session.commit()

  return jsonify(type_schema.dump(new_type)), 200

# read
@app.route('/types/get', methods=['GET'])
def get_all_active_types():
  types = db.session.query(Types).filter(Types.active == True).all()

  return jsonify(types_schema.dump(types)), 200


@app.route('/type/<type_id>', methods=['GET'])
def get_type_by_id(type_id):
  type_result = db.session.query(Types).filter(Types.type_id == type_id).first()

  return jsonify(type_schema.dump(type_result)), 200


# update
@app.route('/type/update/<type_id>', methods=['POST','PUT'])
def type_update(type_id):
  type_result = db.session.query(Types).filter(Types.type_id == type_id).first()

  if not type_result:
    return("sorry dude no type")
  
  post_data = request.json
  if not post_data:
    post_data = request.form

  populate_object(type_result, post_data)
  db.session.commit()
  
  return jsonify(type_schema.dump(type_result))

# delete
@app.route('/type/delete/<type_id>', methods=['GET'])
def delete_type(type_id):
  type_result = db.session.query(Types).filter(Types.type_id == type_id).first()
  
  db.session.delete(type_result)
  db.session.commit()
  return jsonify(type_schema.dump(type_result)), 201

# deactivate
@app.route('/type/deactivate/<type_id>', methods=['GET'])
def deactivate_type(type_id):
  type_result = db.session.query(Types).filter(Types.type_id == type_id).first()

  if not type_result:
    return(f'no type with {type_id}'), 404

  type_result.active = False
  db.session.commit()

  return jsonify(type_schema.dump(type_result)), 200

# activate
@app.route('/type/activate/<type_id>')
def activate_type(type_id):
  type_result = db.session.query(Types).filter(Types.type_id == type_id).first()

  if not type_result:
    return(f'no type with {type_id}'), 404

  type_result.active = True
  db.session.commit()
  return jsonify(type_schema.dump(type_result))

#  --------/
# Customers
# create
@app.route('/customer/add', methods=['POST'])
def customer_add():
  post_data = request.json
  if not post_data:
    post_data = request.form

  name = post_data.get('name')
  phone = post_data.get('phone')
  address = post_data.get('address')
  city = post_data.get('city')
  state = post_data.get('state')
  zip_code = post_data.get('zip_code')
  active = post_data.get('active')

  try:
    response = add_customer(name, phone, address, city, state, zip_code, active)
    return response
  except IndexError:
    return jsonify('duplcated value for unique key'),400
  
def add_customer(name, phone, address, city, state, zip_code, active):
  new_customer = Customers(name, phone, address, city, state, zip_code, active)

  db.session.add(new_customer)
  db.session.commit()

  return jsonify(customer_schema.dump(new_customer)), 200

# read
@app.route('/customers/get', methods=['GET'])
def get_all_active_customers():
  customers = db.session.query(Customers).filter(Customers.active == True).all()

  return jsonify(customers_schema.dump(customers))

@app.route('/customer/<customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):
  customer = db.session.query(Customers).filter(Customers.customer_id == customer_id).first()

  return jsonify(customer_schema.dump(customer))

# update
@app.route('/customer/update/<customer_id>', methods=['POST','PUT'])
def update_customer(customer_id):
  customer = db.session.query(Customers).filter(Customers.customer_id == customer_id).first()

  if not customer:
    return("sorry dude no customer")
  
  post_data = request.json
  if not post_data:
    post_data = request.form

  populate_object(customer, post_data)
  db.session.commit()
  
  return jsonify(customer_schema.dump(customer))

# delete ???
@app.route('/customer/delete/<customer_id>', methods=['GET'])
def delete_customer(customer_id):
  customer = db.session.query(Customers).filter(Customers.customer_id == customer_id).first()

  db.session.delete(customer)
  db.session.commit()

  return jsonify(customer_schema.dump(customer)), 201
# deactivate
@app.route('/customer/deactivate/<customer_id>')
def deactivate_customer(customer_id):
  customer = db.session.query(Customers).filter(Customers.customer_id == customer_id).first()

  if not customer:
    return(f'no customer with id: {customer_id}'), 404

  customer.active = False
  db.session.commit()

  return jsonify(customer_schema.dump(customer)), 200

# activate
@app.route('/customer/activate/<customer_id>')
def activate_customer(customer_id):
  customer = db.session.query(Customers).filter(Customers.customer_id == customer_id).first()

  if not customer:
    return(f'no customer with id: {customer_id}'), 404

  customer.active = True
  db.session.commit()

  return jsonify(customer_schema.dump(customer)), 200
# --------/

# JobInventory
#create
@app.route('/jobinventory/add', methods=['POST'])
def jobinventory_add():
  post_data = request.json
  if not post_data:
    post_data = request.form

  inventory_id = post_data.get('inventory_id')
  job_id = post_data.get('job_id')
  onsite_quantity = post_data.get('onsite_quantity')
  active = post_data.get('active')


  try:
    response = add_jobinventory(inventory_id, job_id, onsite_quantity, active)
    return response
  except IndexError:
    return jsonify('duplcated value for unique key'), 400

def add_jobinventory(inventory_id, job_id,onsite_quantity, active):
  new_jobinventory = JobInventory(inventory_id, job_id, onsite_quantity, active)

  db.session.add(new_jobinventory)
  db.session.commit()

  return jsonify(jobinventory_schema.dump(new_jobinventory)), 200

# read
@app.route('/jobinventories/get')
def get_all_active_inventoryjobs():
  results = db.session.query(JobInventory).filter(JobInventory.active == True).all()

  return jsonify(jobinventories_schema.dump(results)), 200

@app.route('/jobinventory/<job_id>', methods=['GET'])
def get_inventory_by_job_id(job_id):
  job = db.session.query(JobInventory).filter(JobInventory.job_id == job_id).all()

  return jsonify(jobinventories_schema.dump(job))


#update
@app.route('/jobinventory/update/<inventory_id>', methods=['POST','PUT'])
def update_inventory(inventory_id):
  inventory = db.session.query(JobInventory).filter(JobInventory.inventory_id == inventory_id).first()

  if not inventory:
    return("sorry dude no inventory")

  post_data = request.json
  if not post_data:
    post_data = request.form
  
  populate_object(inventory, post_data)
  db.session.commit()

  return jsonify(jobinventory_schema.dump(inventory))

if __name__ == '__main__':
  create_all()
  app.run(host='0.0.0.0', port="8089")
