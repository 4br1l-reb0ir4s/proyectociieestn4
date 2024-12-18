from datetime import datetime

def get_years():
    tuple_years = []
    year = datetime.today().year
    years = list(range(year + 5, 1959, -1))
    for year in years: 
        tuple_years.append((str(year), year))
    return tuple_years

def get_years_graduate():
    tuple_years_graduate = []
    year = datetime.today().year
    years = list(range(year, 1959, -1))
    for year in years: 
        tuple_years_graduate.append((str(year), year))
    return tuple_years_graduate