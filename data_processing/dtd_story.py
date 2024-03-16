from dtd import DTD

if __name__ == "__main__":
    dtd = DTD.load(reload_config=True)
    dtd.date_flight_metrics()
    dtd.aircraft_metrics()
    dtd.airport_metrics()
    dtd.hours_metrics()
    dtd.passenger_metrics()
    dtd.objective_metrics()
    dtd.distance_metrics()
    dtd.save()