from .models import Category

def categories_processor(request):
    main_categories = Category.objects.filter(parent=None).prefetch_related('subcategories')

    return {
        'main_categories': main_categories
    }