from typing import List, Callable, Any

def critique_function(k: int, **kwargs: Any) -> None:
    print(k)
    print(kwargs.get('test'))

def runner(func: Callable[..., None]) -> None:
    func(2, a=10, test=5)

runner(critique_function)

# ------------------------------------------------------ #

class A:
    ...


class B(A):
    ...


lst1 = [A(), A()]
lst2 = [B(), B()]


def get_first_elem(x: List[Any]) -> Any:
    return x[0]



'''

Na função runner, atualizei a anotação de tipo do parâmetro func para Callable[..., None]. 
O uso do ... indica que a função func pode receber qualquer número de argumentos de qualquer tipo.
Entretanto, caso não fosse o caso, poderíamos usar Callable[[int, Any], None]
'''


