"""partition

Revision ID: 62e0c03078dd
Revises:
Create Date: 2023-04-28 17:53:39.841688

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "62e0c03078dd"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password", sa.Text(), nullable=False),
        sa.Column("name", sa.String(length=155), nullable=True),
        sa.Column("verified", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("id"),
    )
    op.create_table(
        "users_roles",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=55), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "social_account",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("social_id", sa.Text(), nullable=False),
        sa.Column("social_name", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("social_id", "social_name", name="social_pk"),
    )
    op.create_table(
        "users_login_history",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("user_agent", sa.Text(), nullable=False),
        sa.Column("authentication_date", sa.DateTime(), nullable=True),
        sa.Column("device_type", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", "device_type"),
        sa.UniqueConstraint("id", "device_type"),
        postgresql_partition_by="LIST (device_type)",
    )
    op.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_desktop" PARTITION OF "users_login_history" FOR VALUES IN ('desktop')"""
    )
    op.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_tablet" PARTITION OF "users_login_history" FOR VALUES IN ('tablet')"""
    )
    op.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_mobile" PARTITION OF "users_login_history" FOR VALUES IN ('mobile')"""
    )
    op.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_bot" PARTITION OF "users_login_history" FOR VALUES IN ('bot')"""
    )
    op.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_unknown" PARTITION OF "users_login_history" FOR VALUES IN ('unknown')"""
    )
    op.create_table(
        "users_service",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("role_id", sa.UUID(), nullable=False),
        sa.Column("date_joined", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["role_id"], ["users_roles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users_service")
    op.drop_table("users_login_history")
    op.drop_table("social_account")
    op.drop_table("users_roles")
    op.drop_table("users")
    # ### end Alembic commands ###
