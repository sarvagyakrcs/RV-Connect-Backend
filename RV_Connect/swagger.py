from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="RV Connect",
        default_version='v1',
        description="Its the API for our RV Connect APP",
        terms_of_service="https://guthib.com/",
        contact=openapi.Contact(email="mukundverma.cd22@rvce.edu.in"),
        license=openapi.License(name="N.A"),
    ),
    public=True,
)
