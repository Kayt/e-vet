from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
question = Table('question', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('content', String, nullable=False),
    Column('number', String(length=100)),
    Column('name', String(length=100)),
    Column('farmer_id', Integer),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=80)),
    Column('email', String(length=120)),
    Column('region', String(length=100)),
    Column('password_hash', String(length=80)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['question'].columns['farmer_id'].create()
    post_meta.tables['question'].columns['name'].create()
    post_meta.tables['question'].columns['number'].create()
    post_meta.tables['user'].columns['region'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['question'].columns['farmer_id'].drop()
    post_meta.tables['question'].columns['name'].drop()
    post_meta.tables['question'].columns['number'].drop()
    post_meta.tables['user'].columns['region'].drop()
