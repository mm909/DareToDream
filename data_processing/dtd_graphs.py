import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def flight_timeline(data, date_markers):
    # convert the date column to datetime
    data['date'] = pd.to_datetime(data['date'])

    # count the number of flights per day
    flights_per_day = data['date'].value_counts().sort_index()
    flights_per_day = flights_per_day.cumsum()

    # plot the data
    fig, ax1 = plt.subplots(figsize=(15, 9))



    ax1.plot(flights_per_day, color='black')
    # ax2.plot(flight_hours_per_day, color='red')

    # add markers for important dates
    for marker in date_markers:

        marker['date'] = pd.to_datetime(marker['date'])

        size = 7
        if marker['type'] == 'Start':
            ax1.plot(marker['date'], flights_per_day[marker['date']], '^', markersize=size, color='red')
        elif marker['type'] == 'Flight':
            ax1.plot(marker['date'], flights_per_day[marker['date']], 'bo', markersize=size, color='blue')
        elif marker['type'] == 'Back':
            ax1.plot(marker['date'], flights_per_day[marker['date']], 's', markersize=size, color='green')
        elif marker['type'] == 'Retired':
            ax1.plot(marker['date'], flights_per_day[marker['date']], '*', markersize=size, color='orange')
        elif marker['type'] == 'Exam':
            ax1.plot(marker['date'], flights_per_day[marker['date']], 'X', markersize=size, color='red')

    ax1.set_xlabel('Date', fontsize=15)
    ax1.set_ylabel('Number of flights', color='black', fontsize=15)

    num_days_between = (data['date'].max() - data['date'].min()).days

    ax1.set_title(f'{num_days_between} Days of Flight Logs', fontsize=20)

    # format the x-axis to show the date
    ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y'))
    ax1.xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=180))

    # add grid lines for the x-axis make it one per year
    ax1.xaxis.set_major_locator(plt.matplotlib.dates.YearLocator())

    # add grid lines for the y-axis
    ax1.yaxis.grid(True, linestyle='--', color='black', alpha=0.5)

    # set the x-axis limits
    ax1.set_xlim(data['date'].min()-pd.Timedelta(days=30), data['date'].max()+pd.Timedelta(days=1))

    # set y lim
    ax1.set_ylim(-25, flights_per_day.max() + 10)

    # adjust the layout to prevent overlapping dates
    fig.autofmt_xdate()

    # Save
    folder = 'data/graphs'
    os.makedirs(folder, exist_ok=True)
    plt.savefig(f'{folder}/flights_per_day.png')

    # show the plot
    plt.show()

    # clear
    plt.clf()

    return


def flight_timeline_2(data, date_markers):
    # convert the date column to datetime
    data['date'] = pd.to_datetime(data['date'])

    # count the number of flights per day
    flights_per_day = data['date'].value_counts().sort_index()
    flights_per_day = flights_per_day.cumsum()

    # plot the data
    fig, ax1 = plt.subplots(figsize=(15, 9))



    ax1.plot(flights_per_day, color='black')
    # ax2.plot(flight_hours_per_day, color='red')

    # add markers for important dates
    for marker in date_markers:

        marker['date'] = pd.to_datetime(marker['date'])

        size = 7
        if marker['type'] == 'Start':
            ax1.plot(marker['date'], flights_per_day[marker['date']], '^', markersize=size, color='red')
        elif marker['type'] == 'Flight':
            ax1.plot(marker['date'], flights_per_day[marker['date']], 'bo', markersize=size, color='blue')
        elif marker['type'] == 'Back':
            ax1.plot(marker['date'], flights_per_day[marker['date']], 's', markersize=size, color='green')
        elif marker['type'] == 'Retired':
            ax1.plot(marker['date'], flights_per_day[marker['date']], '*', markersize=size, color='orange')
        elif marker['type'] == 'Exam':
            ax1.plot(marker['date'], flights_per_day[marker['date']], 'X', markersize=size, color='red')

    ax1.set_xlabel('Date', fontsize=15)
    ax1.set_ylabel('Number of flights', color='black', fontsize=15)

    num_days_between = (data['date'].max() - data['date'].min()).days

    ax1.set_title(f'{num_days_between} Days of Flight Logs', fontsize=20)

    # format the x-axis to show the date
    ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y'))
    ax1.xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=180))

    # add grid lines for the x-axis make it one per year
    ax1.xaxis.set_major_locator(plt.matplotlib.dates.YearLocator())

    # horizontal line at 265 hours
    ax1.axhline(y=265, color='r', linestyle='--', label='265 hours')

    # add grid lines for the y-axis
    ax1.yaxis.grid(True, linestyle='--', color='black', alpha=0.5)

    # set the x-axis limits
    ax1.set_xlim(data['date'].min()-pd.Timedelta(days=30), data['date'].max()+pd.Timedelta(days=1))

    # set y lim
    ax1.set_ylim(-25, flights_per_day.max() + 10)

    # adjust the layout to prevent overlapping dates
    fig.autofmt_xdate()

    # Save
    folder = 'data/graphs'
    os.makedirs(folder, exist_ok=True)
    plt.savefig(f'{folder}/flights_per_day.png')

    # show the plot
    plt.show()

    # clear
    plt.clf()

    return


