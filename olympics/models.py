from django.db import models

RUSSIA_CODE = 'RUS'


# this is all inefficient af but if we stick it behind a cache it will be ok

class Country(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=20, default='Unknown')

    def is_russia(self):
        return self.code == RUSSIA_CODE

    def gold_count(self, ignore_russia):
        if ignore_russia:
            return self.gold_medals.count()

        return self.gold_medals.count() + sum(1 for x in self.silver_medals.all() if x.russia_has_gold())

    def silver_count(self, ignore_russia):
        if not ignore_russia:
            return self.silver_medals.count()

        return sum(1 for x in self.silver_medals.all() if not (x.russia_has_gold())) \
            + sum(1 for x in self.bronze_medals.all() if x.russia_has_silver_or_above())

    def bronze_count(self, ignore_russia):
        if not ignore_russia:
            return self.bronze_medals.count()

        return sum(1 for x in self.bronze_medals.all() if not (x.russia_has_silver_or_above())) \
            + sum(1 for x in self.fourth_wins.all() if x.russia_has_bronze_or_above())

    def total_medals(self, ignore_russia):
        return self.gold_count(ignore_russia) + self.silver_count(ignore_russia) + self.bronze_count(ignore_russia)


class Event(models.Model):
    name = models.CharField(max_length=50)
    discipline = models.CharField(max_length=50)
    gold_winner = models.ForeignKey(Country, related_name='gold_medals', null=True)
    silver_winner = models.ForeignKey(Country, related_name='silver_medals', null=True)
    bronze_winner = models.ForeignKey(Country, related_name='bronze_medals', null=True)
    fourth_place = models.ForeignKey(Country, related_name='fourth_wins', null=True)

    def russia_has_placing(self):
        return self.gold_winner.is_russia() \
               or self.silver_winner.is_russia() \
               or self.bronze_winner.is_russia()

    def russia_has_gold(self):
        return self.gold_winner.is_russia()

    def russia_has_silver_or_above(self):
        return self.russia_has_gold() or self.silver_winner.is_russia()

    def russia_has_bronze_or_above(self):
        return self.russia_has_silver_or_above() or self.bronze_winner.is_russia()

    def get_placings(self, ignore_russia):
        return (country for country in (self.gold_winner, self.silver_winner, self.bronze_winner, self.fourth_place)
                if not (ignore_russia and country.is_russia()))[:3]
