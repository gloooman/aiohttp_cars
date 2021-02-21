from .views import (
    CarListView,
    CarDetailsView,
    CarCreateView,
    CarDeleteView
)


def setup_routes(app):
    app.router.add_view('/', CarListView, name='get_cars')
    app.router.add_view('/cars/create-car', CarCreateView, name='add_car')
    app.router.add_view('/cars/{vin_code}', CarDetailsView, name='car_details')
    app.router.add_view('/cars/{vin_code}/delete', CarDeleteView, name='delete_car')
