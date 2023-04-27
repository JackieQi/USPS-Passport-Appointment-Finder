''' find available passport appointments from usps website '''
import datetime
import json
import sys
import requests


class USPSAppointmentChecker:
    ''' check available appointments for the next 30 days '''
    # root url
    ROOT_URL = "https://tools.usps.com/UspsToolsRestServices/rest/v2"
    MAX_NUMBER_OF_DAYS_TO_CHECK = 30
    appointments = []  # store all available appointments

    # declare request headers
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
        "sec-ch-ua-mobile": "?0",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/json; charset=UTF-8"
    }

    def __init__(self):
        self.zip_code = None
        self.start_date = None
        self.nearby_facilities = []

    def run(self):
        """Run the main program."""
        # get user input (zip code and start date)
        self.get_user_input()

        start_date_string = self.normalize_date(self.start_date)

        # find nearby facilities
        self.nearby_facilities = self.find_nearby_facilities(start_date_string)

        # check appointments for start date
        appointments = self.check_appointments_for_next_days(
            self.start_date, 0)

        if appointments:
            print(
                f"!!! Appointments found !!!\nResult: {json.dumps(appointments, indent=2)}")
        else:
            print("No appointments found")
            user_input = input(
                f"You want to check for next few days (max {self.MAX_NUMBER_OF_DAYS_TO_CHECK} days from today)? (y/n):")
            if user_input == 'y':

                input_days = input(
                    f"How many days do you want to check? (1-{self.MAX_NUMBER_OF_DAYS_TO_CHECK}):")
                if input_days.isdigit():
                    days = int(input_days)
                    if days > self.MAX_NUMBER_OF_DAYS_TO_CHECK:
                        print(
                            f"Maximum number of days is {self.MAX_NUMBER_OF_DAYS_TO_CHECK}")
                        sys.exit()
                else:
                    print("Please enter a number")
                    sys.exit()

                appointments = self.check_appointments_for_next_days(
                    self.start_date, int(input_days))

                if appointments:
                    print(
                        f"!!! Appointments found !!!\nResult: {json.dumps(appointments, indent=2)}")
                else:
                    print("No appointments found")
            else:
                sys.exit()

    def get_user_input(self):
        """Get ZIP code and start date from user input."""
        self.zip_code = input(
            "Please enter your current zip code (e.g. 12345):")
        self.start_date = input(
            "Please enter the date you want to start checking (e.g. 04/01/2021):")

    # call facilities API to get facility id and name tuples in a list

    def find_nearby_facilities(self, start_date):
        """Get facilities"""
        url = f"{self.ROOT_URL}/facilityScheduleSearch"

        # define request payload
        payload = {
            "city": "",
            "date": start_date,
            "zip5": self.zip_code,
            "numberOfAdults": "1",
            "numberOfMinors": "0",
            "poScheduleType": "PASSPORT",
            "radius": "20",
            "state": ""
        }

        response = self.make_request(url, payload)

        # check error from response
        if 'error' in response:
            print(f"Server Error: {response['error']}")
            sys.exit()

        # parse response - store each facility id and name in a tutple in a list
        facilities = [(location['fdbId'], location['name'])
                      for location in response['facilityDetails']]
        print(f'Nearby facilities: {json.dumps(facilities, indent=2)}')
        return facilities

    # seearch appointments from each facility

    def search_appointment_dates_per_facility(self, facility_id, name, date):
        """Search appointments"""
        url = f"{self.ROOT_URL}/appointmentTimeSearch"

        # define request payload
        payload = {
            "date": date,
            "productType": "PASSPORT",
            "numberOfAdults": "1",
            "numberOfMinors": "0",
            "excludedConfirmationNumber": [""],
            # If you use array of facility ids here, for some reason, even you may have availability \
            # from one facility, it will not return it. So just use one facility id instead
            "fdbId": [facility_id],
            "skipEndOfDayRecord": "true"
        }

        response = self.make_request(url, payload)
        # parse response
        appointment_time_details = response['appointmentTimeDetailExtended']

        # filter appointments with status available
        available_appointments = [
            x for x in appointment_time_details if x['appointmentStatus'] == 'Available']

        if available_appointments:
            date_time_dictionary = {}
            # only store start time since every slot has 15 min
            available_time_slots = [x['startTime']
                                    for x in available_appointments]
            # store appointment slots with a date as key
            date_time_dictionary[date] = available_time_slots

            facility_name_appointments_dictionary = {}
            if date_time_dictionary:
                facility_name_appointments_dictionary[name] = date_time_dictionary
                return facility_name_appointments_dictionary

        return None

    # check appointments for up to next 30 days
    # if number_of_days == 0, means we only check input date
    # if number_of_days > 0, means we check input date and next number_of_days

    def check_appointments_for_next_days(self, start_date, number_of_days):
        """Check appointments for next number of days"""
        # initialize date from string
        date_object = datetime.datetime.strptime(start_date, '%m/%d/%Y')
        updated_date_object = date_object.date()

        # initialize result dictionary
        result = {}

        more_days_to_check = number_of_days > 0

        if more_days_to_check:
            # check for next number of days
            for _ in range(number_of_days):
                # check next day
                updated_date_object = updated_date_object + \
                    datetime.timedelta(days=1)

                date_to_display = updated_date_object.strftime('%m/%d/%Y')
                print(
                    f"Checking for appointments on {date_to_display}")

                # convert date to string
                updated_date_string = f"{updated_date_object.year}{updated_date_object.month:02d}{updated_date_object.day:02d}"
                new_appointments = self.search_appointments_with_date(
                    updated_date_string)

                if new_appointments:
                    print(
                        f"Found appointments for {date_to_display}, adding to the final result")
                    result = dict(self.merge_dicts(result, new_appointments))
                else:
                    print(f"No appointments for {date_to_display}")
        else:
            date_to_display = updated_date_object.strftime('%m/%d/%Y')
            print(
                f"Checking for appointments on {date_to_display}")
            # convert date to string
            updated_date_string = f"{updated_date_object.year}{updated_date_object.month:02d}{updated_date_object.day:02d}"
            new_appointments = self.search_appointments_with_date(
                updated_date_string)

            result.update(new_appointments)

        return result

    # check appointments from each facility

    def search_appointments_with_date(self, date):
        """Search appointments with date"""
        result = {}
        # search appointments from each facility
        for facility in self.nearby_facilities:
            appointments_per_facility_per_day = self.search_appointment_dates_per_facility(
                facility[0], facility[1], date)

            if appointments_per_facility_per_day:
                # result contains facility name as key and appointments per day as value
                facility_name = facility[1]
                existing_facility_names = result.keys()
                # if facility name is in result, update appointments per day
                if facility_name in existing_facility_names:
                    result[facility_name].update(
                        appointments_per_facility_per_day)
                else:
                    result.update(appointments_per_facility_per_day)
        return result

    # make API request

    def make_request(self, url, payload, retry=3):
        """Make http request with retry"""
        try:
            response = requests.post(
                url, headers=self.headers, data=json.dumps(payload), timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as error:
            print(f"{error}. Retrying...")
            if retry > 0:
                return self.make_request(url, payload, retry - 1)

            print("Failed to make the request after retrying.")
            sys.exit(1)
        except requests.exceptions.RequestException as error:
            print(f"{error}. Failed to make the request.")
            sys.exit(1)

    # normalize date in string to YYYYMMDD format in string

    def normalize_date(self, date_string):
        """Normalize the date"""
        # initialize date from string
        date_object = datetime.datetime.strptime(date_string, '%m/%d/%Y')
        normalized_date = f"{date_object.year}{date_object.month:02d}{date_object.day:02d}"
        return normalized_date

    def merge_dicts(self, dict1, dict2):
        """Merge two dictionaries and return new one"""
        for k in set(dict1.keys()).union(dict2.keys()):
            if k in dict1 and k in dict2:
                if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                    yield (k, dict(self.merge_dicts(dict1[k], dict2[k])))
                else:
                    # If one of the values is not a dict, you can't continue merging it.
                    # Value from second dict overrides one in first and we move on.
                    yield (k, dict2[k])
                    # Alternatively, replace this with exception raiser to alert you of value conflicts
            elif k in dict1:
                yield (k, dict1[k])
            else:
                yield (k, dict2[k])


if __name__ == '__main__':
    # initialize USPS appointment checker
    appointment_checker = USPSAppointmentChecker()
    appointment_checker.run()
