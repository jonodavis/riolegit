from django.shortcuts import render

# Create your views here.
from olympics.models import Country


def index(request):
    countries = Country.objects.all()
    sorted_countries = sorted(countries, key=lambda x: (-x.gold_medals.count(), -x.silver_medals.count(),
                                                        -x.bronze_medals.count()))
    viewmodel = [{'name': x.name,
                  'gold_medals': x.gold_count(False),
                  'silver_medals': x.silver_count(False),
                  'bronze_medals': x.bronze_count(False),
                  'gold_no_russia': x.gold_count(True),
                  'silver_no_russia': x.silver_count(True),
                  'bronze_no_russia': x.bronze_count(True),
                  'total_medals': x.total_medals(False),
                  'total_no_russia': x.total_medals(True)} for x in sorted_countries]
    return render(request, 'olympics/index.html', {'countries': viewmodel})
