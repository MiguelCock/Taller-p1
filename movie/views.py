from django.shortcuts import render

from .models import Movie

import matplotlib.pyplot as plt
import matplotlib
import io
import base64

# Create your views here.

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()

    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def about(request):
	return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def stadistics_view(request):

    #===========graph 1===========

    matplotlib.use('Agg')
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')

    movie_counts_by_year = {}
    for year in years:
        if year :
            movie_in_year = Movie.objects.filter(year=year)
        else:
            movie_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movie_in_year.count()
        movie_counts_by_year[year] = count

    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))

    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)

    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic1 = base64.b64encode(image_png)
    graphic1 = graphic1.decode('utf-8')

    #===========graph 2===========

    matplotlib.use('Agg')
    genres = Movie.objects.values_list('genre', flat=True).distinct()

    movie_counts_by_genre = {}
    for genre in genres:
        if genre :
            movie_by_genre = Movie.objects.filter(genre=genre)
        else:
            movie_by_genre = Movie.objects.filter(genre__isnull=True)
            genre = "None"
        count = movie_by_genre.count()
        movie_counts_by_genre[genre] = count

    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_genre))

    plt.bar(bar_positions, movie_counts_by_genre.values(), width=bar_width, align='center')
    
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_genre.keys(), rotation=90)

    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic2 = base64.b64encode(image_png)
    graphic2 = graphic2.decode('utf-8')

    return render(request, 'statistics.html', {'graphic1': graphic1, 'graphic2': graphic2})