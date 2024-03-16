import re
import pandas as pd
from dtd_config import dtd_config

class DTD:
    def __init__(self, config) -> None:
        self.config = config
        self.passenger_names = {}
        self.flight_purposes = {}
        return

    def load_flight_data(self) -> None:
        path = self.config['dtd_data_path']
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
                '{PURPOSE} with {PASSENGER NAME}'
                '{PURPOSE} for {PASSENGER NAME}'

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
        '''

        regxes = [
            r'(.*) with (.*)',
            r'(.*) for (.*)'
        ]

        for regx in regxes:
            match = re.search(regx, memo, re.IGNORECASE)
            if match:
                raw_passenger_name = match.group(2)

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
    
    def build_flight_purpose_dict(self) -> None:
        '''
            Build a dictionary of flight purposes and the number
            of times they appear in the memo column

            self.flight_purposes = {
                'Flight Review': 3,
                'Intro Flight': 5,
                ...
            }
        '''

        memos = self.data['memo'].dropna().tolist()

        for memo in memos:
            flight_purpose = self.extract_purpose_from_memo(memo)
            if flight_purpose:
                self.flight_purposes[flight_purpose] = self.flight_purposes.get(flight_purpose, 0) + 1
        
        self.flight_purposes = dict(sorted(self.flight_purposes.items()))
        print(self.flight_purposes)

    def extract_purpose_from_memo(self, memo):
        '''
            Extract the purpose of the flight from the memo

            Most memos are formated like this:
                '{PURPOSE} with {PASSENGER NAME}'
                '{PURPOSE} for {PASSENGER NAME}'
        '''

        regxes = [
            r'(.*) with (.*)',
            r'(.*) for (.*)'
        ]

        for regx in regxes:
            match = re.search(regx, memo, re.IGNORECASE)
            if match:
                flight_purpose = match.group(1)
                return flight_purpose
        pass

    def create_passenger_column(self):
        '''
            Create a new column in the dataframe that contains the passenger name
        '''
        self.data['passenger'] = self.data['memo'].apply(self.extract_passenger_from_memo)

if __name__ == '__main__':
    dtd = DTD(dtd_config)
    dtd.load_flight_data()
    dtd.change_col_names()
    dtd.build_passenger_dict()
    dtd.create_passenger_column()
    dtd.build_flight_purpose_dict()
    dtd.data.to_csv('dtd_data.csv', index=False)
