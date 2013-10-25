import common

from sqlalchemy import Column, ForeignKey, String, Table

parent_relationship_table = Table('parent_relationships', common.Base.metadata,
    Column('child_hash', String, ForeignKey('commits.hash')),
    Column('parent_hash', String, ForeignKey('commits.hash')))