def flights_per_year(data):
    # bar chart of the number of flights per year
    fig, ax = plt.subplots(figsize=(15, 9))

    # count the number of flights per year
    flights_per_year = data['date'].dt.year.value_counts().sort_index()

    # plot the data
    flights_per_year.plot(kind='bar', ax=ax, color='blue', alpha=0.7)

    # set the title and labels
    ax.set_title('Number of Flights per Year', fontsize=20)
    ax.set_xlabel('Year', fontsize=15)
    ax.set_ylabel('Number of Flights', fontsize=15)

    # add grid lines
    ax.grid(True, linestyle='--', color='black', alpha=0.5)

    # Save
    folder = 'data/graphs'
    os.makedirs(folder, exist_ok=True)
    plt.savefig(f'{folder}/flights_per_year.png')

    # show the plot
    plt.show()

    # clear
    plt.clf()    

def flight_timeline_hours(data, date_markers):
    # convert the date column to datetime
    data['date'] = pd.to_datetime(data['date'])

    # count the number of flights per day
    flights_per_day = data['date'].value_counts().sort_index()
    flights_per_day = flights_per_day.cumsum()

    # count number of flight hours per day
    flight_hours_per_day = data.groupby('date')['total_time'].sum()
    flight_hours_per_day = flight_hours_per_day.cumsum()

    # plot the data
    fig, ax1 = plt.subplots(figsize=(15, 9))

    ax1.plot(flights_per_day, color='black', alpha=0.5)
    ax1.plot(flight_hours_per_day, color='red')

    # add markers for important dates
    for marker in date_markers:
        marker['date'] = pd.to_datetime(marker['date'])

        size = 7
        if marker['type'] == 'Start':
            ax1.plot(marker['date'], flights_per_day[marker['date']], '^', markersize=size, color='red', alpha=0.5)
        elif marker['type'] == 'Flight':
            ax1.plot(marker['date'], flights_per_day[marker['date']], 'bo', markersize=size, color='blue', alpha=0.5)
        elif marker['type'] == 'Back':
            ax1.plot(marker['date'], flights_per_day[marker['date']], 's', markersize=size, color='green', alpha=0.5)
        elif marker['type'] == 'Retired':
            ax1.plot(marker['date'], flights_per_day[marker['date']], '*', markersize=size, color='orange', alpha=0.5)
        elif marker['type'] == 'Exam':
            ax1.plot(marker['date'], flights_per_day[marker['date']], 'X', markersize=size, color='red', alpha=0.5)

    ax1.set_xlabel('Date', fontsize=15)
    ax1.set_ylabel('Number of flights', color='black', fontsize=15)

    num_days_between = (data['date'].max() - data['date'].min()).days

    ax1.set_title(f'{num_days_between} Days of Flight Logs (Flights vs Hours)', fontsize=20)

    # format the x-axis to show the date
    ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y'))
    ax1.xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=180))

    # add grid lines for the x-axis make it one per year
    ax1.xaxis.set_major_locator(plt.matplotlib.dates.YearLocator())
    # ax1.xaxis.grid(True, which='major', linestyle='--', color='black', alpha=0.5)

    # add grid lines for the y-axis
    ax1.yaxis.grid(True, linestyle='--', color='black', alpha=0.5)

    # set the x-axis limits
    ax1.set_xlim(data['date'].min()-pd.Timedelta(days=30), data['date'].max()+pd.Timedelta(days=1))

    # set y lim
    ax1.set_ylim(-25, max(flights_per_day.max(), flight_hours_per_day.max()) + 10)

    # adjust the layout to prevent overlapping dates
    fig.autofmt_xdate()

    # Save
    folder = 'data/graphs'
    os.makedirs(folder, exist_ok=True)
    plt.savefig(f'{folder}/flights_per_day_hours.png')

    # show the plot
    plt.show()

    # clear
    plt.clf()

    return

