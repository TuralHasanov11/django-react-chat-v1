from django.shortcuts import render
from inventory import models
from django.contrib.postgres.search import (
    SearchQuery, SearchRank, SearchVector, SearchHeadline,
    TrigramSimilarity, TrigramDistance
)

# Create your views here.
def post_search(request):
  results = []

  if 'q' in request.GET:
      q = request.GET
    # 1.0.1 Standard textual queries (case sensitive)
      results = models.Product.objects.filter(name__contains=q)
      print(models.Product.objects.filter(name__contains=q).explain(verbose=True, analyze=True))
      print(models.Product.objects.filter(name__contains=q).query)

    # # 1.0.2 Standard textual queries (case insensitive)      
      results = models.Product.objects.filter(name__icontains=q)
        
    # 1.0.3 Full text search
      results = models.Product.objects.filter(name__search=q)

    # 1.0.4 SearchVector (search against multiple fields)
      results = models.Product.objects.annotate(search=SearchVector('name', 'price'),).filter(search=q)  

    # 1.0.5 Search Ranking
      vector = SearchVector('name', weight='A') + SearchVector('price', weight='B')
      query = SearchQuery(q)
      results = models.Product.objects.annotate(rank=SearchRank(vector, query, cover_density=True)).order_by('-rank')

    # 1.0.6 Search TrigramSimilarity & TrigramDistance
      results = models.Product.objects.annotate(similarity=TrigramSimilarity('name', q),).filter(similarity__gte=0.3).order_by('-similarity')
      results = models.Product.objects.annotate(distance=TrigramDistance('name', q),).filter(distance__lte=0.8).order_by('distance')

    # 1.0.7 Search Headline
      query = SearchQuery(q)
      vector = SearchVector('price')
      results = models.Product.objects.annotate(search=vector, headline=SearchHeadline('price', query, start_sel='<span>', stop_sel='</span>', )).filter(search=query)

      from django.contrib.postgres.search import TrigramSimilarity

      print("#1")
      print(models.Product.objects.filter(name__trigram_similar=q).explain(analyze=True))
      print("#2")
      print(models.Product.objects.filter(name__trigram_similar=q).annotate(similar=TrigramSimilarity('name', q)).order_by('-similar').explain(analyze=True))


  return render(request, 'index.html', {'results':results, 'q':q})