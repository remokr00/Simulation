"""In this file there is the code that i used to simulate an Inventory System"""


import sys
import random
import numpy

#defining the timing function to find the next event
def timing():

    '''This function is used to find the next event in the event list
    and update the simulation time to the time of the next event
    and the next event type to the type of the next event
    '''

    #i specifies the variables that i need
    global time_next_event
    global simulation_time
    global next_event_type

    min_time_next_event = 1e9
    next_event_type = ''

    #selection of the next event time which is the one in first position of my list
    next_event_tuple = time_next_event[0]
    #now i have a tuple of type ('event', time_of_event)
    next_event_type = next_event_tuple[0]
    min_time_next_event = next_event_tuple[1]

    if next_event_type == '': #if next event is null we have finished
        print('Event list is emplty at time', simulation_time)
        sys.exit()

    simulation_time = min_time_next_event

#defining the main 3 events


#1. demand event
def demand():

    '''This function is used to simulate the demand of the customers
    and update the inventory level
    '''

    global inventory_level

    #i generate the size of the deman
    random_number = random.randint(0,1)

    demand_size = 0
    if random_number < 1/6:
        demand_size = 1
    elif random_number < 1/2:
        demand_size = 2
    elif random_number < 5/6:
        demand_size = 3
    else:
        demand_size = 4

    inventory_level -= demand_size

    print(f'New inventory level after demand: {inventory_level}')

    #i shcedule the next demand event
    time_next_event.pop(0) #i delete the event from consideration
    time_next_event.append(('demand', simulation_time + numpy.random.exponential(scale = 0.1)))
    time_next_event.sort(key = lambda x: x[1])


#2. evaluate event
def evaluate():

    '''This function is used to evaluate the inventory level
    and decide if an order is placed or not
    '''

    global inventory_level
    global s
    global time_next_event
    global simulation_time
    global ordering_cost
    global S
    global K
    global last_order
    global i

    if   inventory_level < s:
        order_size = S - inventory_level
        last_order = order_size
        #updating ordering cost
        ordering_cost += K + i * order_size
        time_next_event.append(('arrival', simulation_time + numpy.random.uniform(0.5, 1)))
    else:
        print('No order is placed')


    time_next_event.pop(0) #i delete the event from consideration
    time_next_event.append(('evaluate', simulation_time + 1))
    time_next_event.sort(key = lambda x: x[1])


#3. order of arrival event
def arrival_of_order():

    '''This function is used to update the inventory level after the arrival of an order
    and delete the event from consideration
    '''

    global inventory_level
    global last_order
    global time_next_event

    #i increment the inventory level
    inventory_level += last_order

    print(f'New inventory level after arrival of order: {inventory_level}')

    #i delete the event from consideration
    time_next_event.pop(0)


def updating_areas():

    global area_under_inventory_level
    global area_inventory_level
    global time_of_last_event
    global simulation_time

    current_period = simulation_time - time_of_last_event
    time_of_last_event = simulation_time

    if inventory_level < 0:
        area_under_inventory_level -= inventory_level * current_period
    elif inventory_level > 0:
        area_inventory_level += inventory_level * current_period



def update_statistical_counters():

    global ordering_cost
    global month_of_evaluation
    global holding_cost
    global area_inventory_level
    global storage_cost
    global area_under_inventory_level
    global total_cost

    avg_ordering_cost = ordering_cost / month_of_evaluation
    avg_holding_cost = holding_cost * area_inventory_level / month_of_evaluation
    avg_shortage_cost = abs(storage_cost * area_under_inventory_level / month_of_evaluation) #abs because it is a cost
    total_cost = avg_ordering_cost + avg_holding_cost + avg_shortage_cost
    return total_cost, avg_ordering_cost, avg_holding_cost, avg_shortage_cost

"""---------------------------- Inizializing the system -----------------------------------"""
 #list of possible policies
    #1. (s, S) = (20, 40)
    #2. (s, S) = (20, 60)
    #3. (s, S) = (20, 80)
    #4. (s, S) = (40, 60)
    #5. (s, S) = (40, 80)
    #6. (s, S) = (40, 100)
    #7. (s, S) = (60, 80)
    #8. (s, S) = (60, 100)

policies = [(20, 40), (20, 60), (20, 80),(20,100), (40, 60), (40, 80), (40, 100), (60, 80), (60, 100)]
results = []

for policy in policies:
    #state variables

    s = policy[0]
    S = policy[1]

    simulation_time = 0
    inventory_level = 60
    orderd_not_arrived = 0 #order not arrived from the supplier
    time_of_last_event = 0

    month_of_evaluation  = 120
    last_order = 0 #to save the amount of last order
    shelf_life_queue = [] #to save the shelf life of the products


    #costs
    holding_cost = 1
    storage_cost = 5
    K = 32
    i = 3
    express_order_fixed_cost = 48
    express_order_variable_cost = 4

    #event list
    time_next_event = []
    #first event is gonna be an evaluation event at time 0
    time_next_event.append(('evaluate', 0)) #first evalyation event
    time_next_event.append(('demand', numpy.random.exponential(scale = 0.1)))
    time_next_event.append(('end', 120)) #end of simulation
    next_event_type = 'evaluate'

    #statistics

    ordering_cost = 0
    area_under_inventory_level = 0
    area_inventory_level = 0
    total_cost = 0

    #main loop for simulation

    update = False

    while simulation_time <= month_of_evaluation:

        timing()
        updating_areas()
        if next_event_type == 'demand':
            demand()
        elif next_event_type == 'evaluate':
            evaluate()
        elif next_event_type == 'arrival':
            arrival_of_order()

        if next_event_type == 'end' and not update:
            results.append(update_statistical_counters())
            update = True
            break

#now we print the table with the result for every policy
print('Policy\t\tTotal cost\tOrdering cost\tHolding cost\tShortage cost')
for i, policy in enumerate(policies):
    print(f'{policy}\t  {results[i][0]:.3f}\t  {results[i][1]:.3f}\t\t{results[i][2]:.3f}\t\t{results[i][3]:.3f}')





