from api.models.test import *
from api.models import *
from sqlalchemy import or_


def init_data():
    p = [Parent(name='p1'), Parent(name='p2')]
    c = [Children(name='c1'), Children(name='c2')]

    db.session.add_all(p)
    db.session.add_all(c)

    db.session.commit()


def add_tags():
    p1 = Parent.query.filter_by(name='p1').first()
    c = Children.query.filter(or_(Children.name == 'c1', Children.name == 'c2')).all()
    p1.children = c
    # p1.children.append(Children(name='c3'))
    # print(p1.children)
    db.session.add(p1)

    db.session.commit()


def add_tags_2():
    c1 = Children.query.filter_by(name='c1').first()
    p = Parent.query.filter(or_(Parent.name == 'p1', Parent.name == 'p2')).all()
    c1.parent = p
    # p1.children.append(Children(name='c3'))
    # print(p1.children)
    db.session.add(c1)

    db.session.commit()


def delete_tags():
    p1 = Parent.query.filter_by(name='p1').first()
    print(p1.children)
    p1.children.clear()
    # print(p1.children)
    # db.session.delete(p1)
    db.session.commit()


def test():
    user = User.query.get(0)
    print(user)
    print(user.users)


if __name__ == '__main__':
    # init_data()
    # add_tags()
    # delete_tags()
    pass
    test()
