
import requests
import json


def analyzeQueryData(data):
    tripIndex = 0
    flightCandidates = []
    for tripIndex, trip in enumerate(data['data']['Trips']):
        for flightIndex, flight in enumerate(trip['Flights']):
            if flight['StopsandConnections'] >= 1:
                continue
            print(tripIndex, flightIndex)
            validFlight = {}
            validFlight['flightNumber'] = flight['OperatingCarrier'] + flight['FlightNumber']
            validFlight['Origin'] = flight['Origin']
            validFlight['Destination'] = flight['Destination']
            validFlight['DepartTime'] = flight['DepartDateFormat'] + "," + flight['DepartTimeFormat']
            validFlight['BookingClassAvailList'] = flight['BookingClassAvailList']
            isValid = False
            for product in flight['Products']:
                if product['BookingCount'] > 0:
                    validFlight[product['ProductTypeDescription']] = product['BookingCode'] + str(product['BookingCount'])
                    isValid = True
            if isValid:
                flightCandidates.append(validFlight)
    print(flightCandidates)


            # print(flight)
            # print("\n\n")


def start():
    data = {}
    with open('unitedResult.json') as json_file:
        data = json.load(json_file)
    analyzeQueryData(data)


if __name__ == '__main__':
    start()