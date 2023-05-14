import uvicorn
import mpmath
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from app.middlewares import ResponseTimeMiddleware

app = FastAPI()
app.add_middleware(ResponseTimeMiddleware)

# Liste de chiffres avec une taille N,  1 < N < 100000000

factorial_cache = {}


def long_calculation(param: int) -> int:
    if param in factorial_cache:
        return factorial_cache[param]
    else:
        result = mpmath.factorial(param)
        factorial_cache[param] = result
        return result

@app.get('/long-calculation')
async def perform_long_calculation(param: int):
    if param < 0:
        return JSONResponse({'error': 'Parameter must be a positive integer'}, status_code=400)

    factorial_result = str(long_calculation(param)).rstrip('0').rstrip('.')
    
    return {'result': factorial_result}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=5000)

