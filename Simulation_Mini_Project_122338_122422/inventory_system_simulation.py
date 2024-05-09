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
    global total_items_removed
    global expired_items

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

    update_shelf_life() #before satysfyng the request we see if there are spoiled product

    inventory_level -= demand_size
    total_items_removed += demand_size + expired_items

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
    global express_order_placed


    #implementing the first changes for the project
    if inventory_level < 0:
        express_order_placed += 1
        order_size = S - inventory_level  # dimension of the order
        last_order += order_size
        ordering_cost += express_order_fixed_cost + express_order_variable_cost * order_size
        # Programmare l'arrivo dell'ordine espresso
        time_next_event.append(('arrival', simulation_time + numpy.random.uniform(0.25, 0.5)))

    if  0 <= inventory_level < s:
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

    #we initialize the new life of the articles in the inventory
    initialize_shelf_life(last_order)

    print(f'New inventory level after arrival of order: {inventory_level}')

    #i delete the event from consideration
    time_next_event.pop(0)


def updating_areas():

    global area_under_inventory_level
    global area_inventory_level
    global time_of_last_event
    global simulation_time
    global total_backlog_time #for the point 1.2

    current_period = simulation_time - time_of_last_event
    time_of_last_event = simulation_time

    if inventory_level < 0:
        area_under_inventory_level -= inventory_level * current_period
        total_backlog_time += current_period
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
    global month_of_evaluation
    global total_backlog_time
    global express_order_placed
    global expired_items
    global total_items_removed

    avg_ordering_cost = ordering_cost / month_of_evaluation
    avg_holding_cost = holding_cost * area_inventory_level / month_of_evaluation
    avg_shortage_cost = abs(storage_cost * area_under_inventory_level / month_of_evaluation) #abs because it is a cost
    total_cost = avg_ordering_cost + avg_holding_cost + avg_shortage_cost
    total_cost_per_month = total_cost / month_of_evaluation
    percentage_of_backlog = total_backlog_time / month_of_evaluation
    percentage_of_spoiled_items = expired_items/total_items_removed
    print((expired_items, total_items_removed))
    return total_cost, avg_ordering_cost, avg_holding_cost, avg_shortage_cost, total_cost_per_month, percentage_of_backlog, express_order_placed, percentage_of_spoiled_items

#function for the second point of the problem
def initialize_shelf_life(order_size):
    global shelf_life_queue
    for _ in range(order_size):
        # assigning a different shelf life for the article
        shelf_life = numpy.random.uniform(1.5, 2.5)
        shelf_life_queue.append((simulation_time, simulation_time + shelf_life))

def update_shelf_life():
    global shelf_life_queue
    global simulation_time
    global inventory_level
    global expired_items
    # Cheking and removal of expired article  
    while shelf_life_queue:
        # computing the time when the article was inserted in the queue
        time_in_inventory = simulation_time - shelf_life_queue[0][0]
        # if the article is expired then i remove it
        if time_in_inventory >= shelf_life_queue[0][1]:
            shelf_life_queue.pop(0)
            inventory_level -= 1  # Diminuisci il livello dell'inventario per ogni articolo scaduto
            expired_items += 1
            print(f"Articolo scaduto rimosso, nuovo livello di inventario: {inventory_level}")
        else:
            # Se l'articolo in testa alla coda non è scaduto, interrompi il ciclo
            break

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

policies = [(20, 40), (20, 60), (20, 80), (20,100), (40, 60), (40, 80), (40, 100), (60, 80), (60, 100)]
results = []

for policy in  policies:
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
    total_backlog_time = 0
    express_order_placed = 0
    expired_items = 0
    total_items_removed = 0

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
print('Policy\t\tTotal cost\tOrdering cost\tHolding cost\tShortage cost\t\t Cost per Month \t \t %I(t) < 0 \t \t Express Orders \t \t %Spoiled Items')
for i, policy in enumerate(policies):
    print(f'{policy}\t  {results[i][0]:.3f}\t  {results[i][1]:.3f}\t\t{results[i][2]:.3f}\t\t{results[i][3]:.3f}\t\t{results[i][4]:.3f}\t\t\t{results[i][5]*100:.3f} \t\t\t{results[i][6]} \t\t\t{results[i][7]*100:.3f}')





