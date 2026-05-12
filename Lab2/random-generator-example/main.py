from random_generator_lib import random_number_generator, timeout_iterator


gen = random_number_generator()
timeout_iterator(gen, 3)