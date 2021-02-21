import aiohttp_jinja2
from aiohttp import web

from .db import car, get_car_by_vin_code, delete_car_by_vin_code
from .utils import check_input_form


class CarListView(web.View):
    @aiohttp_jinja2.template('cars.html')
    async def get(self):
        cars = await self.request.app['mongo'].car.find(
            self.request.rel_url.query).to_list(length=100)
        return {"cars": cars}


class CarDetailsView(web.View):
    @aiohttp_jinja2.template('car_details.html')
    async def get(self):
        car_detail = await get_car_by_vin_code(
            self.request.app['mongo'].car, self.request.match_info['vin_code'])
        if not car_detail:
            return web.HTTPNotFound()
        return {"car": car_detail}

    @aiohttp_jinja2.template('car_details.html')
    async def post(self):
        form = await self.request.post()

        car_detail = await get_car_by_vin_code(self.request.app['mongo'].car,
                                               self.request.match_info['vin_code'])
        if not car_detail:
            return web.HTTPNotFound()

        errors = check_input_form(car, form)
        if errors:
            return {'errors': errors, 'car': form}

        vin_code = form['vin_code']
        car_exists = (car_detail['vin_code'] != vin_code
                      and await get_car_by_vin_code(self.request.app['mongo'].car, vin_code))
        if car_exists:
            return {'errors': {'vin_code': 'Car with this code already exists.'}, 'car': form}

        await self.request.app['mongo'].car.replace_one({'_id': car_detail['_id']}, form)

        return web.HTTPFound(location='/')


class CarCreateView(web.View):
    @aiohttp_jinja2.template('add_car.html')
    async def get(self):
        return {"errors": {}, "form": None}

    @aiohttp_jinja2.template('add_car.html')
    async def post(self):
        form = await self.request.post()

        errors = check_input_form(car, form)
        if errors:
            return {'errors': errors, 'form': form}

        vin_code = form['vin_code']
        car_exists = await get_car_by_vin_code(self.request.app['mongo'].car, vin_code)
        if car_exists:
            return {'errors': {'vin_code': 'Car with this code already exists.'}, 'form': form}

        await self.request.app['mongo'].car.insert_one(
            {
                'vin_code': vin_code,
                'manufacturer': form['manufacturer'],
                'model': form['model'],
                'year_created': form['year_created'],
                'colour': form['colour']
            }
        )
        return web.HTTPFound(location='/')


class CarDeleteView(web.View):
    @aiohttp_jinja2.template('car_delete.html')
    async def get(self):
        car_detail = await get_car_by_vin_code(self.request.app['mongo'].car,
                                               self.request.match_info['vin_code'])
        if not car_detail:
            return web.HTTPNotFound()
        return {}

    @aiohttp_jinja2.template('car_delete.html')
    async def post(self):
        await delete_car_by_vin_code(self.request.app['mongo'].car,
                                     self.request.match_info['vin_code'])
        return web.HTTPFound(location='/')
