# Create your views here.
def category_browse(request):
    # List all categories
    pass

def category_filter(request):
    # Filter by category (maybe use search engine?)
    # No templates yet, just prints out the query
    if request.method == 'GET':
        q_string = request.GET['categories']
        categories = q_string.split(' ')
        for category in categories:
            print category
    else:
        pass

