import logging
import os
import shutil
import webbrowser

import matplotlib.pyplot as plt

from .Market import Market


class Simulation:
    def __init__(self):
        self.market = Market(self)
        self.output_folder = "plots"

    def create_plots(self):
        """plot_budget and save plots to folder"""
        logging.debug("Cleaning the output folder")
        output_folder = self.output_folder
        if os.path.exists(os.path.join(".", output_folder)):
            shutil.rmtree(os.path.join(".", output_folder))
        os.makedirs(os.path.join(".", output_folder))

        # plot_budget the bankrupt contractors
        logging.debug("Plotting the bankrupt contractors")
        plt.figure()
        plt.plot(self.market.data_number_contractors_bankrupt)
        plt.title("Contractors Going Bankrupt")
        plt.xlabel("Steps")
        plt.ylabel("# Contractors")
        plt.savefig(os.path.join(".", output_folder, "bankrupt_contractors.png"))

        # plot_budget each contractor
        # SURVIVING CONTRACTORS
        logging.debug("Plotting the budgets of surviving contractors")
        plt.figure()
        for contractor in self.market.contractors:
            contractor.plot_budget()
        plt.title("Surviving Contractor Budgets")
        plt.legend([str(contractor) for contractor in self.market.contractors])
        plt.savefig(
            os.path.join(".", output_folder, "surviving_contractor_budgets.png"))

        logging.debug("Plotting the markups of surviving contractors")
        plt.figure()
        for contractor in self.market.contractors:
            contractor.plot_markup()
        plt.title("Surviving Contractor Markups")
        plt.legend([str(contractor) for contractor in self.market.contractors])
        plt.savefig(
            os.path.join(".", output_folder, "surviving_contractor_markups.png"))

        # ALL CONTRACTORS
        logging.debug("Plotting the budgets of all contractors")
        plt.figure()
        for contractor in self.market.contractors + self.market.contractors_bankrupt:
            contractor.plot_budget()
        plt.title("All Contractor Budgets")
        plt.legend([str(contractor) for contractor in self.market.contractors])
        plt.savefig(
            os.path.join(".", output_folder, "all_contractor_budgets.png"))

        logging.debug("Plotting the markups of all contractors")
        plt.figure()
        for contractor in self.market.contractors + self.market.contractors_bankrupt:
            contractor.plot_markup()
        plt.title("All Contractor Markups")
        plt.legend([str(contractor) for contractor in self.market.contractors])
        plt.savefig(
            os.path.join(".", output_folder, "all_contractor_markups.png"))

        # open the folder
        webbrowser.open(os.path.join(".", output_folder))

        return self

    def start(self):
        logging.debug("Starting the simulation")
        self.market.loop()
        logging.debug("simulation ended")
        logging.debug("plotting")
        self.create_plots()
        return self
