from store.models import Collection

def collections_list_header(request):
    return {'collections_list_header': Collection.objects.all()}  # Assuming Collection is your model

def canonical_url(request):
    # Build the absolute URI and replace http with https
    canonical_url = request.build_absolute_uri(request.path)
    secure_canonical_url = canonical_url.replace('http://', 'https://')
    return {
        'canonical_url': secure_canonical_url
    }
