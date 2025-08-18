import sqlalchemy as sa

metadata = sa.MetaData()

users = sa.Table(
  "users", metadata,
  sa.Column("id", sa.Integer, primary_key=True, index=True),
  sa.Column("email", sa.String(255), unique=True, index=True),
  sa.Column("name", sa.String(255), index=True)
)

transactions  = sa.Table(
  "transactions", metadata,
  sa.Column("id", sa.Integer, primary_key=True, index=True),
  sa.Column("name", sa.String(255)),
  sa.Column("amount", sa.Float),
  sa.Column("method", sa.Integer, index=True),
  sa.Column("category", sa.Integer, index=True),
  sa.Column("date", sa.String(255)),
  sa.Column("user_id", sa.Integer, index=True),
)

expense_category = sa.Table(
  "expense_category", metadata,
  sa.Column("id", sa.Integer, primary_key=True, index=True),
  sa.Column("name", sa.String(255)),
  sa.Column("isActive", sa.Integer),
  sa.Column("user_id", sa.Integer, index=True),
)

accounts = sa.Table(
  "accounts", metadata,
  sa.Column("id", sa.Integer, primary_key=True, index=True),
  sa.Column("name", sa.String(255)),
  sa.Column("isActive", sa.Integer),
  sa.Column("user_id", sa.Integer, index=True)
)

subscriptions = sa.Table(
  "subscriptions", metadata,
  sa.Column("id", sa.Integer, primary_key=True, index=True),
  sa.Column("service", sa.String(255)),
  sa.Column("amount", sa.Float),
  sa.Column("frequency", sa.String(255)),
  sa.Column("start_date", sa.String(255)),
  sa.Column("user_id", sa.Integer, index=True),
)

savings = sa.Table(
  "savings", metadata,
  sa.Column("id", sa.Integer, primary_key=True, index=True),
  sa.Column("title", sa.String(255)),
  sa.Column("goal_amount", sa.Float),
  sa.Column("current_amount", sa.Float),
  sa.Column("cover", sa.String(255), nullable=True),
  sa.Column("finished", sa.Boolean),
  sa.Column("creation_date", sa.String(255)),
  sa.Column("user_id", sa.Integer, index=True),
)

savings_action = sa.Table(
  "savings_action", metadata,
  sa.Column("id", sa.Integer, primary_key=True, index=True),
  sa.Column("type", sa.String(255)),
  sa.Column("amount", sa.Float),
  sa.Column("date", sa.String(255)),
  sa.Column("goal_id", sa.Integer, index=True),
  sa.Column("user_id", sa.Integer, index=True),
)

budgets = sa.Table(
  "budgets", metadata,
  sa.Column("id", sa.Integer, primary_key=True, index=True),
  sa.Column("amount", sa.Float),
  sa.Column("user_id", sa.Integer, index=True),
  sa.Column("month", sa.String(255)),
)

budget_shares = sa.Table(
  "budget_shares", metadata,
  sa.Column("id", sa.Integer, primary_key=True, index=True),
  sa.Column("amount", sa.Float),
  sa.Column("budget_id", sa.Integer, index=True),
  sa.Column("category_id", sa.Integer, index=True),
)