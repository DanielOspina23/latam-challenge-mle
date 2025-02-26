from datetime import datetime


class Preprocessor:

    @staticmethod
    def get_period_day(date):
        date_time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').time()
        morning_min = datetime.strptime("05:00", '%H:%M').time()
        morning_max = datetime.strptime("11:59", '%H:%M').time()
        afternoon_min = datetime.strptime("12:00", '%H:%M').time()
        afternoon_max = datetime.strptime("18:59", '%H:%M').time()
        evening_min = datetime.strptime("19:00", '%H:%M').time()
        evening_max = datetime.strptime("23:59", '%H:%M').time()
        night_min = datetime.strptime("00:00", '%H:%M').time()
        night_max = datetime.strptime("4:59", '%H:%M').time()

        if morning_min < date_time < morning_max:
            return 'mañana'
        elif afternoon_min < date_time < afternoon_max:
            return 'tarde'
        elif (
                (evening_min < date_time < evening_max) or
                (night_min < date_time < night_max)
        ):
            return 'noche'

    @staticmethod
    def is_high_season(date):
        year = int(date.split('-')[0])
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        range1_min = datetime.strptime('15-Dec', '%d-%b').replace(year=year)
        range1_max = datetime.strptime('31-Dec', '%d-%b').replace(year=year)
        range2_min = datetime.strptime('1-Jan', '%d-%b').replace(year=year)
        range2_max = datetime.strptime('3-Mar', '%d-%b').replace(year=year)
        range3_min = datetime.strptime('15-Jul', '%d-%b').replace(year=year)
        range3_max = datetime.strptime('31-Jul', '%d-%b').replace(year=year)
        range4_min = datetime.strptime('11-Sep', '%d-%b').replace(year=year)
        range4_max = datetime.strptime('30-Sep', '%d-%b').replace(year=year)

        if ((range1_min <= date <= range1_max) or
                (range2_min <= date <= range2_max) or
                (range3_min <= date <= range3_max) or
                (range4_min <= date <= range4_max)):
            return 1
        else:
            return 0

    @staticmethod
    def get_min_diff(data):
        date_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
        date_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
        min_diff = ((date_o - date_i).total_seconds()) / 60
        return min_diff
