import requests
import fileinput
import datetime
from bs4 import BeautifulSoup


class converter:
    def __init__(self, currency="USD"):
        self.currency = currency

    def get_exchange_rate(self, date):
        response = requests.get(
            f"https://www.lb.lt/lt/currency/buhalteriniaiexport/?xml=1&class=Lt&type=day&date_day={date}")

        if response.status_code != 200:
            raise "Non-OK response from LB"

        rates = BeautifulSoup(response.text, "xml")

        node = rates.find(self.get_exchange_rate_node_filter())
        return node.santykis.text

    def get_exchange_rate_node_filter(self):
        return lambda tag: tag.name == "item" and tag.valiutos_kodas.text == self.currency


def main():
    calc = converter()
    for line in fileinput.input():
        date_string = line.rstrip()
        datetime.datetime.strptime(date_string, '%Y-%m-%d')

        print(calc.get_exchange_rate(date_string))


if __name__ == "__main__":
    main()
