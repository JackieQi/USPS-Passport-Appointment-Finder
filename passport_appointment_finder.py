''' find available passport appointments from usps website '''
import configparser
import datetime
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

config = configparser.ConfigParser()


class USPSAppointmentChecker():
    ''' check available appointments for the next 30 days '''

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
        self.appointments = []  # store all available appointments
        self.zip_code = None
        self.start_date = None
        self.nearby_facilities = []

        # read config file and load config
        config.read('config.cfg')
        self.root_url = config.get('DEFAULT', 'ROOT_URL')

        self.max_number_of_days_to_check = int(
            config.get('DEFAULT', 'MAX_NUMBER_OF_DAYS_TO_CHECK'))
        self.max_number_of_threads = int(
            config.get('DEFAULT', 'MAX_NUMBER_OF_THREADS'))

    def run(self):
        """Run the main program."""
        # get user input (zip code and start date)
        self.get_user_input()

        # normalize start date to API request
        start_date_string = self.normalize_date(self.start_date)

        # find nearby facilities
        self.nearby_facilities = self.find_nearby_facilities(start_date_string)

        # check appointments for start date
        self.appointments = self.check_appointments_for_next_days(
            self.start_date, 0)

        # if no appointments found, ask user to check more days
        if self.appointments:
            print(
                f"!!! Appointments found !!!\nResult: {json.dumps(self.appointments, indent=2)}")
            # ask user if they want to book an appointment
            self.ask_user_to_book_an_appointment()
        else:
            self.ask_user_to_check_more_days()

    # get user input from the command line

    def get_user_input(self):
        """Get ZIP code and start date from user input."""
        self.zip_code = input(
            "Please enter your current zip code (e.g. 12345):")
        self.start_date = input(
            "Please enter the date you want to start checking (e.g. 04/01/2023):")

    # call facilities API to get facility id and name tuples in a list

    def find_nearby_facilities(self, start_date):
        """Get facilities"""
        url = f"{self.root_url}/facilityScheduleSearch"

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

    def search_appointments_on_date_per_facility(self, facility_id, name, date):
        """Search appointments"""
        url = f"{self.root_url}/appointmentTimeSearch"

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

    # check earliest apponintments from nearby facilities

    def find_closest_appointment_with_zip_code(self, zip_code):
        """Find closest appointment with ZIP code."""
        # get user input (zip code and start date)
        self.zip_code = zip_code

        # covert date to string
        today = datetime.date.today()
        # 05/01/2021
        start_date = f"{today.month:02d}/{today.day:02d}/{today.year}"
        # 20210501
        start_date_variation = f"{today.year}{today.month:02d}{today.day:02d}"
        self.start_date = start_date

        # check appointments for start date
        appointments = self.find_earliest_appointments(
            start_date_variation)

        # if no appointments found, ask user to check more days
        if appointments:
            print(
                f"!!! Appointments found !!!\nResult: {json.dumps(appointments, indent=2)}")
        else:
            print("No appointments for next 30 days. Please check later.")

    # find earliest appointment date from specific facility
    def find_earliest_appointments(self, start_date):
        """Find earliest appointment date from nearby facilities."""

        self.nearby_facilities = self.find_nearby_facilities(start_date)

        result = {}
        # search appointments from each facility in parallel
        with ThreadPoolExecutor(max_workers=self.max_number_of_threads) as executor:
            # get appointments from each facility
            threads = []

            for facility in self.nearby_facilities:
                threads.append(executor.submit(
                    self.get_available_appointment_date_per_facility, facility[0]))

            for index, task in enumerate(as_completed(threads)):
                try:
                    task_result = task.result()
                except Exception as exception:
                    print(f"Exception: {exception}")
                    continue

                if task_result:  # find appointment date from specific facility
                    appointments = self.search_appointments_on_date_per_facility(
                        facility[0], facility[1], task_result)

                    print(f"the result is: {appointments}")
                    # TODO: check all appointment time from the date in response above
        return result

    # this is used to find the earliest appointment date from a specific facility
    def get_available_appointment_date_per_facility(self, facility_id):
        '''find earliest appointment date from specific facility'''

        url = f"{self.root_url}/appointmentDateSearch"

        payload = {
            "numberOfAdults": "1",
            "numberOfMinors": "0",
            "fdbId": facility_id,
            "productType": "PASSPORT"
        }

        response = self.make_request(url, payload)

        # check error from response
        if 'error' in response:
            print(f"Server Error: {response['error']}")
            sys.exit()

        return response['dates']

    # check with user if more days need to be checked

    def ask_user_to_check_more_days(self):
        """Ask user to check more days if no appointments found."""
        if self.appointments:
            print(
                f"!!! Appointments found !!!\nResult: {json.dumps(self.appointments, indent=2)}")
            self.ask_user_to_book_an_appointment()
        else:
            print("No appointments found")
            selection = self.handle_check_more_days_selection()
            if selection:
                self.handle_selection_of_days_input()
            else:
                print("Exiting...")
                sys.exit()

    # handle user input for checking more days

    def handle_check_more_days_selection(self):
        """Validate user input"""
        user_input = input(
            f"You want to check for next few days (max {self.max_number_of_days_to_check} days from today)? (y/n):")

        if user_input == 'y':
            return True
        if user_input == 'n':
            return False

        print("Please enter y or n")
        return self.handle_check_more_days_selection()

    # handle user input for number of days to check

    def handle_selection_of_days_input(self):
        """Handle user input for number of days to check."""
        input_days = input(
            f"How many days do you want to check? (1-{self.max_number_of_days_to_check}):")
        if input_days.isdigit():
            days = int(input_days)
            if days > self.max_number_of_days_to_check:
                print(
                    f"Maximum number of days is {self.max_number_of_days_to_check}")
                self.handle_selection_of_days_input()
        else:
            print("Please enter a number")
            self.handle_selection_of_days_input()

        self.appointments = self.check_appointments_for_next_days(
            self.start_date, int(input_days))

        if self.appointments:
            print(
                f"!!! Appointments found !!!\nResult: {json.dumps(self.appointments, indent=2)}")
            self.ask_user_to_book_an_appointment()
        else:
            print("No appointments found")
            sys.exit()

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

        # check more appointments for next number of days
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
        # search appointments from each facility in parallel
        with ThreadPoolExecutor(max_workers=self.max_number_of_threads) as executor:
            # get appointments from each facility
            threads = []

            for facility in self.nearby_facilities:
                threads.append(executor.submit(
                    self.search_appointments_on_date_per_facility, facility[0], facility[1], date))

            for index, task in enumerate(as_completed(threads)):
                try:
                    task_result = task.result()
                except Exception as exception:
                    print(f"Exception: {exception}")
                    continue

                if task_result:
                    appointments_per_facility_per_day = task_result

                    if appointments_per_facility_per_day:
                        # result contains facility name as key and appointments per day as value
                        facility_name = self.nearby_facilities[index]
                        existing_facility_names = result.keys()
                        # if facility name is in result, update appointments per day
                        if facility_name in existing_facility_names:
                            result[facility_name].update(
                                appointments_per_facility_per_day)
                        else:
                            result.update(appointments_per_facility_per_day)
        return result

    def ask_user_to_book_an_appointment(self):
        print("Please provide following information for the appointment")
        date = input("Date:")
        time = input("Time:")
        facility_id = input("Facility ID:")

        self.book_appointment(facility_id, date, time)

    # book appointment on a specific date and time
    def book_appointment(self, facility_id, date, time):
        first_name = config.get('DEFAULT', 'FIRST_NAME')
        last_name = config.get('DEFAULT', 'LAST_NAME')
        email = config.get('DEFAULT', 'EMAIL')
        phone = config.get('DEFAULT', 'PHONE')  # format: 650-123-4567
        number_components = phone.split('-')

        if len(number_components) < 3:
            print("Please use expected phone number format.")
            return

        url = f"{self.root_url}/createAppointment"

        payload = {
            "customer": {
                "firstName": first_name,
                "lastName": last_name,
                "regId": ""
            },
            "customerEmailAddress": email,
            "customerPhone": {
                "areaCode": number_components[0],  # 650
                "exchange": number_components[1],  # 123
                "line": number_components[2],  # 4567
                "textable": "true"
            },
            "date": date,  # 20230524
            "fdbId": facility_id,  # 1356376
            "numberOfAdults": "1",
            "numberOfMinors": "0",
            "schedulingType": "PASSPORT",
            "serviceCenter": "Web Service Center",
            "time": time,  # 02:00 pm
            "passportPhotoIndicator": 1
        }

        extra_headers = {
            "x-jfuguzwb-a": "rj4p8c433hs6oPt5nTxU6cVzceq0g8Yoj5wX=bB=jv0S3yZgL7PkdZOOhEPWNS_L8nBZI6=Ija=1pq786jv1D0tolDnPO8mAmjBCI_DpjTMKH7dG_KE=v6TDa2nt5eAStcRy4wWw8jlPYNOvRRlGfTls-E21PehAnQanUxOLpWLWj__IThKEAhS_t6RgZmGla4KkGuu8Eu36PQ6YMyMlAAgXyeAdY3pTjf7dCIds8zG5BrcOCoKfIo8GbaM=62t396hkh0LLXmPCTGlIqK=4JWCRFh1Fh6515l4QKojzjwUPfq=Ay=RucglLf7QCH8VplXXhuQI1jdvC5pU25dTYrNqIXSN7w1jbcGwGLJ5TPMEuKtKoJL1RWhODqokLYe7j1=1F5TkAX=qRVw1KsRzo9BpwQ_cpl8K0vq6aqs9kN-IBokFINH4VTKswfXMUxWZWkpqF=1sI7=8IkV3gKwGscskNN8Z0lCXPhk_qftXVE7QkuESIyjQw969hNxVXkGqvfgFqsq3DaVIhgNnpq8Rrj8FgAgwog6_yq2I8btU1dOJx7zXN3AA9IkgU2VtClaV9CkoPtRh1HFzj_Ldp6X6m8A8DJCPSvGqRvuxFcQ0_4wrR1PWwOm8Qw4R9ghR69dgnhgCzN8j3NNfjda0VXV2RqOsArQuDx515YG4U38mr4I2Ha735YtUxx3=mhAzGCjyp1nsrxKckEP1YQxUovczqs3dkGUVu9RTotlZ1gL-lnUDjXc3jxve3o_s=Fxo_kJpG3_PwPGembmRy0HONf7ZmpmJEAvg9bWFrjtao_aAXQPuvuBaU81LOT4G-=mmD-7G3EY0wFzHS1R1EoPcC7xWd-zTfzJnl8qbq--Zv3DsYKWqKnZt3D4-UzJLFy4lgXC3DCjQmsn=NHlcL7Q5kphaxhwkC5ySx3SRB_RpXX882PMGQOVKtVtCHXCKNV2I33RuoQRorOLPuVT_619pQFPKcyFRGcAM7dkXazYfuczPT5EQBGyQ9jg0mKuQfIGe-AEy-7BXMF0TxDf1ZfwjaSUOQHyGY0rX88rgc3MaKULZzBX7AoavIxCLFe_oqec6-svEEwjPcnF5=GWIk30Y5JulDt-jttJvCR6P3k2DnJQRAU9_a863WELZ8OT6DmoM6LrPjlR1cnclEvdS_qr=gb37TN8TIcda1Hx_cLcRCDbHHCF11lMM_7ZuJYZo6=SsbT5fwv71G3VgFz_SsJ5GSNeJQUoqd_MR4ZleJLdQHJ-gwb1Im_b8tSZMYO5fS6ylztbLoWTYcEqow9YSkpVMAB6M_p=rL1za0efZKQwzwRemHpCugmFhT22paITCghJv9tqyT1PDYjPx8bE0v-CjRyMj8CWs8svwB4vF46nzGHMmHSW_9D7CsXKYy6U-=c2Vj2OxljlZIaoFYx4kE9Ka8kZOS3Q5IgZg=aR1MMgwWWaLLfIoeFcuntwOk89rEacXKxYoxZYdphVBJ69XH5cxSfd8M8d1=dyJ787Xze-=ORSClZWDyhz6H2QpVeuNHISQJGWntV40JwhqC6W8lhJwxXVoIB442vae54smBl120VNFMcvzTpW4lztR1Ks-vmfZUyO3WOJ7-2_8trr1n=54PkmO0ucmtoDNWbFvAoHmZs-tyDanU-UwsVhlennt8ffjo6dHybhZPedbyW=z28mv9k25fVvJ=aqzbKF=IKb20EHNpbkZavelrMBb9chZBQ8FtlTnASUxop=7G7CD0yGv0=uVu2ThsnS9LYQDzUnqySkWxbv=DFtPLT4XjsD6doII0=KU1v6uFBjWz194Y8ynGyUGqPEaFWO_GRf_Veg4QY5ntnaIGJMnIwMX-1wsUbm2uXpjPT1VeMAPrg2nk68j0hTp9UWubK6AA7BgOTs5JSumj1-ayhvNs6Wb_N-KwNBeYjHtqeqvqojUAC-Qfy7xa0L-gS5Njg5Am5S=PMxYAv2JS28XKL4UWeWbkWS-=CnIBCyDUZZeVDEhpmEKW8DaHIRBbp2HRsPnpqhMN7OlQkkJVob52spXcGWSBwkx0Uzu8mzO6lhALHgqK3C3qE6cUDnNN6Fab=xf_HYUB04a5rbeFhgJyshycv_ID3DYTrCRh7sPKD65gF=F=0xHSYcracL6DH26s-kb9wMbtuMxaLDPF=Z_cxmAAlj20UTQZ1Yv=J90TNs4wnhzh5a1DDXK0aJprDYXykO=e5yeeuD4qSb70t9BJ=HdzdZXbGL=KvCAmdrA6f6UcTXkFIAFam3K0KdEc9r3Y4xe-ZxOl4n5N5MXsqeWSWIkrhJXCbw5RTt0lyQ9JhcOGPS4L3VWWWE7v=_S8ykRMdH9hjHOR7tc7cWKyuqLJZ61l1X=U7gn1f65nhX_jRGR5mwTI5WT1akVhs9sblWoyHsYqdbUjryXq2KRmxh19djMMjPvOG05Fr-RFPYBjNtkOAH3=Hrb8B-s5KKue28hWP54KkhIYTmk2Erf7zlvIUxwM5g6_5tGg31jmAAVLmX-zC4WszqqNbbOMRbCwEeUs0d6u5vRAJ6qL9cSM18zZXyYmxb5z1Wo43bcM7M6UWCp_QN3qTBzrnNfM23I7TAyqQJcnMrfQhbhQs8r_CUIHpCnIKJP-_bKwTITL1Ry_wvdqGrfOnevEKJrGlARBfVDq9xHWYp=b=XEoq6OH4hpfrEnFFMzhxsAyZ1_eam9VEU9GrhD2OxoK4YXGS6uHQCDhJzRmpAstt7MkY1KK_4k8UTM4TIZRf-tGSg-fApos8yMN4E5MZbYehfUVEqEmnU5N2gF3rNwhzxF=dRqohmFLzNtRbm49wkWCPDLHbGFXTK4Kma4TSEuHKWBFmn7GMYjy_rZYDloApNVncCxblnOJxtKyvA2PIpEhfaZdNBJ48ZjPKhjFw89ktWEndb3DwIOfrXQlxR9U6yuSTG8u035C9vY7CvNdePnt0I8jd2oLIV-_bMoP2uERN=6m0kYyeg2yn2BueNVvIexTAWT6TUW=fX2QdWCboq_8kS_RWpSD56=39KEXF5kzd9cX4n1enMKrlQnoWRRa9XZuWnVLDnrLR45MIc43u0GA2dOzpWX-lZaYltDtlmuqNHneCl0PbWckNsHmRcHlfjbInGfdRb5qJ9WEeUhn_RlnSW9skaEwtRbb4Rc_vMVgFNB6xw=rF097Jo61STHgTPYoz598fXktKAzJCoK8glp=-EJfUxOM5pJrFhXsxhW-pacRlg71_A9Mm-0VzOWWDzr5SMbUZa99KxWSFlUhb9mYtaenOIFVYH48vAyH7R=G3GfbzL8xtmpMutctawf3o5OOXhIPgB=HoLmQvTjn5OTrjjuW-GLn=WfVkQYXS0LJ8XdT0XbGFu4Nbn4HJBGwc=3k=3khJm=v0yyCHBNF0R0ynogYYN_aCCol7hSUz9JHjOT0sJT3XC5MfIUDQksbQX_5ZxaVPY6dDgyVM8RlxGLpzXWNLFFvoETU465Ad0ff=AqWrgEWjv4GLn2jo1WgDLTOo9RRqtmFfFl9uF73h9jnLgF_Hs-0wv_YdqVfIHsste1X9KlT-Rc4BBMUPExF8TyLlM9qaN-3lBjxbU88M-pWfTkp3Qjd4I72GXaUZpEsC5IRqgFWQXtwqx35etK7wT4OGhJGXLk5lWPX6La=QQ8uoH484tnEBgc41Fp7TWaht19cIxnhQx5leK_2tWsUeYPy=Rn1G60awY7AXCyop-4t7Ok9VJJx35ARY85PqUvCrklrAtDAx7JK70Ar9eHf-scw2eqDTN2k9dfBpPGZtRYRrmfgu_YjnAaCQuQQP6wnk4T7AEm_dpvxeAsaBLRF6o1PkQVGtUzCmTPa05NN4_t8_afACfnmRy3AyF3ry-WTs16sNq8W8CgcRuWrNymaNYK-Xnoab_Gh9=u-AfY3gt=CD8ZkbhZ6K2PdPS0jUMhgZoEmoC04uy5te9fH0wXVY5DrBhFENjw7ovf2TI9sLqdNzpXk8tMfd_vNmAsjT-JRxYsSuHRwrYH5B0f7ZKmdopdYJswYrwTwkcHkpkjOBRg4CZ-pon1uPk9hGMMKOL-lVGHCGuqORLSYC5HGQUmShYfM0uAgBDhZWBcGJ2_mwav=eotAE1OR4NPW2hIrRpqmVPqQsM9D4ybawHGx3U9x8SpzqMQTNwh_BMJgeSMw-dxNqLHVL=DXFPbNGhQK86TT=x_FvzD_dkeoPeOr0WCrUU6PMl7U4wIpfZhWB_NvrAoPUg4arbJFsoaDEfoTpu=tbz34w34pdnMmm8S2dahevjIlDFmhdC-OWv6OBvx2yTVdrYbGs0u8Glrzdho=PHjwHz3xLLVEDOzORupdseGxomUdyE-D8jRSJZpm-0KBvrB800TWpUqfbQfBlDC4yTM5eP=qBdvm=ok-_YD49xSO-yvqMNQl_ICE97I5BFBwSPNKrhpHZa_rwbA1UsS9OEdfTKyqQ056ocqujHdggqWXn_6sksU1Uxx9QFN4RTE88eUk8EfH8l-C1g_9ZSmf-JxlvTGKP0S=uYjL4h4Z4lUMP4Eq-EwukMVGvKVyhU74gvEZr3xgcUjVCqRBRgMDm0LrBln7S9FqNw5ynD7yKp6=2P=8ABqhQ4IrA8GZJWAxp634ZlAY106QHUEbakoJejJ7asX_9yJpvKhhVL-bCG85Gy4JHJenNsVqX1fEHjU0pQxnIv6Kmf6cLUZvpNVrZkBtgrjRHhVYl1WMX-dhQJYWTfzWAphMdZN8Zv0kmrjZ_dZ286YVqUvxcsOK0QwvLcQTSDnbAHlUPjlL5nGgfNTK1RYQWtEbALoLbroB5TZCn8jRUXSuRRUuB8EBIRvU0ZWDCI6=1SU3rO7RX7u0clqH2Goj7llEl-zGufdXwC6ySPL8vvyxBdFSgeN6notUw4FLhVvyxTZYZMxVVLvQZo1_aZYYW1YUh7Tw720m_J80v41lPXoO4036Td-nlAtRDzG4OjWymIzjurxZS5cGFaXKbpNHay0JXp-fc4-ZhRbTAM5JPsQpqMmKUUmDUoFKe4kR1tIcc7XCq7065x9Ar9ChyK53MuTjSKe016s-ShkDOpLv4VyO1mTBdfhFFSl2Z_zUNMWUII6TbpXpnaZoR-1elz7h4KlwK6FLFX=EPV8m6ZK0zm9MXfUdT36fpPFAx5IDlB1uEUr7BDuTS6vZcycHrUmtsUnNSfW5wJtyaEywxuJZ4018FR5EW4W9Yp8kzen74UrkBS58kM4DueAIkFGvlFttgrDvwUKdPXuGtQlwHJCG4Fx=Enena9ocxRMd7--nXYKEB1lVvTAb-LnKG6mSmbPYamaCSF7Jk6bRRjsxJ-5-pLLxTqhVM9Anj5O1G9Stb9ZnAPjyp_A7_MQwR-M5qhll7A9JX95xH_2WbrO3EwLMKOGNHh6VB3RtFJGcw8tGkdjhUDgzm-PeHznvZ1APlb_eLDE9uN2jRUzHaX-A0mHWpEHbvOmWowsWsKawJfaelzWQQESMOZcfK6Z6AX4jDt673cHKcnm_P2R0nrnGJj1x_lg-sU_ZEoTmRzNG_GK_zRVgIN65SIvXVK2WdL2UnHhPXutfEbCryklVF9kQLmWL7oMUDLS=M_c8We3rgfaUXVj56fmITmaCwSTGDq_XyIqROugw9ovYVVdLOLQTckoZh=KI9d3qLlW8jmHoanqtnyT3boKqUfNQ1sD0a377HE9xjKR0IEkBHbx25fD55gzwZfrGjyJJlk0zYwPGZJq-50fDRGQPdTKLWpXb8Nrky2aLnSufQB1pMIuREde4FuY4tdNXNgB=mdzS7jqyIENbBUuJQ=0GZ9x18vAoY0O8CqaX-fykc=dApXM2DEn929wKP=A0_cukSTff10RaJJrmT71=v0TlyUmgsG8pUIoekzvqXF6MbHDn3hywOXqkx3q3HQ063VbZ3l8B4SnIxpZ0Phjr1aN3NgpUwN8tddJo3fu3-apulI-WcgE6YVZHH5NMGl-jyXskhHwtcLAYHsqza4VnAYpcJUqljSMfKxJ5b0q62e6xa=HwjpHe3HC0QxV47O-FILRyXsVxWvV9R7UKVo0_nIpKuBondjD6T6MOWtGVk8dHav_Ubo=hLTkI7TSayqShVLrTvpJDJYHI8VnHCsVt9VZGqbu9DuLsYfbAQRhzkWYzqlFQG1x2YC-hdbE_NegS3cBRr-OAqkt-JXS2hm6FT_rEJeGKGZw=5D4EjKeZIQdLnFczxQ3eQTwSPPx8my9sx8E7-5l44790=I4M_XowIezn5CR02UkEwG-wKvVf7VvTUtJN0AeT7=k6wQNmNsIJbsB7FjW3lckUzvsK1wqXaoJQfBBsMUNOSfpP0U_ZJSlq1EcVca64WbY4IO4FKEQxYX970WTqk3bfTaZSjlhczy57u3jdZhdSLdO2JyU8w2ahmn96Sz=J5O25gVPtju1xb8InPSQVuLbXpQbhCypcbLfZCV3jGp2-bgIgqsjJ50tV0CXTlMXNalqB7CxQoYVKeayUdqvbfZTTmH=PIsuSDJla4_OpdcWGGXFVfVIQkpSEg7cD0IBds2wBIKX5qQBEFfoXpLsuCtyRRV4p_zTcAICG7eDCupVL-2Hbu1yUHWrLSaKvI0lz341TL=v9j=2GfhU3yJbchtBomno0qtdH0gg_7a2M0szOmxI51BFqeCW6aEuK5oPZ1p6YQ_xnuRy5oVcEyEkf3rWWx3x4RrlnmLUEVMTfUM5KNzTlYcu_YatJX8CgTusx58-9XzpCW2C2RquuZSaqog0xyewp671FN7QYfbAqxQPERkeSs=wl8nPMC2BQAxpuNy4EZZHT8d2vdNUzgXvDKIF4P2vZl84PpCam706oBoBHRqddcq7_Bk7UQsj9U=ZohByQ_yM_vrzv3vokuL8U=Wc5MsAa-hH2dKHz8MbY_Vl=6AvvC4UdsSR7zmMYxuOsbqoy3aUvljxNdv2D541yIsn0nLJ2n3g71jO4TQQecvPSH321tPdptQetnXHQ2SXN9uGoSfRSRqkeTGRyC1JMkJbTSn-CBwCRrEBMqsQyFtLZAcFr5IdRlHEoVpGsw6lVA87McxuBQ4v-vfsq5KXhosUSE85wMjJVnQbxF8n89gd_jqTqXVZesyWcp1OmROE-CcL7qAqg1Tv0QtmlGnlraScAbmVn_McjdYM0ywGaIH5sSYZOhNUUDXq8-zm__AxUkNor5K-a6na1nnMmWIeDlPO5ldF_qFBb7XrwslmZqOz3vz6bIM265yRTSPesF-5L61zoZbTyhXYPHpMs1XhVXPc1-tPe7Oz8Z5C4jxVG32F4QXWnS_5MXQ3fy85waSlJkDKgdx8f7N5K",
            "x-jfuguzwb-b": "-1u0a1k",
            "x-jfuguzwb-c": "AOCk-m6IAQAAFYrvrCjicYVdphI6nlJ3xiiF8l5oMjFB_QTLITtibCNBPpkT",
            "x-jfuguzwb-d": "ABaChIjBDKGNgUGAQZIQhISi0eIAtJmBDgA7YmwjQT6ZE_____-zYDxSADTRI9oH3bull_PmqGB7R8Q",
            "x-jfuguzwb-f": "Az-M_G6IAQAAFUK-h9BMxTIx4rh9Td-iOduSShaYujc8uwi0rhnpE7CqXFtwAWBA7-muchRAwH8AAOfvAAAAAA==",
            "x-jfuguzwb-z": "q",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-fetch-dest": "empty",
            "authority": "tools.usps.com",
            "sec-ch-ua-platform": "macOS",
            "origin": "https://tools.usps.com",
            "referer": "https://tools.usps.com/rcas.htm"
        }

        extra_headers.update(self.headers)

        response = self.make_request(url, payload, headers=extra_headers)

        # check error from response
        if 'error' in response:
            print(f"Server Error: {response['error']}")
            sys.exit()

        print(f"Response is: {response}")

        if not bool(response['result']['success']):
            error_message = response['result']['resultCodeMessageList'][0]['message']
            print("Error: " + error_message)
            return

        # internal confirmation number (3CjhqsA7fhyC0LmvN6H8/Hj==)
        confirmation_number = response['scheduling']['confirmationNumber']

        print(f"Internal confirmation number: {confirmation_number}")
        if confirmation_number:
            self.get_appointment_confirmation_number_from_booking(
                confirmation_number)
        return confirmation_number

    # get public facing appointment number from internal number after booking appointment

    def get_appointment_confirmation_number_from_booking(self, internal_number):
        url = f"{self.root_url}/appointmentByConfirmation"

        payload = {
            "confirmationNumber": internal_number  # 885V6oaBATo7E0hF32nDvpq==
        }

        response = self.make_request(url, payload)
        print(f"Response is: {response}")

        # check error from response
        if 'error' in response:
            print(f"Server Error: {response['error']}")
            sys.exit()

        confirmation_number = response['scheduling']['confirmationNumber']
        print(
            f"Successfully scheduled appointment. Confirmation number: {confirmation_number}")
        return confirmation_number

    def get_internal_confirmation_number_from_public_number(self, public_number):
        url = f"{self.root_url}/appointmentByConfirmationPhoneEmail"
        email = config.get('DEFAULT', 'EMAIL')

        payload = {
            "confirmationNumber": public_number,
            "customerEmailAddress": email,
            "customerPhone": ""
        }

        response = self.make_request(url, payload)
        print(f"Response is: {response}")

        # check error from response
        if 'error' in response:
            print(f"Server Error: {response['error']}")
            sys.exit()

        confirmation_number = response['scheduling']['comments']
        print(
            f"Internal confirmation number: {confirmation_number}")
        return confirmation_number

    # ask user which appointment to cancel with public facing number (WEA249265474)
    def ask_user_which_appointment_to_cancel(self):
        public_number = input("Please provide appointment number to cancel:")
        internal_number = self.get_internal_confirmation_number_from_public_number(
            public_number)
        self.cancel_appointment(internal_number)

    # cancel appointment

    def cancel_appointment(self, confirmation_number):
        url = f"{self.root_url}/cancelAppointment"

        payload = {
            "confirmationNumber": confirmation_number,
            "cancelReason": "DONOTNEED"
        }

        response = self.make_request(url, payload)

        if response['scheduling']['status'] == 'CANCELLED':
            print("Successfully cancelled appointment.")

    # make API request

    def make_request(self, url, payload, headers=None, retry=3):
        """Make http request with retry"""
        if headers is None:
            headers = self.headers
        try:
            response = requests.post(
                url, headers=headers, data=json.dumps(payload), timeout=60)
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

    # normalize input string MM/DD/YYYY to YYYYMMDD format for API request

    def normalize_date(self, date_string):
        """Normalize the date"""
        # initialize date from string
        date_object = datetime.datetime.strptime(date_string, '%m/%d/%Y')
        normalized_date = f"{date_object.year}{date_object.month:02d}{date_object.day:02d}"
        return normalized_date

    # helper function to merge two dictionaries recursively

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