def flight_timeline_hours(data, date_markers):
    # convert the date column to datetime
    data['date'] = pd.to_datetime(data['date'])

    # count number of flight hours per day
    flight_hours_per_day = data.groupby('date')['total_time'].sum()
    flight_hours_per_day = flight_hours_per_day.cumsum()

    # plot the data
    fig, ax1 = plt.subplots(figsize=(15, 9))

    ax1.plot(flight_hours_per_day)

    ax1.set_xlabel('Date', fontsize=15)

    num_days_between = (data['date'].max() - data['date'].min()).days

    ax1.set_title(f'{num_days_between} Days of Flight Logs - 265 Hours', fontsize=20)

    # format the x-axis to show the date
    ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y'))
    ax1.xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=180))

    # add grid lines for the x-axis make it one per year
    ax1.xaxis.set_major_locator(plt.matplotlib.dates.YearLocator())
    # ax1.xaxis.grid(True, which='major', linestyle='--', color='black', alpha=0.5)

    # horizontal line at 265 hours
    ax1.axhline(y=265, color='r', linestyle='--', label='265 hours')

    # add grid lines for the y-axis
    ax1.yaxis.grid(True, linestyle='--', color='black', alpha=0.5)

    # y-lim
    ax1.set_ylim(0, flight_hours_per_day.max() + 10)

    # y label
    ax1.set_ylabel('Total Flight Hours', fontsize=15)

    # set the x-axis limits
    ax1.set_xlim(data['date'].min()-pd.Timedelta(days=30), data['date'].max()+pd.Timedelta(days=1))

    # adjust the layout to prevent overlapping dates
    fig.autofmt_xdate()

    # Save
    folder = 'data/graphs'
    os.makedirs(folder, exist_ok=True)
    plt.savefig(f'{folder}/flights_per_day_hours_265.png')

    # show the plot
    plt.show()

    # clear
    plt.clf()

    return

def flight_timeline_num_models(data, date_markers):
    # convert the date column to datetime
    data['date'] = pd.to_datetime(data['date'])

    # count the number of flights per day
    flights_per_day = data['date'].value_counts().sort_index()
    flights_per_day = flights_per_day.cumsum()

    # count the first instance of each new aircraft_make_model
    # eg if row 1 has C172 and row 2 has C172 then it should only count the first instance of C172
    # but when it sees C182 it should count that as a new model and the total should be 2
    data['first_instance'] = data['aircraft_make_model'].ne(data['aircraft_make_model'].shift()).astype(int)
    first_instance_indices = data.groupby('aircraft_make_model')['first_instance'].idxmax()
    num_models = data.loc[first_instance_indices].groupby('date')['first_instance'].sum().sort_index()
    num_models = num_models.cumsum()

    # plot the data
    fig, ax1 = plt.subplots(figsize=(15, 9))
    # split the plot into two y-axes
    ax2 = ax1.twinx()

    ax1.plot(flights_per_day, color='black', alpha=0.5)
    ax2.plot(num_models, color='red')

    # add markers for important dates
    for marker in date_markers:
        marker['date'] = pd.to_datetime(marker['date'])

        size = 7
        if marker['type'] == 'Start':
            ax1.plot(marker['date'], flights_per_day[marker['date']], '^', markersize=size, color='red', alpha=0.5)
        elif marker['type'] == 'Flight':
            ax1.plot(marker['date'], flights_per_day[marker['date']], 'bo', markersize=size, color='blue', alpha=0.5)
        elif marker['type'] == 'Back':
            ax1.plot(marker['date'], flights_per_day[marker['date']], 's', markersize=size, color='green', alpha=0.5)
        elif marker['type'] == 'Retired':
            ax1.plot(marker['date'], flights_per_day[marker['date']], '*', markersize=size, color='orange', alpha=0.5)
        elif marker['type'] == 'Exam':
            ax1.plot(marker['date'], flights_per_day[marker['date']], 'X', markersize=size, color='red', alpha=0.5)

    ax1.set_xlabel('Date', fontsize=15)
    ax1.set_ylabel('Number of flights', color='black', fontsize=15)
    ax2.set_ylabel('Number of models', color='red', fontsize=15)

    num_days_between = (data['date'].max() - data['date'].min()).days

    ax1.set_title(f'{num_days_between} Days of Flight Logs (Flights vs Models)', fontsize=20)

    # format the x-axis to show the date
    ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y'))
    ax1.xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=180))

    # add grid lines for the x-axis make it one per year
    ax1.xaxis.set_major_locator(plt.matplotlib.dates.YearLocator())
    # ax1.xaxis.grid(True, which='major', linestyle='--', color='black', alpha=0.5)

    # add grid lines for the y-axis
    ax1.yaxis.grid(True, linestyle='--', color='black', alpha=0.5)

    # set the x-axis limits
    ax1.set_xlim(data['date'].min()-pd.Timedelta(days=30), data['date'].max()+pd.Timedelta(days=1))

    # set y lim
    ax1.set_ylim(-25, max(flights_per_day.max(), num_models.max()) + 10)

    # adjust the layout to prevent overlapping dates
    fig.autofmt_xdate()

    # Save
    folder = 'data/graphs'
    os.makedirs(folder, exist_ok=True)
    plt.savefig(f'{folder}/flights_per_day_models.png')

    # show the plot
    plt.show()

    # clear
    plt.clf()

    return

