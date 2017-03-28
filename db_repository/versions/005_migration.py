from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
answers = Table('answers', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('content', VARCHAR, nullable=False),
    Column('session_id', VARCHAR, nullable=False),
)

surveys = Table('surveys', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['answers'].drop()
    pre_meta.tables['surveys'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['answers'].create()
    pre_meta.tables['surveys'].create()
