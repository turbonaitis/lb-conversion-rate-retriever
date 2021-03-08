import requests
import fileinput
import datetime
import xml.etree.ElementTree as ET


class converter:
    def __init__(self, currency="USD"):
        self.currency = currency

    def get_exchange_rate(self, date):
        response = requests.get(
            f"https://www.lb.lt/lt/currency/buhalteriniaiexport/?xml=1&class=Lt&type=day&date_day={date}")

        if response.status_code != 200:
            raise "Non-OK response from LB"

        root = ET.fromstring(response.text)
        for child in root.findall("item"):
            currency_code = child.find("valiutos_kodas")
            if currency_code.text == self.currency:
                return child.find("santykis").text
        raise Exception(f"Couldn't find node for {date}")


def main():
    calc = converter()
    for line in fileinput.input():
        date_string = line.rstrip()
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        fx = calc.get_exchange_rate(date_string)
        print(f"{date_string}, {fx}")


if __name__ == "__main__":
    main()