def bar_chart_models(data):
    # make a bar chart of the number of flights per aircraft_make_model
    fig, ax = plt.subplots(figsize=(15, 9))

    # count the number of flights per aircraft_make_model
    flights_per_model = data['aircraft_make_model'].value_counts()

    # sort alphabetically
    flights_per_model = flights_per_model.sort_index()

    # plot the data
    flights_per_model.plot(kind='bar', ax=ax, color='blue', alpha=0.7)

    # set the title and labels
    ax.set_title('Number of Flights per Aircraft Make and Model', fontsize=20)
    
    ax.set_xlabel('Aircraft Make and Model', fontsize=15)
    ax.set_ylabel('Number of Flights', fontsize=15)

    # add grid lines
    ax.grid(True, linestyle='--', color='black', alpha=0.5)

    # Save
    folder = 'data/graphs'
    os.makedirs(folder, exist_ok=True)
    plt.savefig(f'{folder}/flights_per_model.png')

    # show the plot
    plt.show()

    # clear
    plt.clf()

def bar_chart_models_hours(data):
    # make a bar chart of the number of flights per aircraft_make_model
    fig, ax = plt.subplots(figsize=(15, 9))

    # count the number of flight hours per aircraft_make_model
    flight_hours_per_model = data.groupby('aircraft_make_model')['total_time'].sum()

    # sort alphabetically
    flight_hours_per_model = flight_hours_per_model.sort_index()

    # plot the data
    flight_hours_per_model.plot(kind='bar', ax=ax, color='red', alpha=0.7)

    # set the title and labels
    ax.set_title('Number of Flights and Hours per Aircraft Make and Model', fontsize=20)
    
    ax.set_xlabel('Aircraft Make and Model', fontsize=15)
    ax.set_ylabel('Number of Flights', fontsize=15)

    # add grid lines
    ax.grid(True, linestyle='--', color='black', alpha=0.5)

    # Save
    folder = 'data/graphs'
    os.makedirs(folder, exist_ok=True)
    plt.savefig(f'{folder}/flights_and_hours_per_model.png')

    # show the plot
    plt.show()

    # clear
    plt.clf()

