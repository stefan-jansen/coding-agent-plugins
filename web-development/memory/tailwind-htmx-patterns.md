# Tailwind + htmx Common Patterns

**Version**: 1.0.0
**Last Updated**: 2025-10-16

This document contains proven patterns for combining Tailwind CSS with htmx for dynamic, interactive web applications.

## Core Philosophy

- **Tailwind**: Utility-first CSS for rapid UI development
- **htmx**: Declarative AJAX for server-side rendered apps
- **Together**: Build dynamic UIs without complex JavaScript frameworks

## Pattern 1: Dynamic Content Loading

**Use Case**: Load content from server without page reload

**HTML + htmx**:
```html
<div hx-get="/api/posts/latest"
     hx-trigger="load"
     hx-swap="innerHTML"
     class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div class="loading loading-spinner loading-lg"></div>
</div>
```

**Django View**:
```python
def latest_posts(request):
    posts = Post.objects.all()[:10]
    return render(request, 'partials/post-grid.html', {'posts': posts})
```

**Partial Template** (`partials/post-grid.html`):
```html
{% for post in posts %}
<div class="card bg-base-100 shadow-xl">
  <div class="card-body">
    <h2 class="card-title">{{ post.title }}</h2>
    <p>{{ post.excerpt }}</p>
    <div class="card-actions justify-end">
      <a href="{% url 'post_detail' post.pk %}" class="btn btn-primary">Read More</a>
    </div>
  </div>
</div>
{% endfor %}
```

**Benefits**:
- Server returns HTML (no JSON parsing)
- Tailwind classes work immediately
- No client-side templating needed

## Pattern 2: Form Submission with AJAX

**Use Case**: Submit form without page reload, show validation errors

**HTML + htmx**:
```html
<form hx-post="{% url 'create_post' %}"
      hx-target="#form-result"
      hx-swap="outerHTML"
      class="space-y-4">
  {% csrf_token %}
  <div class="form-control">
    <label class="label">
      <span class="label-text">Title</span>
    </label>
    <input type="text"
           name="title"
           class="input input-bordered w-full"
           required>
  </div>

  <div class="form-control">
    <label class="label">
      <span class="label-text">Content</span>
    </label>
    <textarea name="content"
              class="textarea textarea-bordered w-full"
              rows="5"
              required></textarea>
  </div>

  <button type="submit" class="btn btn-primary">Submit</button>
</form>

<div id="form-result"></div>
```

**Django View**:
```python
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'partials/success-message.html')
        else:
            return render(request, 'partials/form-errors.html', {'form': form})
```

**Success Partial** (`partials/success-message.html`):
```html
<div class="alert alert-success">
  <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
  <span>Post created successfully!</span>
</div>
```

**Error Partial** (`partials/form-errors.html`):
```html
{% if form.errors %}
<div class="alert alert-error">
  <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
  <div>
    {% for field, errors in form.errors.items %}
      <div><strong>{{ field }}:</strong> {{ errors|join:", " }}</div>
    {% endfor %}
  </div>
</div>
{% endif %}
```

## Pattern 3: Real-time Updates (Polling)

**Use Case**: Dashboard metrics that update every few seconds

**HTML + htmx**:
```html
<div hx-get="{% url 'dashboard_metrics' %}"
     hx-trigger="every 10s"
     hx-swap="innerHTML"
     class="stats shadow w-full">
  <!-- Initial loading state -->
  <div class="stat">
    <div class="stat-title">Loading...</div>
  </div>
</div>
```

**Django View**:
```python
def dashboard_metrics(request):
    metrics = {
        'users_online': get_online_users_count(),
        'total_posts': Post.objects.count(),
        'new_today': Post.objects.filter(created_at__date=date.today()).count()
    }
    return render(request, 'partials/metrics.html', metrics)
```

**Partial Template** (`partials/metrics.html`):
```html
<div class="stat">
  <div class="stat-figure text-primary">
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="inline-block w-8 h-8 stroke-current">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
    </svg>
  </div>
  <div class="stat-title">Users Online</div>
  <div class="stat-value text-primary">{{ users_online }}</div>
</div>

<div class="stat">
  <div class="stat-title">Total Posts</div>
  <div class="stat-value">{{ total_posts }}</div>
  <div class="stat-desc">{{ new_today }} created today</div>
</div>
```

## Pattern 4: Infinite Scroll

