import angr
import claripy
import sys


path_to_binary = './rage'
project = angr.Project(path_to_binary)

# Address were you want to indicate the relation BitVector - registries
start_address = 0x08049661
initial_state = project.factory.blank_state(
    addr=start_address,
)
print("esp:",initial_state.regs.esp)

# Create Bit Vectors
bit = 8*8
password0 = claripy.BVS('password0', bit)
password1 = claripy.BVS('password1', bit)
password2 = claripy.BVS('password2', bit)
password3 = claripy.BVS('password3', bit)

# Relate it Vectors with the registriy values you are interested in to reach an address

fake_heap_address0 = 0x7fff0000-0x100
pointer_to_malloc_memory_address0 = 0x90fb2d4
initial_state.memory.store(pointer_to_malloc_memory_address0,fake_heap_address0, endness=project.arch.memory_endness)

fake_heap_address1 = 0x7fff0000 - 0x120
pointer_to_malloc_memory_address1 = 0x90fb2d8
initial_state.memory.store(pointer_to_malloc_memory_address1,fake_heap_address1, endness=project.arch.memory_endness)

fake_heap_address2 = 0x7fff0000 - 0x130
pointer_to_malloc_memory_address2 = 0x90fb2dc
initial_state.memory.store(pointer_to_malloc_memory_address2,fake_heap_address2, endness=project.arch.memory_endness)

fake_heap_address3 = 0x7fff0000 - 0x140
pointer_to_malloc_memory_address3 = 0x90fb2e0
initial_state.memory.store(pointer_to_malloc_memory_address3,fake_heap_address3, endness=project.arch.memory_endness)

initial_state.memory.store(fake_heap_address0, password0)
initial_state.memory.store(fake_heap_address1, password1)
initial_state.memory.store(fake_heap_address2, password2)
initial_state.memory.store(fake_heap_address3, password3)

simulation = project.factory.simgr(initial_state)

def is_successful(state):
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return 'Yes'.encode() in stdout_output

def should_abort(state):
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return 'wrong'.encode() in stdout_output

avoid = [0x080492FC, 0x08049847]
simulation.explore(find=0x08049859, avoid=avoid)
print(simulation.found)
if simulation.found:
    solution_state = simulation.found[0]

    solution0 = solution_state.solver.eval(password0)
    solution1 = solution_state.solver.eval(password1)
    solution2 = solution_state.solver.eval(password2)
    solution3 = solution_state.solver.eval(password3)

    # Aggregate and format the solutions you computed above, and then print
    # the full string. Pay attention to the order of the integers, and the
    # expected base (decimal, octal, hexadecimal, etc).
    solution = ' '.join(map('{:x}'.format, [ solution0, solution1, solution2, solution3 ]))  # :string
    print(solution)
else:
    raise Exception('Could not find the solution')

