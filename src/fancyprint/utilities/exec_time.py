#######################
# IMPORTING LIBRARIES #
#######################
from functools import wraps
from time import time


##############
# DECORATORS #
##############
def exec_time(func):
    @wraps
    def wrapper(*args, **kwargs):
        print(f"Executing {func.__name__}...")
        
        # Get Starting Time
        start_time = time()
        
        # Execute the function
        func(*args, **kwargs)
        
        # Get end time
        end_time = time()
        
        # Caculate execution time
        execution_time = end_time - start_time
        
        # Print
        print("Execution finished!")
        print(f"Execution took {execution_time:.4f} seconds")
        
        # Return the function
        return func
        
    # return the wrapper functino
    return wrapper