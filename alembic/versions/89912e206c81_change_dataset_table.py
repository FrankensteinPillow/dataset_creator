"""change_dataset_table

Revision ID: 89912e206c81
Revises:
Create Date: 2021-08-23 17:17:06.279328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89912e206c81'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("datasets")
    op.create_table(
        "datasets",
        sa.Column(
            "id", sa.Integer, primary_key=True, autoincrement=True
        ),
        sa.Column("start_timestamp", sa.Text),
        sa.Column("end_timestamp", sa.Text),
        sa.Column("dataset_hash", sa.Text)
    )
    op.create_table(
        "datasets_to_sensors",
        sa.Column("dataset_id", sa.Integer),
        sa.Column("sensor_name", sa.Text),
        sa.Column("sensor_id", sa.Integer),
        sa.Column("timestamp", sa.Text)
    )


def downgrade():
    op.drop_table("datasets_to_sensors")
    op.drop_table("datasets")
    op.create_table("datasets",
        sa.Column("id", sa.Integer),
        sa.Column("start_timestamp", sa.Text),
        sa.Column("end_timestamp", sa.Text),
    )
