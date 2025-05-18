from typing import Dict
import reflex as rx

class State(rx.State):
    _token: Dict[str, str] = {}
