import trafaret as t
from trafaret.contrib.object_id import MongoId

car = t.Dict({
    t.Key('_id'): MongoId(),
    t.Key('vin_code'): t.String(),
    t.Key('manufacturer'): t.String(),
    t.Key('model'): t.String(),
    t.Key('year_created'): t.Date(format='%Y'),
    t.Key('colour'): t.String(),
})


async def get_car_by_vin_code(car_collection, vin_code):
    car_detail = await car_collection.find_one({'vin_code': vin_code})
    return car_detail


async def delete_car_by_vin_code(car_collection, vin_code):
    car_detail = await car_collection.delete_one({'vin_code': vin_code})
    return car_detail
