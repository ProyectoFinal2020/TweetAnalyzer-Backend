
from ...models.chartValue import ChartValue

def merge(frequencies):
    dtosList = list()
    for key, value in frequencies.items():
        dtosList.append(ChartValue(label=key, value=value)) 
    return sorted(dtosList, key=lambda i: i.value, reverse=True)