**Use Case**: Load more items as user scrolls

**HTML + htmx**:
```html
<div class="space-y-4">
  {% for post in posts %}
  <div class="card bg-base-100 shadow-xl">
    <div class="card-body">
      <h2 class="card-title">{{ post.title }}</h2>
      <p>{{ post.excerpt }}</p>
    </div>
  </div>
  {% endfor %}

  {% if has_more %}
  <div hx-get="/api/posts?page={{ next_page }}"
       hx-trigger="intersect once"
       hx-swap="afterend"
       class="text-center py-4">
    <span class="loading loading-spinner loading-lg"></span>
  </div>
  {% endif %}
</div>
```

**Django View**:
```python
from django.core.paginator import Paginator

def post_list(request):
    page_num = int(request.GET.get('page', 1))
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page = paginator.get_page(page_num)

    return render(request, 'partials/post-list.html', {
        'posts': page.object_list,
        'has_more': page.has_next(),
        'next_page': page.next_page_number() if page.has_next() else None
    })
```

## Pattern 5: Modal Dialogs

**Use Case**: Open content in modal without page navigation

**Trigger Button**:
```html
<button hx-get="/posts/123/edit"
        hx-target="#modal-content"
        onclick="document.getElementById('edit-modal').showModal()"
        class="btn btn-primary">
  Edit Post
</button>
```

**Modal Container**:
```html
<dialog id="edit-modal" class="modal">
  <div class="modal-box">
    <div id="modal-content">
      <!-- Content loaded via htmx -->
    </div>
  </div>
  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>
```

**Django View** (returns form HTML):
```python
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(instance=post)
    return render(request, 'partials/edit-form.html', {'form': form, 'post': post})
```

**Form in Modal** (`partials/edit-form.html`):
```html
<h3 class="font-bold text-lg">Edit Post</h3>
<form hx-put="/posts/{{ post.pk }}/update"
      hx-target="#modal-content"
      class="py-4 space-y-4">
  {% csrf_token %}

  <div class="form-control">
    <label class="label">
      <span class="label-text">Title</span>
    </label>
    {{ form.title }}
  </div>

  <div class="modal-action">
    <button type="submit" class="btn btn-primary">Save</button>
    <button type="button"
            class="btn"
            onclick="document.getElementById('edit-modal').close()">
      Cancel
    </button>
  </div>
</form>
```

## Pattern 6: Search with Debouncing

**Use Case**: Live search as user types (with delay to reduce requests)

**HTML + htmx**:
```html
<div class="form-control">
  <input type="search"
         name="q"
         placeholder="Search posts..."
         class="input input-bordered w-full"
         hx-get="/search"
         hx-trigger="keyup changed delay:500ms"
         hx-target="#search-results">
</div>

<div id="search-results" class="mt-4">
  <!-- Results appear here -->
</div>
```

**Django View**:
```python
def search(request):
    query = request.GET.get('q', '')
    if len(query) < 3:
        return HttpResponse('<p class="text-gray-500">Type at least 3 characters...</p>')

    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    )[:10]

    return render(request, 'partials/search-results.html', {'posts': posts, 'query': query})
```

**Results Partial** (`partials/search-results.html`):
```html
{% if posts %}
<div class="menu bg-base-100 rounded-box">
  {% for post in posts %}
  <li>
    <a href="{% url 'post_detail' post.pk %}" class="flex justify-between">
      <span>{{ post.title }}</span>
      <span class="badge">{{ post.created_at|date:"M d" }}</span>
    </a>
  </li>
  {% endfor %}
</div>
{% else %}
<p class="text-gray-500">No results for "{{ query }}"</p>
{% endif %}
```

## Pattern 7: Delete Confirmation

**Use Case**: Confirm before deleting item

**HTML + htmx**:
```html
<button hx-delete="/posts/{{ post.pk }}"
        hx-confirm="Are you sure you want to delete this post?"
        hx-target="closest .card"
        hx-swap="outerHTML swap:1s"
        class="btn btn-error btn-sm">
  Delete
</button>
```

**Django View**:
```python
def delete_post(request, pk):
    if request.method == 'DELETE':
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return HttpResponse('')  # Empty response removes element
```

**Tailwind Swap Animation** (add to tailwind.config.js):
```javascript
module.exports = {
  theme: {
    extend: {
      animation: {
        'fade-out': 'fadeOut 1s ease-in-out',
      },
      keyframes: {
        fadeOut: {
          '0%': { opacity: '1' },
          '100%': { opacity: '0' },
        }
      }
    }
  }
}
```

