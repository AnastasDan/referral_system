from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]


urlpatterns += [
    path(
        "swagger/",
        TemplateView.as_view(
            template_name="swagger-ui.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="swagger",
    ),
    path(
        "redoc/",
        TemplateView.as_view(
            template_name="redoc.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="redoc",
    ),
]
