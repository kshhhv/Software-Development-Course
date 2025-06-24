import ctypes

# Load shared library
lib = ctypes.CDLL('./calculator.so')

# Declare the function signature
lib.run.argtypes = [ctypes.c_char_p]
lib.run.restype = ctypes.c_float

def run_calculator(expr: str) -> float:
    # Convert Python string to bytes (C char*)
    expr_bytes = expr.encode('utf-8')
    result = lib.run(expr_bytes)
    return result

if __name__ == "__main__":

    expression = "5 + 3 + 4 - 1"
    
    result = run_calculator(expression)
    
    print(f"Result: {result}")
