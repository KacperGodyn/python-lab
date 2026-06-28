class Product:
    """Reprezentuje produkt w sklepie internetowym."""

    def __init__(self, name: str, price: float, quantity: int):
        if price < 0:
            raise ValueError("Cena nie może być ujemna")
        if quantity < 0:
            raise ValueError("Ilość nie może być ujemna")

        self.name = name
        self.price = price
        self.quantity = quantity

    def add_stock(self, amount: int):
        if amount < 0:
            raise ValueError("Dodawana ilość nie może być ujemna")
        self.quantity += amount

    def remove_stock(self, amount: int):
        if amount < 0:
            raise ValueError("Usuwana ilość nie może być ujemna")
        if amount > self.quantity:
            raise ValueError("Brak wystarczającej ilości w magazynie")
        self.quantity -= amount

    def is_available(self) -> bool:
        return self.quantity > 0

    def total_value(self) -> float:
        return self.price * self.quantity

    def apply_discount(self, percent: float):
        """Obniza cene o podany procent (0-100)."""
        if percent < 0 or percent > 100:
            raise ValueError("Procent rabatu musi być w przedziale 0-100")
        self.price = self.price * (1 - (percent / 100))
