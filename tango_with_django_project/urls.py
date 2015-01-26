from django.conf.urls import patterns, include, url
from django.contrib import admin
<<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static


if not settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tango_with_django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

=======

urlpatterns = patterns('',
>>>>>>> abdf291b10d8f97959b4fea6b2b49787baffccdc
    url(r'^admin/', include(admin.site.urls)),
	url(r'^rango/', include('rango.urls')),
	url(r'^about/', include('rango.urls')),
)
<<<<<<< HEAD
if settings.DEBUG:
	urlpatterns += patterns(
	'django.views.static',
	(r'^media/(?P<path>.*)',
	'serve',
	{'document_root':settings.MEDIA_ROOT}),)
=======
>>>>>>> abdf291b10d8f97959b4fea6b2b49787baffccdc
