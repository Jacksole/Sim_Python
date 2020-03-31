#!/usr/bin/env python3
# Blockbuster Movie Premire Simulation
# Created from the RealPython Tutorial on Simulations
# Programmer: Le Aundre 
# Date: 3/31/2020

import simpy
import random
import statistics

wait_times = []


class Theater(object):
    def __init__(self, env, num_cashiers, num_servers, num_ushers):
        self.env = env
        self.cashier = simpy.Resource(env, num_cashiers)
        self.server = simpy.Resource(env, num_servers)
        self.usher = simpy.Resource(env, num_ushers)

    def purchase_ticket(self, moviegoer):
        yield self.env.timeout(random.randint(1, 3))

    def check_ticket(self, moviegoer):
        yield self.env.timeout(3 / 60)

    def sell_food(self, moviegoer):
        yield self.env.timeout(random.randint(1, 5))

    def go_to_movies(env, moviegoer, theater):
        # Moviegoer arrives at the theater
        arrival_time = env.now

        with theater.cashier.request() as request:
            yield request
            yield env.process(theater.purchase_ticket(moviegoer))

        with theater.usher.request() as request:
            yield request
            yield env.process(theater.check_ticket(moviegoer))

        if random.choice([True, False]):
            with theater.server.request() as request:
                yield request
                yield env.process(theater.sell_food(moviegoer))

        # Moviegoer heads into the theater
        wait_times.append(env.now - arrival_time)

    def run_theater(env, num_cashiers, num_servers, num_ushers):
        theater = Theater(env, num_cashiers, num_servers, num_ushers)

        for moviegoer in range(3):
            env.process(go_to_movies(env, go_to_movies, theater))

        while True:
            yield env.timeout(0.20)  # Wait a bit before generating

            moviegoer += 1
            env.process(go_to_movies(env, moviegoer, theater))

    def get_average_wait_time(wait_times):
        average_wait = statistics.mean(wait_times)

    def calculate_wait_time(arrival_times, departure_times):
        average_wait = statistics.mean(wait_times)
        # Pretty print the results
        minutes, frac_minutes = divmod(average_wait, 1)
        seconds = frac_minutes * 60
        return round(minutes), round(seconds)

    def get_user_input():
        num_cashiers = input("Input # of cashiers working: ")
        num_servers = input("Input # of servers working: ")
        num_ushers = input("Input # of ushers working: ")
        params = [num_cashiers, num_servers, num_ushers]
        if all(str(i).isdigit() for i in params):  # Check input is valid
            params = [int(x) for x in params]
            else:
                print(
                    "Could not parse input. The simulation will use default values:",
                    "\n1 cashier, 1 server, 1 usher.",
                )
                params = [1, 1, 1]
                return params
