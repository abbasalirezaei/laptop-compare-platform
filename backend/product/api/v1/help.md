# Django ORM Advanced Filtering Guide

## Understanding Q Objects

Q objects are a powerful feature in Django that enable complex database queries. They are especially useful when you need to:

- Construct OR conditions
- Apply NOT logic
- Build dynamic queries
- Combine multiple conditions

### Basic Q Object Syntax

```python
from django.db.models import Q

# Basic AND query
Product.objects.filter(Q(field1=value1) & Q(field2=value2))

# Basic OR query
Product.objects.filter(Q(field1=value1) | Q(field2=value2))

# NOT query
Product.objects.filter(~Q(field1=value1))
```

### Dynamic Query Building

Here's a common pattern for building dynamic queries:

```python
def filter_products(search=None, category=None):
    q = Q()  # Initialize empty Q object
    
    if search:
        q &= Q(name__icontains=search)  # AND condition
    if category:
        q &= Q(category=category)  # AND condition
    
    return Product.objects.filter(q)
```

### Common Query Examples

1. Search products by name and category:
```python
Product.objects.filter(
    Q(name__icontains="book") & Q(category="fiction")
)
```

2. Search products in multiple categories:
```python
Product.objects.filter(
    Q(category="fiction") | Q(category="non-fiction")
)
```

### Best Practices

1. Always import Q from django.db.models
2. Initialize empty Q objects with Q()
3. Use &= for AND operations
4. Use |= for OR operations
5. Use parentheses for complex queries
6. Chain filters for readability

### Common Operators

- `&`: AND
- `|`: OR
- `~`: NOT
- `__icontains`: Case-insensitive contains
- `__exact`: Exact match
- `__in`: In a list of values

Remember to apply filters to your queryset using:
```python
qs = qs.filter(q)
```

```

✅ Example: All in one
python
Copy
Edit
q = Q()
q |= Q(name__icontains="book")
q |= Q(description__icontains="book")
q &= ~Q(category="electronics")
Product.objects.filter(q)
👉 Returns products that:

Have "book" in name or description

And are not in category "electronics"
```
Time filtering:
