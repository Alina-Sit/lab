class Observable:
    def __init__(self):
        self._listeners: dict[str, list[callable]] = {}
        self._error_listeners: list[callable] = []

    def subscribe(self, event: str, listener: callable) -> callable:
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(listener)

        def unsubscribe():
            if event in self._listeners and listener in self._listeners[event]:
                self._listeners[event].remove(listener)

        return unsubscribe

    def on_error(self, listener: callable) -> callable:
        self._error_listeners.append(listener)

        def unsubscribe():
            if listener in self._error_listeners:
                self._error_listeners.remove(listener)

        return unsubscribe

    def emit(self, event: str, data=None) -> None:
        for listener in list(self._listeners.get(event, [])):
            try:
                listener(data)
            except Exception as err:
                self._handle_error(err)

    def _handle_error(self, err: Exception) -> None:
        if not self._error_listeners:
            print(f"Unhandled observable error: {err}")
            return
        for listener in list(self._error_listeners):
            try:
                listener(err)
            except Exception as inner:
                print(f"Error in error handler: {inner}")
class UserService(Observable):
    def login(self, username: str) -> None:
        self.emit("login", {"username": username})

    def logout(self, username: str) -> None:
        self.emit("logout", {"username": username})

    def purchase(self, username: str, amount: float) -> None:
        self.emit("purchase", {"username": username, "amount": amount})


class NotificationService:
    def on_login(self, data: dict) -> None:
        print(f"[Notification] Welcome, {data['username']}!")

    def on_purchase(self, data: dict) -> None:
        print(f"[Notification] Purchase confirmed: ${data['amount']:.2f}")


class AnalyticsService:
    def on_login(self, data: dict) -> None:
        print(f"[Analytics] User logged in: {data['username']}")

    def on_logout(self, data: dict) -> None:
        print(f"[Analytics] User logged out: {data['username']}")

    def on_purchase(self, data: dict) -> None:
        print(f"[Analytics] Purchase tracked: {data['username']} spent ${data['amount']:.2f}")