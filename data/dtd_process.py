import re
import os
import pickle
import pandas as pd
import airportsdata
from dtd_config import dtd_config
from dtd_utils import airport_distance

class DTD:
    def __init__(self, config) -> None:
        self.config = config
        self.passenger_names = {}
        self.flight_objectives = {}
        self.airport_data = {}
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
                if 'and' in passenger_name:
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
            pickle.dump(dtd, f)

if __name__ == '__main__':
    dtd = DTD(dtd_config)
    dtd.load_flight_data()
    dtd.change_col_names()

    dtd.simple_clean_data()

    dtd.build_passenger_dict()
    dtd.create_passenger_column()

    dtd.build_flight_objective_dict()
    dtd.create_flight_objective_column()

    dtd.get_airport_location()
    dtd.create_distance_travlled_columns()

    dtd.save()



    

