
__registered_machines = []

def on_machine_HB(message, machine_address):
    print 'platform_status on_machine_HB'
    if machine_address not in __registered_machines:
        print 'platform_status unknown machine: ' + str(machine_address)
        __registered_machines.append(machine_address)
    