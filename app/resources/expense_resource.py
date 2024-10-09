from flask_restx import Resource, Namespace, fields
from utils.db import get_db

expense_ns = Namespace("expenses", description="Expense operations")

non_group_expense_model = expense_ns.model('non_group_expense', {
  'description': fields.String,
  'amount': fields.Float,
  'payor_id': fields.Integer,
  'payee_id': fields.Integer,
})

group_expense_model = expense_ns.model('group_expense', {
  'description': fields.String,
  'amount': fields.Float,
  'payor_id': fields.Integer,
  'group_id': fields.Integer,
})

@expense_ns.route('/non-group-expenses')
class AddNonGroupExpense(Resource):

  @expense_ns.expect(non_group_expense_model)
  def post(self):
    data = expense_ns.payload

    with get_db() as conn:
      with conn.cursor() as cur:
        cur.execute("""
          INSERT INTO "non_group_expense" (description, amount, payor_id, payee_id)
          VALUES (%s, %b, %b, %b)
          RETURNING id;
        """, (data['description'], data['amount'], data['payor_id'], data['payee_id']))
        non_group_expense_id = cur.fetchone()[0]
        conn.commit()
    
    return {'message': 'Expense created', 'non_group_expense_id': non_group_expense_id}, 201

@expense_ns.route('/group-expenses')
class AddGroupExpense(Resource):

  @expense_ns.expect(group_expense_model)
  def post(self):
    data = expense_ns.payload

    with get_db() as conn:
      with conn.cursor() as cur:
        cur.execute("""
          INSERT INTO "group_expense" (description, amount, payor_id, group_id)
          VALUES (%s, %b, %b, %b)
          RETURNING id;
        """, (data['description'], data['amount'], data['payor_id'], data['group_id']))
        group_expense_id = cur.fetchone()[0]
        conn.commit()
    
    return {'message': 'Expense created', 'group_expense_id': group_expense_id}, 201
