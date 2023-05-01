'''cli for appointment checker'''
import argparse
import passport_appointment_finder as paf


class AppointmentCheckerCLI(argparse.Action):
    '''cli for appointment checker'''

    def __init__(self, option_strings=None, dest=None, nargs=None, **kwargs):
        super().__init__(option_strings, dest, **kwargs)
        self.checker = paf.USPSAppointmentChecker()

    def __call__(self, parser, namespace, values, option_string=None):
        self.checker.find_closest_appointment_with_zip_code(values)


parser = argparse.ArgumentParser()
parser.add_argument('--zipcode', action=AppointmentCheckerCLI,
                    help='zip code', required=True)
parser.parse_args()
