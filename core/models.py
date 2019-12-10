from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Address(models.Model):
    street = models.CharField(max_length=200)
    suite = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)

    def __str__(self):
        return "street: {}, suite: {}, city: {}, zipcode: {}".format(
        self.street ,self.suite, self.city, self.zipcode)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='clients')

    def __str__(self):
        return "Client: {}".format(self.name)
    

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    email = models.EmailField()
    cpf = models.CharField(max_length=11)
    salary = models.FloatField()

    def __str__(self):
        return "Manager: {}".format(self.name)


class Status(models.Model):

    STATUS = (
       ('Processando Compra', 'Processando Compra'),
       ('Aguardando Finalização', 'Aguardando Finalização'),
       ('Compra Finalizada', 'Compra Finalizada'),
       ('Aprovado', 'Aprovado'),
       ('Compra enviada', 'Compra enviada'),
    )

    message = models.CharField(max_length=30, default='Processando Compra', choices=STATUS)
    
    def __str__(self):
        return "Status: {}".format(self.message)


class CreditCard(models.Model):
    flag = models.CharField(max_length=60)
    number = models.CharField(max_length=60)
    number_security = models.CharField(max_length=3)

    def __str__(self):
        return "Flag: {}, Number: {}, Number security: {}".format(
        self.flag, self.number, self.number_security)


class Order(models.Model):

    CALC = (
       (0.0, 0.0),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="orders")
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True, related_name="managers")
    credit_card = models.ForeignKey(CreditCard, on_delete=models.CASCADE, related_name="credits_cards")
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name="status")
    total = models.FloatField(default=0.0, choices=CALC)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Client: {}, Manager: {}, Total: $ {}, Status: {}, Creditcard: {}".format(
        self.client.name, self.manager.name, self.total, self.status.message, self.credit_card)
    
    @property
    def get_status(self):
        return self.status.message


class Author(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField()

    def __str__(self):
        return "Author: {}".format(self.name)


class Genre(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return "Genre: {}".format(self.description)


class Book(models.Model):
    title = models.CharField(max_length=60)
    prince = models.FloatField()
    stock = models.IntegerField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return "Book: {}, Prince: $ {}, Genre: {}, Stock: {}".format(
        self.title, self.prince, self.genre.description, self.stock)


class Write(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="writes")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return "Author: {}, Book: {}".format(self.author, self.book)


class ItemOrder(models.Model):

    CALC = (
       (0.0, 0.0),
    )
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="items_orders")
    amount = models.IntegerField()
    subtotal = models.FloatField(default=0.0, choices=CALC)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Book: {}, Amount: {}, Subtotal".format(self.book, self.amount, self.subtotal)

    @property
    def calc_amount(self):
        instance = self
        self.subtotal = (self.amount * self.book.prince)
        instance.save() 

    @property
    def sub_stock(self):
        self.book.stock -= self.amount 
        self.book.save()

    @property
    def add_stock(self):
        self.book.stock += self.amount
        self.book.save()
    
    @property
    def add_total_order(self):
        self.order.total += self.subtotal
        self.order.save()

    @property
    def sub_total_order(self):
        self.order.total -= self.subtotal
        self.order.save()

    @property
    def get_status(self):
        return self.order.status.message