from app.models.bus_stop import BusStop

def test_new_bus_stop():
    """
    GIVEN a BusStop model
    WHEN a new BusStop is created
    THEN check the stop name, latitude and longitude fields are defined correctly
    """
    bus_stop = BusStop('MSC',30.624153066, -96.35417108)
    assert bus_stop.stopname != None
    assert bus_stop.latitude != None
    assert bus_stop.longitude != None
    assert bus_stop.stopname == 'MSC'
    assert bus_stop.latitude == 30.624153066
    assert bus_stop.longitude == -96.35417108