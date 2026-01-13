#!/usr/bin/env python3

import pytest
from app import app
from models import db, Bakery, BakedGood

@pytest.fixture(autouse=True)
def setup_db():
    """Set up the test database before each test."""
    with app.app_context():
        db.create_all()
        
        # Clear existing data
        BakedGood.query.delete()
        Bakery.query.delete()
        
        # Seed data
        bakeries = []
        bakeries.append(Bakery(name='Delightful donuts'))
        bakeries.append(Bakery(name='Incredible crullers'))
        db.session.add_all(bakeries)
        db.session.flush()
        
        baked_goods = []
        baked_goods.append(BakedGood(name='Chocolate dipped donut', price=2.75, bakery=bakeries[0]))
        baked_goods.append(BakedGood(name='Apple-spice filled donut', price=3.50, bakery=bakeries[0]))
        baked_goods.append(BakedGood(name='Glazed honey cruller', price=3.25, bakery=bakeries[1]))
        baked_goods.append(BakedGood(name='Chocolate cruller', price=3.40, bakery=bakeries[1]))
        
        db.session.add_all(baked_goods)
        db.session.commit()
        
        yield
        
        # Clean up after test
        db.session.remove()
        db.drop_all()

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))