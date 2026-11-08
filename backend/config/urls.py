import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from config.settings import BASE_DIR


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/common/', include('common.urls')),

    path('api/captcha/' , include('captcha.urls')),

    path('api/auth/', include('accounts.urls', namespace='accounts')),

    path('api/initialborders/', include('initialborders.urls')),
    path('api/contracts/', include('contracts.urls')),
    path('api/layers/', include('layers.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
if settings.DEBUG:
    urlpatterns += static(
        "/glyphs/",
        document_root=os.path.join(BASE_DIR, "glyphs")
    )