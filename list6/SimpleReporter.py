from TimeSeries import TimeSeries

class SimpleReporter():
    def analyze(self, series: TimeSeries):
        return [f"Info:{series.indicator} at {series.station_code} has mean {series.mean} and standard deviation {series.stddev}"]
    


def main():
    series = TimeSeries()
    pass

if __name__ == "__main__":
    main()