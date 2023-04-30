<p align="center">
  <img src="Resources/United-States-Postal-Service-Logo.png" width="448" height="252"/>
</p>

[![Twitter](https://img.shields.io/badge/twitter-%40JackieQi-blue.svg?style=flat-square)](https://twitter.com/JackieQi)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-JackieQi-blue.svg?style=flat-square)](https://www.linkedin.com/in/chiqi/)
# USPS Passport appointment finder



Little python script to help check available passport appointment for 30 days given specified location and start date.

<p align="center">
  <img src="Resources/demo.gif" alt="animated" />
</p>

- [Helpful links](#helpful-links)
- [Features](#features)
- [Requirements](#requirements)
- [Usage](#usage)
- [API reference](#api-reference)
- [Contributing](#contributing)
- [Backstory](#backstory)



## Helpful links
[Appointment entrance](https://tools.usps.com/rcas.htm)

[Processing time](https://travel.state.gov/content/travel/en/passports/how-apply/processing-times.html)

## Features
- [x] search by zip and date
- [x] search for next one month continuously

## Requirements

You need to install [pyhon3](ttps://www.python.org/downloads/) and its package manager [pip](https://pip.pypa.io/en/stable/installation/#get-pip-py), then install required packages

```pip3 install -r requirements.txt```


## Usage
```$ python3 FILE_NAME```

## API reference
Pleas refer to [API](https://github.com/JackieQi/USPSPassportAppointmentFinder/blob/main/API_Reference.md) document. 
Including appointment searching, booking, cancellation.

## Todo
- [ ] move hard coded info out of main class
- [ ] add exception handler
- [ ] book closest appointment ([API](https://github.com/JackieQi/USPSPassportAppointmentFinder/blob/main/API_Reference.md) available here)
- [ ] add CLI with parameters
- [ ] add web frontend

## Contributing

Before contributing, please read the instructions detailed here [contribution guide](https://github.com/JackieQi/USPSPassportAppointmentFinder/blob/main/CONTRIBUTING.md).

## Backstory

USPS website is so hard to use when searching for appointments. I have an international trip coming which requires visa after naturalization.
It's pretty urgent for me to get the passport. Now here is the script to help whoever has the need.