## Pattern 8: Loading States

**Use Case**: Show spinner while content loads

**HTML + htmx**:
```html
<button hx-get="/api/data"
        hx-target="#content"
        hx-indicator="#spinner"
        class="btn btn-primary">
  Load Data
</button>

<div id="spinner" class="htmx-indicator loading loading-spinner loading-lg"></div>

<div id="content"></div>
```

**CSS for htmx-indicator**:
```css
/* htmx adds .htmx-request to elements during requests */
.htmx-indicator {
  display: none;
}

.htmx-request .htmx-indicator {
  display: inline-block;
}

.htmx-request.htmx-indicator {
  display: inline-block;
}
```

**Or use htmx classes directly**:
```html
<button hx-get="/api/data"
        hx-target="#content"
        class="btn btn-primary">
  <span class="htmx-indicator loading loading-spinner"></span>
  <span>Load Data</span>
</button>
```

## Pattern 9: Optimistic Updates

**Use Case**: Update UI immediately, rollback if request fails

**HTML + htmx**:
```html
<button hx-post="/posts/{{ post.pk }}/like"
        hx-swap="outerHTML"
        class="btn btn-ghost btn-sm gap-2">
  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
    <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
  </svg>
  <span>{{ post.likes_count }}</span>
</button>
```

**Django View**:
```python
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.likes_count += 1
    post.save()

    return render(request, 'partials/like-button.html', {'post': post})
```

**With Error Handling**:
```html
<button hx-post="/posts/{{ post.pk }}/like"
        hx-swap="outerHTML"
        hx-on:htmx:after-request="if(event.detail.failed) alert('Failed to like post')"
        class="btn btn-ghost btn-sm">
  Like ({{ post.likes_count }})
</button>
```

## Pattern 10: File Upload with Progress

**Use Case**: Upload files with htmx

**HTML + htmx**:
```html
<form hx-post="/upload"
      hx-encoding="multipart/form-data"
      hx-target="#upload-result"
      class="space-y-4">
  {% csrf_token %}

  <div class="form-control">
    <label class="label">
      <span class="label-text">Choose file</span>
    </label>
    <input type="file"
           name="file"
           class="file-input file-input-bordered w-full"
           required>
  </div>

  <button type="submit" class="btn btn-primary">
    <span class="htmx-indicator loading loading-spinner"></span>
    Upload
  </button>
</form>

<div id="upload-result"></div>
```

**Django View**:
```python
def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        # Process file...
        return render(request, 'partials/upload-success.html', {
            'filename': uploaded_file.name,
            'size': uploaded_file.size
        })
```

## Best Practices

1. **Partial Templates**: Always use separate partials for htmx responses
2. **CSRF Tokens**: Include `{% csrf_token %}` or set headers for POST/PUT/DELETE
3. **Loading Indicators**: Always show loading state for user feedback
4. **Error Handling**: Use `hx-on` events to handle errors gracefully
5. **Debouncing**: Use `delay:` for search/autocomplete to reduce server load
6. **Target Specificity**: Use specific IDs/classes for `hx-target` to avoid side effects
7. **Swap Strategies**: Choose appropriate `hx-swap` (innerHTML, outerHTML, beforeend, etc.)
8. **Tailwind Purging**: Configure Tailwind to scan partial templates

**tailwind.config.js**:
```javascript
module.exports = {
  content: [
    './templates/**/*.html',
    './templates/partials/**/*.html',  // Don't forget partials!
  ],
  // ...
}
```

## Debugging Tips

1. **htmx Events**: Listen to htmx events in browser console
   ```javascript
   document.body.addEventListener('htmx:afterRequest', (e) => {
     console.log('Request complete:', e.detail);
   });
   ```

2. **Network Tab**: Check Chrome DevTools network tab for htmx requests

3. **htmx Extension**: Install htmx logging extension for debugging
   ```html
   <script src="https://unpkg.com/htmx.org/dist/ext/debug.js"></script>
   <body hx-ext="debug">
   ```

4. **Django Debug Toolbar**: Use for inspecting queries and performance

---

*These patterns are battle-tested with Tailwind CSS 3.4+ and htmx 1.9+*
*For DaisyUI components, wrap htmx-loaded content in DaisyUI classes*
