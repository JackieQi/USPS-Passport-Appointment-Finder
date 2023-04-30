'''cli for appointment checker'''
import argparse
import datetime
import json
import passport_appointment_finder as paf


class AppointmentCheckerCLI(argparse.Action):
    '''cli for appointment checker'''

    def __init__(self, option_strings=None, dest=None, nargs=None, **kwargs):
        super().__init__(option_strings, dest, **kwargs)
        self.checker = paf.USPSAppointmentChecker()

    def __call__(self, parser, namespace, values, option_string=None):
        self.find_closest_appointment_with_zip_code(values)

    def find_closest_appointment_with_zip_code(self, zip_code):
        """Find closest appointment with ZIP code."""
        # get user input (zip code and start date)
        self.checker.zip_code = zip_code

        # covert date to string
        today = datetime.date.today()
        # 05/01/2021
        start_date = f"{today.month:02d}/{today.day:02d}/{today.year}"
        # 20210501
        start_date_variation = f"{today.year}{today.month:02d}{today.day:02d}"
        self.checker.start_date = start_date

        # find nearby facilities
        self.checker.nearby_facilities = self.checker.find_nearby_facilities(
            start_date_variation)

        # check appointments for start date
        appointments = self.checker.check_appointments_for_next_days(
            start_date, 0)

        # if no appointments found, ask user to check more days
        if appointments:
            print(
                f"!!! Appointments found !!!\nResult: {json.dumps(appointments, indent=2)}")
        else:
            self.checker.ask_user_to_check_more_days()


parser = argparse.ArgumentParser()
parser.add_argument('--zipcode', action=AppointmentCheckerCLI,
                    help='zip code', required=False)
parser.parse_args()
