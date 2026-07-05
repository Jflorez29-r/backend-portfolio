import time
from functools import wraps
from typing import Any, Callable


def measure_time(
    fn: Callable[..., Any] | None = None, *, label: str = "TELEMETRY", unit: str = "ms"
) -> Callable[..., Any]:
    def decorator(inner_fn: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(inner_fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            result = inner_fn(*args, **kwargs)
            elapsed = time.perf_counter() - start

            normalized_unit = unit if unit in {"ms", "s"} else "ms"
            if normalized_unit == "ms":
                elapsed *= 1000
                suffix = "ms"
            else:
                suffix = "s"

            print(f"\n[{label}] {inner_fn.__name__} took {elapsed:.3f} {suffix}")
            return result

        return wrapper

    if fn is not None and callable(fn):
        return decorator(fn)

    return decorator
