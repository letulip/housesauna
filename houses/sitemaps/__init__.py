from .index import IndexViewSiteMap
from .static import StaticViewSiteMap
from .categories import CategoryHouseSitemap, CategorySaunaSitemap
from .subcategories import SubCategoryHouseSitemap, SubCategorySaunaSitemap
from .houses import HouseSitemap
from .saunas import SaunaSitemap
from .projects import ProjectSitemap

sitemaps = {
    'index': IndexViewSiteMap,
    'static': StaticViewSiteMap,
    'saunas_categories': CategorySaunaSitemap,
    'houses_categories': CategoryHouseSitemap,
    'saunas_subcategories': SubCategorySaunaSitemap,
    'houses_subcategories': SubCategoryHouseSitemap,
    'houses': ProjectSitemap,
    'saunas': SaunaSitemap,
    'projects': ProjectSitemap,
}
