"""Decorators for zinnia.views"""
from django.template import RequestContext
from django.contrib.auth.views import login
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache

from zinnia.models import Entry

def update_queryset(view, queryset,
                    queryset_parameter='queryset'):
    """Decorator around views based on a queryset
    passed in parameter, who will force the update
    of the queryset before executing the view.
    Related to issue http://code.djangoproject.com/ticket/8378"""

    def wrap(*args, **kwargs):
        """Regenerate the queryset before passing it to the view."""
        kwargs[queryset_parameter] = queryset()
        return view(*args, **kwargs)

    return wrap

@csrf_protect
@never_cache
def password(request, entry):
    """Displays the password form and handle validation
    by setting the valid password in a cookie."""
    error = False
    if request.method == 'POST':
        if request.POST.get('password') == entry.password:
            request.session['zinnia_entry_%s_password' % entry.pk] = entry.password
            return redirect(entry)
        error = True
    return render_to_response('zinnia/password.html', {'error': error},
                              context_instance=RequestContext(request))

def protect_entry(view):
    """Decorator performing a security check if needed
    around the generic.date_based.entry_detail view"""

    def wrap(*ka, **kw):
        request = ka[0]
        entry = get_object_or_404(Entry, slug=kw['slug'],
                                  creation_date__year=kw['year'],
                                  creation_date__month=kw['month'],
                                  creation_date__day=kw['day'])

        if entry.login_required and not request.user.is_authenticated():
            return login(request, 'zinnia/login.html')
        if entry.password and entry.password != \
               request.session.get('zinnia_entry_%s_password' % entry.pk):
            return password(request, entry)
        return view(*ka, **kw)

    return wrap
