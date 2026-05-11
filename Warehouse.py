class Product:
    """
    Хранит информацию о продукте
    """
    def __init__(self, name: str, price: int, quantity: int):
        self.__name=name 
        if price <= 0:
            raise ValueError("Цена не может быть 0 или ниже")
        self.__price=price
        if quantity < 0:
            raise ValueError("Количество товара не может быть меньше 0")
        self.__quantity=quantity        
    
    
    def __str__(self):
        return f"Товар: {self.__name}, цена: {self.__price}руб., количество: {self.__quantity}шт."
    
    
    @property #геттер имени
    def name(self):
        return self.__name
    
        
    @property #геттер цены
    def price(self):
        return self.__price
    
    
    @property #геттер количества
    def quantity(self):
        return self.__quantity
        
    
    @quantity.setter # сеттер количества
    def quantity(self, value):
        if value<0:
            raise ValueError('количество товара не может быть меньше нуля')
        self.__quantity=value
    
    @property #геттер общей стоимости товаров
    def total_value(self):
        return self.__price*self.__quantity


class PerishableProduct(Product):
    """
    содержит информацию о скоропортящихся продуктах
    """
    def __init__(self,name,price,quantity,expiry_days):
        super().__init__(name,price,quantity)
        if expiry_days < 0:
            raise ValueError('Я не буду учитывать испорченные продукты')
        self.__expiry_days = expiry_days
        
    
    def __str__(self):
        return f"{super().__str__()}, годность: {self.__expiry_days} дней"
        
        
class WareHouse():
    """
    Управляет списком продуктов
    """
    def __init__(self):
        self.product = []
    
    
    def add_product(self, product): # обавляем проукт в список склаа, если проукт с таким именем уже ест - дообаляем колчеств, цену не меяем
        for existing in self.product:
            if existing.name == product.name:
                existing.quantity += product.quantity
                return
        self.product.append(product)
        
        
    def remove_product(self, name: str, quantity: int):
        for existing in self.product:
            if existing.name == name:
                if existing.quantity < quantity:
                    raise ValueError("Недостаточно товара на складе")
                existing.quantity -= quantity
                return
        raise ValueError("Товар не найден")              
        
        
    def total_warehouse_value(self):
        return sum(p.total_value for p in self.product)
    
    
    def find_products(self, min_price = None, max_price = None):
        result = []
        for existing in self.product:
            price = existing.price
            if (min_price is None or price >= min_price)and(max_price is None or price <= max_price):
                result.append(existing.name)
        return result
        

# Создаём товары
apple = Product("Яблоко", 50, 100)
milk = PerishableProduct("Молоко", 80, 20, 5)
tv = Product("Телевизор", 25000, 3)

# Склад
wh = WareHouse()
wh.add_product(apple)
wh.add_product(milk)
wh.add_product(tv)

print(wh.total_warehouse_value())  
# 100*50 + 20*80 + 3*25000 = 5000+1600+75000 = 81600

# Добавляем ещё яблоки (должно увеличить количество существующих)
more_apples = Product("Яблоко", 55, 50)   # цена не важна, количество увеличится
wh.add_product(more_apples)
# Теперь яблок должно стать 150 (цена осталась 50)

# Удаляем часть молока
wh.remove_product("Молоко", 10)   # останется 10

print(wh.find_products(min_price=60, max_price=500))  # например, "Молоко" (80)

# Проверка ошибок
try:
    wh.remove_product("Хлеб", 1)
except ValueError as e:
    print(e)   # "Товар не найден"

try:
    tv.quantity = -5
except ValueError as e:
    print(e)   # "Количество не может быть отрицательным"