def bar_chart_models_hours_and_flights(data):
    # make a bar chart of the number of flights per aircraft_make_model
    fig, ax = plt.subplots(figsize=(15, 9))

    # count the number of flights per aircraft_make_model
    flights_per_model = data['aircraft_make_model'].value_counts()

    # count the number of flight hours per aircraft_make_model
    flight_hours_per_model = data.groupby('aircraft_make_model')['total_time'].sum()

    # sort alphabetically
    flights_per_model = flights_per_model.sort_index()
    flight_hours_per_model = flight_hours_per_model.sort_index()

    # plot the data as two groups of bars
    width = 0.35
    x = range(len(flights_per_model))

    ax.bar(x, flights_per_model, width, label='Flights', color='blue', alpha=0.7)
    ax.bar([i + width for i in x], flight_hours_per_model, width, label='Hours', color='red', alpha=0.7)

    # set the title and labels
    ax.set_title('Number of Flights and Hours per Aircraft Make and Model', fontsize=20)

    ax.set_xlabel('Aircraft Make and Model', fontsize=15)
    ax.set_ylabel('Number of Flights', fontsize=15)

    # set x axis labels as the aircraft make and model
    ax.set_xticks([i + width/2 for i in x])
    ax.set_xticklabels(flights_per_model.index, rotation=90)


    # add grid lines
    ax.grid(True, linestyle='--', color='black', alpha=0.5)

    # add the legend
    ax.legend()

    # Save
    folder = 'data/graphs'
    os.makedirs(folder, exist_ok=True)
    plt.savefig(f'{folder}/flights_and_hours_per_model.png')

    # show the plot
    plt.show()

    # clear
    plt.clf()

def flight_timeline_num_tailnumbers(data, date_markers):
    # convert the date column to datetime
    data['date'] = pd.to_datetime(data['date'])

    # count the number of flights per day
    flights_per_day = data['date'].value_counts().sort_index()
    flights_per_day = flights_per_day.cumsum()

    # count the first instance of each new aircraft_make_model
    # eg if row 1 has C172 and row 2 has C172 then it should only count the first instance of C172
    # but when it sees C182 it should count that as a new model and the total should be 2
    data['first_instance'] = data['aircraft_id'].ne(data['aircraft_id'].shift()).astype(int)
    first_instance_indices = data.groupby('aircraft_id')['first_instance'].idxmax()
    num_models = data.loc[first_instance_indices].groupby('date')['first_instance'].sum().sort_index()
    num_models = num_models.cumsum()

    # plot the data
    fig, ax1 = plt.subplots(figsize=(15, 9))
    # split the plot into two y-axes
    ax2 = ax1.twinx()

    ax1.plot(flights_per_day, color='black', alpha=0.5)
    ax2.plot(num_models, color='red')

    # add markers for important dates
    for marker in date_markers:
        marker['date'] = pd.to_datetime(marker['date'])

        size = 7
        if marker['type'] == 'Start':
            ax1.plot(marker['date'], flights_per_day[marker['date']], '^', markersize=size, color='red', alpha=0.5)
        elif marker['type'] == 'Flight':
            ax1.plot(marker['date'], flights_per_day[marker['date']], 'bo', markersize=size, color='blue', alpha=0.5)
        elif marker['type'] == 'Back':
            ax1.plot(marker['date'], flights_per_day[marker['date']], 's', markersize=size, color='green', alpha=0.5)
        elif marker['type'] == 'Retired':
            ax1.plot(marker['date'], flights_per_day[marker['date']], '*', markersize=size, color='orange', alpha=0.5)
        elif marker['type'] == 'Exam':
            ax1.plot(marker['date'], flights_per_day[marker['date']], 'X', markersize=size, color='red', alpha=0.5)

    ax1.set_xlabel('Date', fontsize=15)
    ax1.set_ylabel('Number of flights', color='black', fontsize=15)
    ax2.set_ylabel('Number of models', color='red', fontsize=15)

    num_days_between = (data['date'].max() - data['date'].min()).days

    ax1.set_title(f'{num_days_between} Days of Flight Logs (Flights vs Tail Numbers)', fontsize=20)

    # format the x-axis to show the date
    ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y'))
    ax1.xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=180))

    # add grid lines for the x-axis make it one per year
    ax1.xaxis.set_major_locator(plt.matplotlib.dates.YearLocator())
    # ax1.xaxis.grid(True, which='major', linestyle='--', color='black', alpha=0.5)

    # add grid lines for the y-axis
    ax1.yaxis.grid(True, linestyle='--', color='black', alpha=0.5)

    # set the x-axis limits
    ax1.set_xlim(data['date'].min()-pd.Timedelta(days=30), data['date'].max()+pd.Timedelta(days=1))

    # set y lim
    ax1.set_ylim(-25, max(flights_per_day.max(), num_models.max()) + 10)

    # adjust the layout to prevent overlapping dates
    fig.autofmt_xdate()

    # Save
    folder = 'data/graphs'
    os.makedirs(folder, exist_ok=True)
    plt.savefig(f'{folder}/flights_per_day_tailnumbers.png')

    # show the plot
    plt.show()

    # clear
    plt.clf()

    return

