"""empty message

Revision ID: dbe751272e8b
Revises: 
Create Date: 2018-01-13 16:54:50.708421

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbe751272e8b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Switch')
    op.drop_table('Node')
    op.drop_table('Firewall')
    op.drop_table('Regenerator')
    op.drop_table('Optical channel')
    op.drop_table('Antenna')
    op.drop_table('Optical link')
    op.drop_table('Ethernet link')
    op.drop_table('NapalmConfigTask')
    op.drop_table('User')
    op.drop_table('Host')
    op.drop_table('NapalmGettersTask')
    op.drop_table('Script')
    op.drop_table('Optical switch')
    op.drop_table('Server')
    op.drop_table('NetmikoTask')
    op.drop_table('BGP peering')
    op.drop_table('Task')
    op.drop_table('Router')
    op.drop_table('Pseudowire')
    op.drop_table('Etherchannel')
    op.drop_table('Link')
    op.drop_table('Object')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Object',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=120), nullable=True),
    sa.Column('description', sa.VARCHAR(), nullable=True),
    sa.Column('location', sa.VARCHAR(), nullable=True),
    sa.Column('vendor', sa.VARCHAR(length=120), nullable=True),
    sa.Column('type', sa.VARCHAR(length=50), nullable=True),
    sa.Column('visible', sa.BOOLEAN(), nullable=True),
    sa.CheckConstraint('visible IN (0, 1)'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Link',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('source_id', sa.INTEGER(), nullable=False),
    sa.Column('destination_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['destination_id'], ['Node.id'], ),
    sa.ForeignKeyConstraint(['id'], ['Object.id'], ),
    sa.ForeignKeyConstraint(['source_id'], ['Node.id'], ),
    sa.PrimaryKeyConstraint('id', 'source_id', 'destination_id')
    )
    op.create_table('Etherchannel',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['Link.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Pseudowire',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['Link.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Router',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['Node.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Task',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('type', sa.VARCHAR(), nullable=True),
    sa.Column('recurrent', sa.BOOLEAN(), nullable=True),
    sa.Column('name', sa.VARCHAR(length=120), nullable=True),
    sa.Column('status', sa.VARCHAR(), nullable=True),
    sa.Column('creation_time', sa.INTEGER(), nullable=True),
    sa.Column('logs', sa.BLOB(), nullable=True),
    sa.Column('nodes', sa.BLOB(), nullable=True),
    sa.Column('frequency', sa.VARCHAR(length=120), nullable=True),
    sa.Column('scheduled_date', sa.VARCHAR(), nullable=True),
    sa.Column('creator', sa.VARCHAR(), nullable=True),
    sa.CheckConstraint('recurrent IN (0, 1)'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('BGP peering',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['Link.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('NetmikoTask',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('script', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['Task.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Server',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['Node.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Optical switch',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['Node.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Script',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=120), nullable=True),
    sa.Column('type', sa.VARCHAR(length=50), nullable=True),
    sa.Column('content', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('NapalmGettersTask',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('script', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['Task.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Host',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['Node.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('User',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=120), nullable=True),
    sa.Column('email', sa.VARCHAR(length=120), nullable=True),
    sa.Column('access_rights', sa.VARCHAR(length=120), nullable=True),
    sa.Column('password', sa.VARCHAR(length=30), nullable=True),
    sa.Column('secret_password', sa.VARCHAR(length=30), nullable=True),
    sa.Column('dashboard_node_properties', sa.VARCHAR(), nullable=True),
    sa.Column('dashboard_link_properties', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('NapalmConfigTask',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('script', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['Task.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Ethernet link',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['Link.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Optical link',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['Link.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Antenna',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['Node.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Optical channel',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['Link.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Regenerator',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['Node.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Firewall',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['Node.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Node',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('operating_system', sa.VARCHAR(length=120), nullable=True),
    sa.Column('os_version', sa.VARCHAR(length=120), nullable=True),
    sa.Column('ip_address', sa.VARCHAR(length=120), nullable=True),
    sa.Column('longitude', sa.FLOAT(), nullable=True),
    sa.Column('latitude', sa.FLOAT(), nullable=True),
    sa.Column('secret_password', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['Object.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Switch',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['Node.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
