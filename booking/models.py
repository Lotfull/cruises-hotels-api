from django.db import models


class Hotel(models.Model):
    link = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.id}: link: {self.link}'

    @staticmethod
    def rooms_lt(rooms_limit=20):
        return (Hotel.objects
                .annotate(room_count=models.Count("hotelroom"))
                .filter(room_count__lt=rooms_limit))


class Room(models.Model):
    num = models.IntegerField()
    tv = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id}: num: {self.num}'


class Hotelroom(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.id}: room: {self.room} | hotel: {self.hotel} | price: {self.price}'


def fake_db(hotels=20):
    import random
    for i in range(hotels):
        hotel = Hotel.objects.create(link=f'http://hotel-{i}.com')
        for j in range(random.randint(0, 50)):
            room = Room.objects.create(num=j)
            Hotelroom.objects.create(room=room, hotel=hotel, price=random.randint(1, 5) * 1000)