def bar_chart_tailnumbers(data):
    # make a bar chart of the number of flights per aircraft_make_model
    fig, ax = plt.subplots(figsize=(15, 9))

    # count the number of flights per aircraft_make_model
    flights_per_model = data['aircraft_id'].value_counts()

    # plot the data
    flights_per_model.plot(kind='bar', ax=ax, color='blue', alpha=0.7)

    # set the title and labels
    ax.set_title('Number of Flights per Aircraft Tail Number', fontsize=20)
    
    ax.set_xlabel('Aircraft Tail Number', fontsize=15)
    ax.set_ylabel('Number of Flights', fontsize=15)

    # add grid lines
    ax.grid(True, linestyle='--', color='black', alpha=0.5)

    # Save
    folder = 'data/graphs'
    os.makedirs(folder, exist_ok=True)
    plt.savefig(f'{folder}/flights_per_tailnumber.png')

    # show the plot
    plt.show()

    # clear
    plt.clf()

    return

def bar_chart_tailnumbers_hours(data):
    # make a bar chart of the number of flights per aircraft_make_model
    fig, ax = plt.subplots(figsize=(15, 9))

    # count the number of flights per aircraft_make_model
    flights_per_model = data['aircraft_id'].value_counts()

    # count the number of flight hours per aircraft_make_model
    flight_hours_per_model = data.groupby('aircraft_id')['total_time'].sum()

    # plot the data
    flights_per_model.plot(kind='bar', ax=ax, color='blue', alpha=0.7)
    flight_hours_per_model.plot(kind='bar', ax=ax, color='red', alpha=0.7)

    # set the title and labels
    ax.set_title('Number of Flights and Hours per Aircraft Tail Number', fontsize=20)
    
    ax.set_xlabel('Aircraft Tail Number', fontsize=15)
    ax.set_ylabel('Number of Flights', fontsize=15)

    # add grid lines
    ax.grid(True, linestyle='--', color='black', alpha=0.5)

    # Save
    folder = 'data/graphs'
    os.makedirs(folder, exist_ok=True)
    plt.savefig(f'{folder}/flights_and_hours_per_tailnumber.png')

    # show the plot
    plt.show()

    # clear
    plt.clf()

    return

def bar_chart_tailnumbers_hours_and_flights(data):
    # make a bar chart of the number of flights per aircraft_make_model
    fig, ax = plt.subplots(figsize=(15, 9))

    # count the number of flights per aircraft_make_model
    flights_per_model = data['aircraft_id'].value_counts()

    # count the number of flight hours per aircraft_make_model
    flight_hours_per_model = data.groupby('aircraft_id')['total_time'].sum()

    # sort alphabetically
    flights_per_model = flights_per_model.sort_index()
    flight_hours_per_model = flight_hours_per_model.sort_index()

    # plot the data as two groups of bars
    width = 0.35
    x = range(len(flights_per_model))

    ax.bar(x, flights_per_model, width, label='Flights', color='blue', alpha=0.7)
    ax.bar([i + width for i in x], flight_hours_per_model, width, label='Hours', color='red', alpha=0.7)

    # set the title and labels
    ax.set_title('Number of Flights and Hours per Aircraft Tail Number', fontsize=20)
    
    ax.set_xlabel('Aircraft Tail Number', fontsize=15)
    ax.set_ylabel('Number of Flights', fontsize=15)

    # set x axis labels as the aircraft make and model
    ax.set_xticks([i + width/2 for i in x])
    ax.set_xticklabels(flights_per_model.index, rotation=90)

    # add grid lines
    ax.grid(True, linestyle='--', color='black', alpha=0.5)

    # add the legend
    ax.legend()

    # Save
    folder = 'data/graphs'
    os.makedirs(folder, exist_ok=True)
    plt.savefig(f'{folder}/flights_and_hours_per_tailnumber.png')

    # show the plot
    plt.show()

    # clear
    plt.clf()

    return


