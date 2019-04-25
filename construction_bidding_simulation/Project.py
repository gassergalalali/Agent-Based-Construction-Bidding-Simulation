import random
import logging


class Project:
    # records the last id used
    last_id = 0

    def __init__(self, market):
        Project.last_id += 1
        self.id = Project.last_id
        logging.debug("Creating {}".format(self))
        # Create a random project cost
        self.cost = int(round(random.uniform(100000, 500000), 0))
        # list to hold the contractors bidding
        self.contractors = []
        # list to hold the bid prices
        self.bid_prices = []
        # save the market
        self.market = market

    def add_bid(self, contractor, bid_price):
        """Contractor is bidding for this project"""
        self.contractors.append(contractor)
        self.bid_prices.append(int(bid_price))

    def get_winning_contractor(self):
        """return the Contractor who won the project"""
        if self.contractors == []:
            logging.warning("No One is bidding {}!".format(self))
            return None
        return self.contractors[self.bid_prices.index(min(self.bid_prices))]

    def get_lowest_bid_price(self):
        """return the value of the winning bid"""
        return min(self.bid_prices)

    def __str__(self):
        return "Project {}".format(self.id)
