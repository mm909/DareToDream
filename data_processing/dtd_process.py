from dtd import DTD

if __name__ == '__main__':
    dtd = DTD()
    dtd.load_flight_data()
    dtd.change_col_names()

    dtd.simple_clean_data()
    dtd.simple_data_metrics()

    dtd.build_passenger_dict()
    dtd.create_passenger_column()

    dtd.build_flight_objective_dict()
    dtd.create_flight_objective_column()

    dtd.get_airport_location()
    dtd.create_distance_travlled_columns()

    dtd.save()