def flight_hour_distribution(data):
    # plot the distribution of flight hours
    fig, ax = plt.subplots(figsize=(15, 9))

    # plot the density curve
    sns.kdeplot(data['total_time'], color='blue', alpha=0.7)

    # set the title and labels
    ax.set_title('Distribution of Flight Hours', fontsize=20)
    ax.set_xlabel('Flight Hours', fontsize=15)
    ax.set_ylabel('Density', fontsize=15)

    # add grid lines
    ax.grid(True, linestyle='--', color='black', alpha=0.5)

    # x-axis limits
    ax.set_xlim(0, None)

    # Save
    folder = 'data/graphs'
    os.makedirs(folder, exist_ok=True)
    plt.savefig(f'{folder}/flight_hour_distribution.png')

    # show the plot
    plt.show()

    # clear
    plt.clf()

    return

def flight_distance_distribution(data):
    # plot the distribution of flight hours
    fig, ax = plt.subplots(figsize=(15, 9))

    # plot the density curve
    sns.kdeplot(data['distance_travelled'], color='blue', alpha=0.7)

    # add bar chart
    # sns.histplot(data['distance_travelled'], color='blue', alpha=0.7, bins=20)

    # set the title and labels
    ax.set_title('Distribution of Flight Distance', fontsize=20)
    ax.set_xlabel('Flight Distance', fontsize=15)
    ax.set_ylabel('Density', fontsize=15)

    # add grid lines
    ax.grid(True, linestyle='--', color='black', alpha=0.5)

    # x-axis limits
    ax.set_xlim(0, None)

    # Save
    folder = 'data/graphs'
    os.makedirs(folder, exist_ok=True)
    plt.savefig(f'{folder}/flight_distance_distribution.png')

    # show the plot
    plt.show()

    # clear
    plt.clf()

    return

def bar_passenger(data):
    # make a bar chart of the number of flights per passenger
    fig, ax = plt.subplots(figsize=(15, 9))

    # count the number of flights per passenger
    flights_per_passenger = data['passenger'].value_counts()

    # > 1 passenger
    flights_per_passenger = flights_per_passenger[flights_per_passenger > 1]

    # plot the data
    flights_per_passenger.plot(kind='bar', ax=ax, color='blue', alpha=0.7)

    # set the title and labels
    ax.set_title('Number of Flights per Passenger', fontsize=20)
    
    ax.set_xlabel('Passenger', fontsize=15)
    ax.set_ylabel('Number of Flights', fontsize=15)

    # add grid lines
    ax.grid(True, linestyle='--', color='black', alpha=0.5)

    # Save
    folder = 'data/graphs'
    os.makedirs(folder, exist_ok=True)
    plt.savefig(f'{folder}/flights_per_passenger.png')

    # show the plot
    plt.show()

    # clear
    plt.clf()

    return

def bar_flight_objective(data):
    # make a bar chart of the number of flights per objective
    fig, ax = plt.subplots(figsize=(15, 9))

    # count the number of flights per objective
    flights_per_objective = data['flight_objective'].value_counts()

    # plot the data
    flights_per_objective.plot(kind='bar', ax=ax, color='blue', alpha=0.7)

    # set the title and labels
    ax.set_title('Number of Flights per Objective', fontsize=20)
    
    ax.set_xlabel('Objective', fontsize=15)
    ax.set_ylabel('Number of Flights', fontsize=15)

    # add grid lines
    ax.grid(True, linestyle='--', color='black', alpha=0.5)

    # Save
    folder = 'data/graphs'
    os.makedirs(folder, exist_ok=True)
    plt.savefig(f'{folder}/flights_per_objective.png')

    # show the plot
    plt.show()

    # clear
    plt.clf()

    return

# def animated_flight_timeline(data):
#     # convert the date column to datetime
#     data['date'] = pd.to_datetime(data['date'])

#     # count the number of flights per day
#     flights_per_day = data['date'].value_counts().sort_index()
#     flights_per_day = flights_per_day.cumsum()

#     # create a figure and axis for the animation
#     fig, ax = plt.subplots(figsize=(15, 9))

#     def animate(i):
#         # clear the previous plot
#         ax.clear()

#         # plot the data up to the current index
#         ax.plot(flights_per_day[:i+1])

