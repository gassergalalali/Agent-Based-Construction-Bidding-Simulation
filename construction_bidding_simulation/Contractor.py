import random
import logging
import math

import matplotlib.pyplot as plt


class Contractor:
    # records the last id used
    last_id = 0

    def __init__(self, market):
        Contractor.last_id += 1
        self.id = Contractor.last_id
        logging.debug("Creating {}".format(self))
        # Each contractor starts with a random budget
        self.budget_initial = random.uniform(100000, 1000000)
        self.budget = self.budget_initial
        # Each contractor has a random error range when bidding
        self.error_mu = 0
        self.error_sigma = 0.01
        # each contractor has an initial markup
        self.markup_factor = round(random.uniform(0.05, 0.10), 4)
        # Step size when correcting the markup for learning
        self.markup_correction_step = 0.001
        self.minimum_markup = 0
        # save the market
        self.market = market
        # create a history for the budget
        self.data_budget = []
        # create a history of the step number
        self.data_budget_step_number = []
        # create a history for the budget
        self.data_markup = []
        # create a history of the step number
        self.data_markup_step_number = []

    def log_budget(self):
        self.data_budget.append(self.budget)
        self.data_budget_step_number.append(self.market.step_number)

    def log_markup(self):
        self.data_markup.append(self.markup_factor)
        self.data_markup_step_number.append(self.market.step_number)

    def calculate_bid_price(self, actual_project_cost):
        """Calculate the price of the bid according to the project cost"""
        return int(round(
            actual_project_cost * (1
                                   + self.markup_factor
                                   + random.normalvariate(
                                             self.error_mu,
                                             self.error_sigma)),
            0))

    def start_bidding(self):
        """Start bidding for projects"""
        remaining_allocated_budget = self.budget
        for project in self.market.projects:
            bid_price = int(self.calculate_bid_price(project.cost))
            if (bid_price / 5) < remaining_allocated_budget:
                project.add_bid(self, bid_price)
                remaining_allocated_budget -= (bid_price / 3)
                logging.debug("{} is bidding {} for {}".format(
                    self,
                    bid_price,
                    project
                ))

    def win(self, project):
        """The contractor won the project!"""
        # Make the profit
        self.budget += round(
            (project.get_lowest_bid_price()
             - project.cost),
            0)
        logging.debug("{} won {} with cost {} and bid price {} winning {}.".format(
            self,
            project,
            project.cost,
            project.get_lowest_bid_price(),
            round(
                (project.get_lowest_bid_price()
                 - project.cost),
                0)
        ))
        self.log_budget()

        # adjust markup
        if self.is_profitable():
            # winning project and profitable, do nothing
            self.log_markup()
        else:
            # winning projects, but not profittable, increase markup
            self.increase_markup()

    def loose(self, project):
        # adjust learning
        if self.is_profitable():
            # Loosing project, but is still profitable, do nothing
            self.log_markup()
        else:
            # loosing project and not profitable, decrease markup
            self.decrease_markup()

    def is_profitable(self):
        # Check if profits are good so far, according to the MARR,
        # to adjust the markup
        if self.budget > (
                self.budget_initial * (1 + math.pow(
                self.market.MARR,
                self.market.step_number))):
            return True
        else:
            return False

    def increase_markup(self):
        self.markup_factor += self.markup_correction_step
        logging.debug("Increasing the markup factor of {} to {}".format(
            self,
            self.markup_factor))
        self.log_markup()

    def decrease_markup(self):
        if (self.markup_factor - self.markup_correction_step) > self.minimum_markup:
            self.markup_factor -= self.markup_correction_step
            logging.debug("Decreasing the markup factor of {} to {} because he keeps winning money".format(
                self,
                self.markup_factor))
        else:
            logging.debug("Markup factor of {} at minimum {}".format(
                self,
                self.markup_factor))
        self.log_markup()

    def pay_overhead(self):
        self.budget -= max(
            self.budget * self.market.overhead_percentage,
            self.market.overhead_minimum)
        self.budget = int(self.budget)
        self.log_budget()

    def plot_budget(self):
        if self.data_budget is not []:
            logging.debug("Plotting budget of {}".format(self))
            plt.plot(self.data_budget_step_number, self.data_budget)
            plt.title("{} Budget".format(self))
            plt.xlabel("Step Number")
            plt.ylabel("Budget ($)")

    def plot_markup(self):
        if self.data_markup is not []:
            logging.debug("Plotting markup of {}".format(self))
            plt.plot(self.data_markup_step_number, self.data_markup)
            plt.title("{} Markup".format(self))
            plt.xlabel("Step Number")
            plt.ylabel("Markup Factor")

    def __str__(self):
        return "Contractor {}".format(self.id)
