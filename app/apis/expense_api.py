from flask_restx import Resource, Namespace, fields
from psycopg.rows import dict_row
from psycopg import errors
from utils.db import get_db
from flask_jwt_extended import jwt_required, current_user

authorizations = {
  'jwt': {
    'type': 'apiKey',
    'in': 'header',
    'name': 'Authorization'
  }
}

expense_ns = Namespace("expenses", authorizations = authorizations, description="Expense operations")

non_group_expense_model = expense_ns.model('non_group_expense_model', {
  'description': fields.String,
  'amount': fields.Float,
  'payor_id': fields.Integer,
  'payee_id': fields.Integer
})

"""
group_expense_model = expense_ns.model('group_expense_model', {
  'description': fields.String,
  'amount': fields.Float,
  'payor_id': fields.Integer,
  'group_id': fields.Integer
})
"""

@expense_ns.route('/non-group-expenses')
class NonGroupExpense(Resource):

  method_decorators = [jwt_required()]

  @expense_ns.doc(security = "jwt", description = "Get non-group expenses for user.")
  @expense_ns.marshal_list_with(non_group_expense_model)
  def get(self):

    try:
      with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
          cur.execute(
            """
            SELECT description, amount, payor_id, payee_id
            FROM "non_group_expense"
            WHERE payor_id = %b OR payee_id = %b;
            """,
            (current_user['id'], current_user['id']))
          non_group_expenses = cur.fetchall()
          conn.commit()

      return non_group_expenses, 200
    
    except errors.DatabaseError as e:
      # Handle general database errors
      return {"message": "Database error occurred!", "error": str(e)}, 500

    except Exception as e:
      # Handle any other exceptions
      return {"message": "An error occurred!", "error": str(e)}, 500

  @expense_ns.doc(security = "jwt", description = "Add a non-group expense.")
  @expense_ns.expect(non_group_expense_model)
  @expense_ns.marshal_with(non_group_expense_model)
  def post(self):

    try:
      data = expense_ns.payload

      with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
          cur.execute(
            """
            INSERT INTO "non_group_expense" (description, amount, payor_id, payee_id)
            VALUES (%s, %b, %b, %b)
            RETURNING description, amount, payor_id, payee_id;
            """,
            (data['description'], data['amount'], data['payor_id'], data['payee_id']))
          non_group_expense = cur.fetchone()
          conn.commit()

      return non_group_expense, 201
  
    except errors.DatabaseError as e:
      # Handle general database errors
      return {"message": "Database error occurred!", "error": str(e)}, 500

    except Exception as e:
      # Handle any other exceptions
      return {"message": "An error occurred!", "error": str(e)}, 500

@expense_ns.route('/non-group-expenses/<int:id>')
class NonGroupExpensesByExpenseID(Resource):

  @expense_ns.expect(non_group_expense_model)
  @expense_ns.marshal_with(non_group_expense_model)
  def put(self, id):

    data = expense_ns.payload

    with get_db() as conn:
      with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
          """
          UPDATE "non_group_expense"
          SET description = %s, amount = %b, payor_id = %b, payee_id = %b
          WHERE id = %b
          RETURNING description, amount, payor_id, payee_id;
          """,
          (data['description'], data['amount'], data['payor_id'], data['payee_id'], id))
        non_group_expense = cur.fetchone()
        conn.commit()

    return non_group_expense, 201
  
  def delete(self, id):

    with get_db() as conn:
      with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
          """
          DELETE FROM "non_group_expense"
          WHERE id = %b;
          """,
          (id,))
        conn.commit()

    return "", 204
