import re
import os
import json
import pickle
import pandas as pd
import airportsdata
from dtd_config import dtd_config
from dtd_utils import airport_distance, CustomEncoder

class DTD:
    def __init__(self, config=None) -> None:
        self.config = config if config else dtd_config
        self.passenger_names = {}
        self.flight_objectives = {}
        self.airport_data = {}
        self.report = {}
        return

    def load_flight_data(self) -> None:
        path = self.config['data_path']
        self.data = pd.read_csv(path)
        return
    
    def change_col_names(self) -> None:

        # Initial Cols
        # 'Date', 
        # 'Aircraft Make and Model', 'Aircraft Ident.', 
        # 'Departure', 'Arrival', 'Arrival 2', 'Arrival 3', 
        # 'ASEL', 'AMEL', 
        # 'Day', 'Night',
        # 'PIC', 'Solo', 'Cross Country', 'Simulated', 'Actual', 'Ground Trainer',
        # 'Duel Recieved', 'Basic Given', 'Advanced Given', 
        # 'Day.1', 'Night.1', 'Approaches', 
        # 'Memo',
        # 'Complex', 'High Preformance', 'TAA', 
        # 'M20R', 'M20V', 'PA24-250', 'PA24-180', 'PA28-140', 'PA28-160', 'PA28-180', 'PA28-181', 'DA-40', 'C172', 'C172 XP', 'C177', 'C150', 'C152', 'C182', 'C175', 'C210', 'PA44-180', 'RV-8', 'LNCE', 'AC11'

        # Replace spaces with underscores
        self.data.columns = self.data.columns.str.replace(' ', '_')

        # Rename Columns
        new_col_names = {
            'Date': 'date',
            'Aircraft_Make_and_Model': 'aircraft_make_model',
            'Aircraft_Ident.': 'aircraft_id',
            'Departure': 'departure',
            'Arrival': 'arrival_1',
            'Arrival_2': 'arrival_2',
            'Arrival_3': 'arrival_3',
            'Day': 'day',
            'Night': 'night',
            'PIC': 'PIC',
            'Solo': 'solo',
            'Cross_Country': 'cross_country',
            'Simulated': 'instrument_simulated',
            'Actual': 'instrument_actual',
            'Ground_Trainer': 'ground_trainer',
            'Duel_Recieved': 'duel_received',
            'Basic_Given': 'basic_given',
            'Advanced_Given': 'advanced_given',
            'Day.1': 'day_landings',
            'Night.1': 'night_landings',
            'Approaches': 'approaches',
            'Memo': 'memo',
            'Complex': 'complex_systems',
            'High_Preformance': 'high_performance_systems',
            'TAA': 'TAA_systems',
        }
        self.data.rename(columns=new_col_names, inplace=True)

        return

    def simple_clean_data(self) -> None:
        self.data['departure'] = self.data['departure'].str.strip()
        self.data['arrival_1'] = self.data['arrival_1'].str.strip()
        self.data['arrival_2'] = self.data['arrival_2'].str.strip()
        self.data['arrival_3'] = self.data['arrival_3'].str.strip()
        self.data['aircraft_make_model'] = self.data['aircraft_make_model'].str.strip()
        self.data['aircraft_id'] = self.data['aircraft_id'].str.strip()

    def simple_data_metrics(self) -> None:
        self.data['total_time'] = self.data['day'].fillna(0) + self.data['night'].fillna(0)
        self.data['duel_received'] = self.data['duel_received'].fillna(0)
        self.data['basic_given'] = self.data['basic_given'].fillna(0)
        self.data['advanced_given'] = self.data['advanced_given'].fillna(0)
        self.data['duel_received'] = self.data['duel_received'].replace(' ', 0)
        self.data['basic_given'] = self.data['basic_given'].replace(' ', 0)
        self.data['advanced_given'] = self.data['advanced_given'].replace(' ', 0)

    def build_passenger_dict(self) -> None:
        '''
            Build a dictionary of passenger names and the number
            of times they appear in the memo column

            self.passenger_names = {
                'Bruce Roden': 3,
                'Cody Nielson': 5,
                ...
            }
        '''

        memos = self.data['memo'].dropna().tolist()

        for memo in memos:
            passenger_name = self.extract_passenger_from_memo(memo)
            if passenger_name:
                self.passenger_names[passenger_name] = self.passenger_names.get(passenger_name, 0) + 1
        
        self.passenger_names = dict(sorted(self.passenger_names.items()))

    def extract_passenger_from_memo(self, memo):
        '''
            Extract the passenger name from the memo
            
            Most memos are formated like this:
                '{OBJECTIVE} with {PASSENGER NAME}'
                '{OBJECTIVE} for {PASSENGER NAME}'
                'With {PASSENGER NAME}'


            There are a few notable exceptions
                (Handled) 'Cris '
                (Handled) 'Adam Berger / Flight Review' 
                (Handled) 'Brian Mann, Break Failure'
                (Handled) 'Chris Koch Alternator Failure'
                (Handled) 'Andrew ILS 3 KGCN'
                'Search for Hourse With Hinds' (Kinda Handled -> in misspelling fix)
                (Handled) 'Intro flight for Brad and Melanie'
                (Handled) 'Aircraft moved for maintaince'
                (Handled) 'Test Flight for breaks'
                (Handled) 'Instrument Training eith Rick Casebolt'
                'With Rick Casbolt'
        '''

        regxes = [
            r'(.*) with (.*)',
            r'(.*) eith (.*)',
            r'(.*) for (.*)',
            r'With (.*)'
        ]

        for regx in regxes:
            match = re.search(regx, memo, re.IGNORECASE)
            if match:
                group = len(match.groups())
                raw_passenger_name = match.group(group)

                # Handle 'Cris '
                passenger_name = raw_passenger_name.strip()

                # Handle 'Adam Berger / Flight Review'
                if '/' in passenger_name:
                    passenger_name = passenger_name.split('/')[0].strip()

                # Handle 'Brian Mann, Break Failure'
                elif ',' in passenger_name:
                    passenger_name = passenger_name.split(',')[0].strip()

                # Handle 'Chris Koch Alternator Failure'
                elif ' ' in passenger_name:
                    passenger_name = ' '.join(passenger_name.split()[:2])

                # Handle 'Andrew ILS 3 KGCN'
                # if second word is an acronym (all letter are cap and more than one letter), only take first
                if len(passenger_name.split()) > 1 and passenger_name.split()[1].isupper() and len(passenger_name.split()[1]) > 1:
                    passenger_name = passenger_name.split()[0]
                
                # Handel 'Intro flight for Brad and Melanie' / Poorly
                if 'and' in passenger_name and passenger_name not in ['Brandon Salazar', 'Sanders Esplin']:
                    passenger_name = passenger_name.split('and')[0].strip()

                # Handle 'Aircraft moved for Maintance'
                if 'maintaince' == passenger_name:
                    continue

                # Handle 'Test Flight for breaks'
                if 'breaks' == passenger_name:
                    continue

                # fix misspellings
                spelling_fixes = self.config['passenger_name_consolidation']
                for correct_name, misspelled_names in spelling_fixes.items():
                    if passenger_name in misspelled_names:
                        passenger_name = correct_name

                return passenger_name
    
    def build_flight_objective_dict(self) -> None:
        '''
            Build a dictionary of flight objectives and the number
            of times they appear in the memo column

            self.flight_objectives = {
                'Flight Review': 3,
                'Intro Flight': 5,
                ...
            }
        '''

        memos = self.data['memo'].dropna().tolist()

        for memo in memos:
            flight_objective = self.extract_objective_from_memo(memo)
            if flight_objective:
                self.flight_objectives[flight_objective] = self.flight_objectives.get(flight_objective, 0) + 1
        
        self.flight_objectives = dict(sorted(self.flight_objectives.items()))

    def extract_objective_from_memo(self, memo):
        '''
            Extract the objective of the flight from the memo

            Most memos are formated like this:
                '{OBJECTIVE} with {PASSENGER NAME}'
                '{OBJECTIVE} for {PASSENGER NAME}'
        '''

        regxes = [
            r'(.*) with (.*)',
            r'(.*) eith (.*)',
            r'(.*) for (.*)',
            r'With (.*)'
        ]

        for regx in regxes:
            match = re.search(regx, memo, re.IGNORECASE)
            if match:
                if len(match.groups()) > 1:
                        flight_objective = match.group(1)
                        break
                else:
                    flight_objective = "Other"
            else:
                flight_objective = memo

        # Condenesed flight objectives
        objective_consolidation = self.config['flight_objective_consolidation']
        for correct_objective, misspelled_objectives in objective_consolidation.items():
            if flight_objective in misspelled_objectives:
                flight_objective = correct_objective

        return flight_objective

    def get_airport_location(self):
        '''
            Get the location of the airport from the departure and arrival columns
        '''

        airports = self.data['departure'].tolist()
        airports += self.data['arrival_1'].tolist()
        airports += self.data['arrival_2'].tolist()
        airports += self.data['arrival_3'].tolist()
        airports = [airport for airport in airports if str(airport) != 'nan']
        
        airport_counts = {}
        for airport in airports:
            airport_counts[airport] = airport_counts.get(airport, 0) + 1
            self.airport_data[airport] = None

        airports = airportsdata.load() 
        for airport in airport_counts:
            if airport in airports:
                self.airport_data[airport] = airports[airport]

        airports = airportsdata.load('LID')
        for airport in airport_counts:
            if airport in airports:
                self.airport_data[airport] = airports[airport]
        
    def create_passenger_column(self):
        '''
            Create a new column in the dataframe that contains the passenger name
        '''
        self.data['passenger'] = self.data['memo'].apply(self.extract_passenger_from_memo)

    def create_flight_objective_column(self):
        '''
            Create a new column in the dataframe that contains the flight objective
        '''
        self.data['flight_objective'] = self.data['memo'].apply(self.extract_objective_from_memo)

    def create_distance_travlled_columns(self):
        '''
            Create a new column in the dataframe that contains the distance travelled
        '''
        self.data['distance_travelled_1'] = self.data.apply(lambda row: airport_distance(self.airport_data, row['departure'], row['arrival_1']), axis=1)
        self.data['distance_travelled_2'] = self.data.apply(lambda row: airport_distance(self.airport_data, row['arrival_1'], row['arrival_2']), axis=1)
        self.data['distance_travelled_3'] = self.data.apply(lambda row: airport_distance(self.airport_data, row['arrival_2'], row['arrival_3']), axis=1)
        self.data['distance_travelled'] = self.data['distance_travelled_1'] + self.data['distance_travelled_2'] + self.data['distance_travelled_3']

    def save(self):
        output_folder = self.config['output_folder']
        os.makedirs(output_folder, exist_ok=True)

        self.data.to_csv(f'{output_folder}/processed_flight_data.csv', index=False)
        
        with open(f'{output_folder}/dtd.pkl', 'wb') as f:
            pickle.dump(self, f)

        with open(f'{output_folder}/reports/dtd_report.json', 'w') as f:
            json.dump(self.report, f, indent=4, cls=CustomEncoder)

    @staticmethod
    def load(reload_config=False):
        folder = dtd_config['output_folder']
        file = f'{folder}/dtd.pkl'
        with open(file, 'rb') as f:
            dtd = pickle.load(f)

        if reload_config:
            dtd.config = dtd_config
        return dtd
    
    def date_flight_metrics(self):
        '''
            Create a dictionary of the number of flights per year/year-month/date
        '''
        self.data['date'] = pd.to_datetime(self.data['date'])
        self.data['year'] = self.data['date'].dt.year
        self.data['month'] = self.data['date'].dt.month

        self.data['year_month'] = self.data['date'].dt.to_period('M')
        self.data['year_month'] = self.data['year_month'].astype(str)

        self.data['date_str'] = self.data['date'].dt.date.astype(str)

        self.flights_per_period()
        self.longest_consecutive_days_with_flights()

        return
    
    def flights_per_period(self):
        # Number of flights per year/year-month/date
        flights_per_year = self.data['year'].value_counts()
        self.report['flights_per_year'] = flights_per_year.to_dict()

        flights_per_month = self.data['year_month'].value_counts()
        self.report['flights_per_month'] = flights_per_month.to_dict()

        flights_per_day = self.data['date_str'].value_counts()
        self.report['flights_per_day'] = flights_per_day.to_dict()

        max_flights_year = flights_per_year.idxmax()
        max_flights_month = flights_per_month.idxmax()
        max_flights_day = flights_per_day.idxmax()

        # Most flights per time period
        most_flights_year = pd.DataFrame({
            'year': [max_flights_year],
            'flights': [flights_per_year[max_flights_year]]
        })
        self.report['most_flights_year'] = most_flights_year.to_dict(orient='records')[0]

        most_flights_month = pd.DataFrame({
            'year_month': [max_flights_month],
            'flights': [flights_per_month[max_flights_month]]
        })
        self.report['most_flights_month'] = most_flights_month.to_dict(orient='records')[0]

        most_flights_day = pd.DataFrame({
            'date': [max_flights_day],
            'flights': [flights_per_day[max_flights_day]]
        })
        self.report['most_flights_day'] = most_flights_day.to_dict(orient='records')[0]

        # Save the reports
        folder = f'{self.config['output_folder']}/reports'
        os.makedirs(folder, exist_ok=True)

        flights_per_year.to_csv(f'{folder}/flights_per_year.csv')
        flights_per_month.to_csv(f'{folder}/flights_per_month.csv')
        flights_per_day.to_csv(f'{folder}/flights_per_day.csv')
        most_flights_day.to_csv(f'{folder}/most_flights_day.csv')
        most_flights_month.to_csv(f'{folder}/most_flights_month.csv')
        most_flights_year.to_csv(f'{folder}/most_flights_year.csv')

    def longest_consecutive_days_with_flights(self):
        temp_df = self.data.drop_duplicates(subset=['date'])['date']
        # Ensure the 'date' column is of datetime type
        temp_df = pd.to_datetime(temp_df)

        # Sort the dataframe by date
        temp_df = temp_df.sort_values()

        # Identify gaps in dates where the difference is not 1 day
        temp_df = temp_df.to_frame()
        temp_df['gap'] = temp_df['date'].diff().dt.days != 1

        # Group by the identified gaps and count the size of each group
        consecutive_days = temp_df.groupby(temp_df['gap'].cumsum()).size()

        # Find the longest period with consecutive flights
        longest_period = consecutive_days.max()

        # Find the start and end date of the longest period
        longest_period_group = consecutive_days.idxmax()
        start_date = temp_df[temp_df['gap'].cumsum() == longest_period_group]['date'].min()
        end_date = temp_df[temp_df['gap'].cumsum() == longest_period_group]['date'].max()

        longest_period_df = pd.DataFrame({
            'start_date': [start_date.date().strftime('%Y-%m-%d')],
            'end_date': [end_date.date().strftime('%Y-%m-%d')],
            'consecutive_days': [longest_period]
        })
        self.report['longest_consecutive_days'] = longest_period_df.to_dict(orient='records')[0]

        # Save the report
        folder = f'{self.config['output_folder']}/reports'
        os.makedirs(folder, exist_ok=True)

        consecutive_days.to_csv(f'{folder}/consecutive_days.csv')
        longest_period_df.to_csv(f'{folder}/longest_period.csv')

    def aircraft_metrics(self):
        # count number of flights per aircraft make and model
        flights_per_aircraft = self.data['aircraft_make_model'].value_counts()
        self.report['flights_per_aircraft'] = flights_per_aircraft.to_dict()
        
        flight_hours_per_aircraft = self.data.groupby('aircraft_make_model')['total_time'].sum()
        self.report['flight_hours_per_aircraft'] = flight_hours_per_aircraft.to_dict()
        
        self.report['aircraft_count'] = flights_per_aircraft.shape[0]

        # count number of flights per aircraft id
        flights_per_aircraft_id = self.data['aircraft_id'].value_counts()
        self.report['flights_per_aircraft_id'] = flights_per_aircraft_id.to_dict()

        flight_hours_per_aircraft_id = self.data.groupby('aircraft_id')['total_time'].sum()
        self.report['flight_hours_per_aircraft_id'] = flight_hours_per_aircraft_id.to_dict()

        self.report['aircraft_id_count'] = flights_per_aircraft_id.shape[0]

        # Save the reports
        folder = f'{self.config['output_folder']}/reports'
        os.makedirs(folder, exist_ok=True)

        flights_per_aircraft.to_csv(f'{folder}/flights_per_aircraft.csv')
        flights_per_aircraft_id.to_csv(f'{folder}/flights_per_aircraft_id.csv')
        flight_hours_per_aircraft.to_csv(f'{folder}/flight_hours_per_aircraft.csv')
        flight_hours_per_aircraft_id.to_csv(f'{folder}/flight_hours_per_aircraft_id.csv')

        self.first_time_aircraft_flown()

        return
    
    def first_time_aircraft_flown(self):
        first_flight_date_model = self.data.groupby('aircraft_make_model')['date'].min()
        first_flight_date_model = first_flight_date_model.reset_index()
        first_flight_date_model.columns = ['aircraft_make_model', 'date']
        first_flight_date_model['date'] = first_flight_date_model['date'].astype(str)

        self.report['first_flight_date_model'] = first_flight_date_model.to_dict(orient='records')

        first_flight_date_id = self.data.groupby('aircraft_id')['date'].min()
        first_flight_date_id = first_flight_date_id.reset_index()
        first_flight_date_id.columns = ['aircraft_id', 'date']
        first_flight_date_id['date'] = first_flight_date_id['date'].astype(str)

        self.report['first_flight_date_id'] = first_flight_date_id.to_dict(orient='records')

        # Save the reports
        folder = f'{self.config['output_folder']}/reports'
        os.makedirs(folder, exist_ok=True)

        first_flight_date_model.to_csv(f'{folder}/first_flight_date_model.csv')
        first_flight_date_id.to_csv(f'{folder}/first_flight_date_id.csv')

        return
        
    def airport_metrics(self):
        self.first_time_at_each_airport()
        self.number_of_visits_at_each_airport()
        return
    
    def number_of_visits_at_each_airport(self):
        airport_visits = pd.concat([self.data['departure'], self.data['arrival_1'], self.data['arrival_2'], self.data['arrival_3']])
        airport_visits = airport_visits.value_counts()
        self.report['airport_visits'] = airport_visits.to_dict()

        num_unique_airports = pd.DataFrame({
            'unique_airports': [airport_visits.shape[0]]
        })
        self.report['num_unique_airports'] = num_unique_airports.to_dict(orient='records')[0]

        # count of number of local flights vs non-local flights
        local_flights = self.data[self.data['arrival_1'].str.lower() == 'local']
        local_flights = local_flights.shape[0]
        non_local_flights = self.data.shape[0] - local_flights

        local_flights_df = pd.DataFrame({
            'local_flights': [local_flights],
            'non_local_flights': [non_local_flights]
        })
        self.report['local_flights'] = local_flights_df.to_dict(orient='records')[0]

        # Save the report
        folder = f'{self.config['output_folder']}/reports'
        os.makedirs(folder, exist_ok=True)
        
        airport_visits.to_csv(f'{folder}/airport_visits.csv')
        num_unique_airports.to_csv(f'{folder}/num_unique_airports.csv')
        local_flights_df.to_csv(f'{folder}/local_flights.csv')
        return

    def first_time_at_each_airport(self):
        # first time departing or landing at each airport
        first_flight_date_departure = self.data.groupby('departure')['date'].min()
        first_flight_date_departure = first_flight_date_departure.reset_index()
        first_flight_date_departure.columns = ['airport', 'date']
        first_flight_date_departure['date'] = first_flight_date_departure['date'].astype(str)

        first_flight_date_arrival_1 = self.data.groupby('arrival_1')['date'].min()
        first_flight_date_arrival_1 = first_flight_date_arrival_1.reset_index()
        first_flight_date_arrival_1.columns = ['airport', 'date']
        first_flight_date_arrival_1['date'] = first_flight_date_arrival_1['date'].astype(str)

        first_flight_date_arrival_2 = self.data.groupby('arrival_2')['date'].min()
        first_flight_date_arrival_2 = first_flight_date_arrival_2.reset_index()
        first_flight_date_arrival_2.columns = ['airport', 'date']
        first_flight_date_arrival_2['date'] = first_flight_date_arrival_2['date'].astype(str)

        first_flight_date_arrival_3 = self.data.groupby('arrival_3')['date'].min()
        first_flight_date_arrival_3 = first_flight_date_arrival_3.reset_index()
        first_flight_date_arrival_3.columns = ['airport', 'date']
        first_flight_date_arrival_3['date'] = first_flight_date_arrival_3['date'].astype(str)
        
        # combine all the first flight dates
        first_flight_date = pd.concat([first_flight_date_departure, first_flight_date_arrival_1, first_flight_date_arrival_2, first_flight_date_arrival_3])
        first_flight_date = first_flight_date.groupby('airport')['date'].min()
        first_flight_date = first_flight_date.reset_index()
        first_flight_date.columns = ['airport', 'date']
        first_flight_date['date'] = first_flight_date['date'].astype(str)   

        self.report['first_flight_date'] = first_flight_date.to_dict(orient='records')

        # Save the reports
        folder = f'{self.config['output_folder']}/reports'
        os.makedirs(folder, exist_ok=True)

        first_flight_date_departure.to_csv(f'{folder}/first_flight_date_departure.csv')
        first_flight_date_arrival_1.to_csv(f'{folder}/first_flight_date_arrival_1.csv')
        first_flight_date_arrival_2.to_csv(f'{folder}/first_flight_date_arrival_2.csv')
        first_flight_date_arrival_3.to_csv(f'{folder}/first_flight_date_arrival_3.csv')
        first_flight_date.to_csv(f'{folder}/first_flight_date.csv')
        return
    
    def hours_metrics(self):
        # total hours
        total_hours = pd.DataFrame({
            'total_hours': [self.data['total_time'].sum()]
        })
        self.report['total_hours'] = total_hours.to_dict(orient='records')[0]
        
        # cumulative hours per day
        cumulative_hours_per_day = self.data.groupby('date')['total_time'].sum().cumsum()
        cumulative_hours_per_day = cumulative_hours_per_day.reset_index()
        cumulative_hours_per_day.columns = ['date', 'cumulative_hours']
        cumulative_hours_per_day['date'] = cumulative_hours_per_day['date'].astype(str)
        self.report['cumulative_hours_per_day'] = cumulative_hours_per_day.to_dict()

        # Cross country hours
        cross_country_hours = pd.DataFrame({
            'cross_country_hours': [self.data['cross_country'].sum()]
        })
        self.report['cross_country_hours'] = cross_country_hours.to_dict(orient='records')[0]

        # Hours of instruction received
        hours_of_instruction_received = pd.DataFrame({
            'duel_received': [self.data['duel_received'].sum()]
        })
        self.report['hours_of_instruction_received'] = hours_of_instruction_received.to_dict(orient='records')[0]

        # Hours of instruction given
        hours_of_instruction_given = pd.DataFrame({
            'total_given': [ self.data['basic_given'].astype(float).sum() + self.data['advanced_given'].astype(float).sum()]
        })
        self.report['hours_of_instruction_given'] = hours_of_instruction_given.to_dict(orient='records')[0]

        # Save the reports
        folder = f'{self.config['output_folder']}/reports'
        os.makedirs(folder, exist_ok=True)

        total_hours.to_csv(f'{folder}/total_hours.csv')
        cumulative_hours_per_day.to_csv(f'{folder}/cumulative_hours_per_day.csv')
        cross_country_hours.to_csv(f'{folder}/cross_country_hours.csv')
        hours_of_instruction_received.to_csv(f'{folder}/hours_of_instruction_received.csv')
        hours_of_instruction_given.to_csv(f'{folder}/hours_of_instruction_given.csv')

    def passenger_metrics(self):
        # Number of flights per passenger
        flights_per_passenger = self.data['passenger'].value_counts()
        self.report['flights_per_passenger'] = flights_per_passenger.to_dict()

        # Number of hours per passenger
        hours_per_passenger = self.data.groupby('passenger')['total_time'].sum()
        self.report['hours_per_passenger'] = hours_per_passenger.to_dict()

        self.first_passenger_flight()
        self.passenger_timelines()

        # Save the report
        folder = f'{self.config['output_folder']}/reports'
        os.makedirs(folder, exist_ok=True)

        flights_per_passenger.to_csv(f'{folder}/flights_per_passenger.csv')
        hours_per_passenger.to_csv(f'{folder}/hours_per_passenger.csv')

    def first_passenger_flight(self):
        first_flight_date_passenger = self.data.groupby('passenger')['date'].min()
        first_flight_date_passenger = first_flight_date_passenger.reset_index()
        first_flight_date_passenger.columns = ['passenger', 'date']
        first_flight_date_passenger['date'] = first_flight_date_passenger['date'].astype(str)

        self.report['first_flight_date_passenger'] = first_flight_date_passenger.to_dict(orient='records')

        # Save the report
        folder = f'{self.config['output_folder']}/reports'
        os.makedirs(folder, exist_ok=True)

        first_flight_date_passenger.to_csv(f'{folder}/first_flight_date_passenger.csv')

    def passenger_timelines(self):
        # make a df of passenger name, first flight, last flight, total flights, total hours, total days in between
        passenger_timelines = self.data.groupby('passenger').agg(
            first_flight=('date', 'min'),
            last_flight=('date', 'max'),
            total_flights=('date', 'count'),
            total_hours=('total_time', 'sum')
        )
        passenger_timelines['days_between'] = (passenger_timelines['last_flight'] - passenger_timelines['first_flight']).dt.days
        passenger_timelines = passenger_timelines.reset_index()
        
        passenger_timelines['first_flight'] = passenger_timelines['first_flight'].dt.date.astype(str)
        passenger_timelines['last_flight'] = passenger_timelines['last_flight'].dt.date.astype(str)
        
        self.report['passenger_timelines'] = passenger_timelines.to_dict(orient='records')

        # Save the report
        folder = f'{self.config['output_folder']}/reports'
        os.makedirs(folder, exist_ok=True)

        passenger_timelines.to_csv(f'{folder}/passenger_timelines.csv')

    def objective_metrics(self):
        # Number of flights per objective
        flights_per_objective = self.data['flight_objective'].value_counts()
        self.report['flights_per_objective'] = flights_per_objective.to_dict()

        # Number of hours per objective
        hours_per_objective = self.data.groupby('flight_objective')['total_time'].sum()
        self.report['hours_per_objective'] = hours_per_objective.to_dict()

        # Save the report
        folder = f'{self.config['output_folder']}/reports'
        os.makedirs(folder, exist_ok=True)

        flights_per_objective.to_csv(f'{folder}/flights_per_objective.csv')
        hours_per_objective.to_csv(f'{folder}/hours_per_objective.csv')

    def distance_metrics(self):
        # Cumulative distance per day
        cumulative_distance_per_day = self.data.groupby('date')['distance_travelled'].sum().cumsum()
        cumulative_distance_per_day = cumulative_distance_per_day.reset_index()
        cumulative_distance_per_day.columns = ['date', 'cumulative_distance']
        cumulative_distance_per_day['date'] = cumulative_distance_per_day['date'].astype(str)
        self.report['cumulative_distance_per_day'] = cumulative_distance_per_day.to_dict()

        # Save the report
        folder = f'{self.config['output_folder']}/reports'
        os.makedirs(folder, exist_ok=True)

        cumulative_distance_per_day.to_csv(f'{folder}/cumulative_distance_per_day.csv')