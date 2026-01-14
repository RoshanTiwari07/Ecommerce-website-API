from sqlalchemy.dialects import postgresql

# Reusable Postgres ENUM for shipment status
# create_type=False ensures Alembic/SA won't try to CREATE TYPE implicitly,
# you should explicitly create it in a migration with checkfirst=True once.
shipmentstatus_enum = postgresql.ENUM(
    'placed', 'processing', 'shipped', 'in_transit', 'out_for_delivery', 'delivered',
    name='shipmentstatus',
    create_type=False,
)
