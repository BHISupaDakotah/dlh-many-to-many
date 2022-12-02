from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from db import *
from sqlalchemy.exc import IntegrityError

from job import Jobs, job_schema, jobs_schema
from inventory import Inventory, inventory_schema, inventories_schema
from product import Products, product_schema, products_schema
from supplier import Suppliers, supplier_schema, suppliers_schema
from type import Types, type_schema, types_schema
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
  project_manager = post_data.get('project_manager')
  location = post_data.get('location')
  customer_id = post_data.get('customer_id')
  active = post_data.get('active')

  try:
    response = add_job(description, project_manager, location, customer_id, active)
    return response
  except IntegrityError:
    return jsonify('duplicated value for unique key'), 400

def add_job(description, project_manager, location, customer_id, active):
  new_job = Jobs(description, project_manager, location, customer_id, active)

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

  name = post_data.get('name')
  quantity = post_data('quantity')
  active = post_data('active')

  try: 
    response = add_inventory(name, quantity, active)
    return response
  except IntegrityError:
    return jsonify('duplicate value for unique key')

def add_inventory(name, quantity, active):
  new_inventory = Inventory(name, quantity, active)

  db.session.add(new_inventory)
  db.session.commit()

  return jsonify(inventory_schema(new_inventory)), 200

# get all
# _________ start with get all inventory then get all inventory etc _________
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

# _________ start with get all suppliers then get all suppliers etc _________

#----------/

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

if __name__ == '__main__':
  create_all()
  app.run(host='0.0.0.0', port="8089")
