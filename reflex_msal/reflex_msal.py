"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from .auth import Auth


def index() -> rx.Component:
    """Welcome Page (Index)"""
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.link(
                rx.button("Protected page"),
                href="/authenticated",
                is_external=False,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
    )


def authenticated() -> rx.Component:
    """Authenticated Page"""

    return rx.cond(
        ~Auth.check_auth,
        rx.spinner(size="3", margin="auto"),
        rx.container(
            rx.color_mode.button(position="top-right"),
            rx.vstack(
                rx.heading(f"Hello {Auth.token['name']} to this protected page", size="9"),
                spacing="5",
                justify="center",
                min_height="85vh",
            ),
            rx.logo(),
        ),
    )


def callback() -> rx.Component:
    """Callback Page"""
    return rx.container()


app = rx.App()
app.add_page(index)
app.add_page(callback, route="/callback", on_load=Auth.callback)
app.add_page(authenticated, route="/authenticated", on_load=Auth.require_auth)
