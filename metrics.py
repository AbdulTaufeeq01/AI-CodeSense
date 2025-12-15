import time

def estimate_tokens(text):
    # 1 token ≈ 4 characters (rough but standard)
    return len(text) // 4

def measure_execution(func, *args):
    start = time.time()
    result = func(*args)
    end = time.time()
    return result, end - start