#         # set the title and labels
#         ax.set_title('Cumulative Flights per Day')
#         ax.set_xlabel('Date')
#         ax.set_ylabel('Number of flights')

#         # format the x-axis to show the date
#         ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
#         ax.xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=180))
#         plt.xticks(rotation=45)

#         # set the x-axis limits
#         if data['date'].min() == flights_per_day.index[i]:
#             ax.set_xlim(data['date'].min(), flights_per_day.index[i] + pd.Timedelta(days=1))
#         else:
#             ax.set_xlim(data['date'].min(), flights_per_day.index[i])
            
#     # create the animation
#     ani = animation.FuncAnimation(fig, animate, frames=len(flights_per_day), interval=200)

#     # Save
#     folder = 'data/graphs'
#     os.makedirs(folder, exist_ok=True)
#     ani.save(f'{folder}/animated_flights_per_day.gif', writer='pillow')  # Save as GIF instead of MP4

#     # show the animation
#     plt.show()

#     # clear
#     plt.clf()

#     return

date_markers = [
    {
        'date': '2009-03-18',
        'label': 'First Flight',
        'type': 'Start',
        'offset': 50
    },
    {
        'date': '2012-04-18',
        'label': 'Started Flight School',
        'type': 'Flight',
        'offset': 1500
    },
    {
        'date': '2012-07-16',
        'label': 'First Solo',
        'type': 'Flight',
        'offset': 1400
    },
    {
        'date': '2012-07-18',
        'label': 'First Cross Country',
        'type': 'Flight',
        'offset': 1300
    },
    {
        'date': '2012-09-14',
        'label': 'Night Flight!',
        'type': 'Flight',
        'offset': 1200
    },
    {
        'date': '2013-02-05',
        'label': 'Solo Cross Country',
        'type': 'Flight',
        'offset': 1100
    },
    {
        'date': '2013-02-27',
        'label': 'Private Pilot',
        'type': 'Flight',
        'offset': 1000
    },
    {
        'date': '2013-04-23',
        'label': 'Multi Engine Training',
        'type': 'Flight',
        'offset': 900
    },
    {
        'date': '2013-05-27',
        'label': 'Checkride 2/8',
        'type': 'Flight',
        'offset': 800
    },
    {
        'date': '2013-10-23',
        'label': 'Checkride 3/8',
        'type': 'Flight',
        'offset': 700
    },
    {
        'date': '2014-01-17',
        'label': 'Checkride 4/8',
        'type': 'Flight',
        'offset': 600
    },
    {
        'date': '2014-02-21',
        'label': 'Checkride 5/8',
        'type': 'Flight',
        'offset': 500
    },
    {
        'date': '2014-03-14',
        'label': 'Checkride 6/8',
        'type': 'Flight',
        'offset': 400
    },
    {
        'date': '2014-07-08',
        'label': 'Checkride 7/8',
        'type': 'Flight',
        'offset': 300
    },
    {
        'date': '2014-07-08',
        'label': 'Offical CFI 8/8',
        'type': 'Flight',
        'offset': 200
    },
    {
        'date': '2014-08-12',
        'label': 'First Student',
        'type': 'Flight',
        'offset': 100
    },
    {
        'date': '2019-05-14',
        'label': 'Back',
        'type': 'Back',
        'offset': 100
    },
    {
        'date': '2020-03-17',
        'label': 'Back',
        'type': 'Back',
        'offset': 100
    },
    {
        'date': '2020-09-22',
        'label': 'Retired',
        'type': 'Retired',
        'offset': 100
    },
    {
        'date': '2023-06-12',
        'label': 'hours for exam',
        'type': 'Exam',
        'offset': 100
    },
]

data = pd.read_csv('data/output/processed_flight_data.csv')
print(data)
# flights_per_year(data)
# flight_timeline(data, date_markers)
# flight_timeline_num_models(data, date_markers)
# bar_chart_models_hours_and_flights(data)
# flight_timeline_num_tailnumbers(data, date_markers)
# bar_chart_tailnumbers_hours_and_flights(data)
# flight_hour_distribution(data)
# flight_distance_distribution(data)
# bar_passenger(data)
# bar_flight_objective(data)
# flight_timeline_hours(data, date_markers)


# animated_flight_timeline(data)