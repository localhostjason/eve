from ..db import db

tags = db.Table(
    'tags',
    db.Column('parent_id', db.Integer, db.ForeignKey('parent.id'), primary_key=True),
    db.Column('children_id', db.Integer, db.ForeignKey('children.id'), primary_key=True),
    db.Column('num', db.Integer)
)


class Parent(db.Model):
    name = db.Column(db.String(120))


class Children(db.Model):
    name = db.Column(db.String(120))

    # [].clear()
    parent = db.relationship('Parent', secondary=tags, lazy='subquery',
                             backref=db.backref('children', lazy='subquery'))
