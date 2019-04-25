import logging
from .Project import Project
from .Contractor import Contractor


class Market:
    def __init__(self, simulation):
        """Create the market"""
        logging.debug("Creating the market.")
        self.projects = []
        self.contractors = []
        self.contractors_bankrupt = []
        self.max_number_of_contractors = 20
        self.max_number_of_projects = 15
        self.step_number = -1
        self.max_steps = 1000
        self.data_number_contractors_bankrupt = []
        # the market belongs to a simulation
        self.simulation = simulation
        # Minimum attractive rate of return
        self.MARR = 0.01
        # overhead settings
        self.overhead_percentage = 0.01
        self.overhead_minimum = 10000

    def step(self):
        """Make a new step"""
        self.step_number += 1
        logging.info("Step: {}".format(self.step_number))
        # kill the old projects
        self.projects = []

        # Create new projects
        number_of_projects_created = 0
        while len(self.projects) < self.max_number_of_projects:
            self.projects.append(Project(self))
            number_of_projects_created += 1
        logging.debug("Created {} new projects.".format(number_of_projects_created))

        # Make sure that we have the required number of contractors
        number_of_contractors_created = 0
        while len(self.contractors) < self.max_number_of_contractors:
            self.contractors.append(Contractor(self))
            number_of_contractors_created += 1
        logging.debug("Created {} new contractors.".format(number_of_contractors_created))

        # Let the contractors start bidding
        logging.debug("Starting the bid process.")
        for contractor in self.contractors:
            contractor.start_bidding()

        # get the winning contractors and give them their profits
        logging.debug("Finding the winning contractors and telling them.")
        for project in self.projects:
            for contractor in project.contractors:
                if contractor == project.get_winning_contractor():
                    contractor.win(project)
                else:
                    contractor.loose(project)

        # make all the contractors pay their over head
        logging.debug("Contractors are paying their overheads.")
        for contractor in self.contractors:
            contractor.pay_overhead()

        # delete the bankrupt contractors
        number_of_contractors_going_bankrupt = 0
        for contractor in self.contractors:
            if contractor.budget < 0:
                logging.debug("{} is going bankrupt".format(contractor))
                self.contractors.remove(contractor)
                self.contractors_bankrupt.append(contractor)
                number_of_contractors_going_bankrupt += 1
        self.data_number_contractors_bankrupt.append(number_of_contractors_going_bankrupt)

        # output the budgets of the contractors
        for contractor in self.contractors:
            logging.debug("{} now has {}".format(
                contractor,
                contractor.budget
            ))

    def loop(self):
        """Start the loop"""
        logging.debug("Starting the loop")
        while self.step_number < self.max_steps:
            self.step()
