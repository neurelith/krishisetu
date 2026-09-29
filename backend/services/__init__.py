"""Service package.

Services are imported lazily by routers so the API can expose non-ML utilities
without loading the LightGBM stack during module import.
"""

