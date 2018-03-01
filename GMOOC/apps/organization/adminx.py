#_*_ conding:utf-8 _*_
import xadmin
from xadmin import views
from .models import CityDict,CourseOrganization,Teacher

class CityDictAdmin(object):
    list_display = ['CityName','CityDescribe','AddTime']
    search_fields = ['CityName','CityDescribe']
    list_filter = ['CityName','CityDescribe','AddTime']

#利用 admin.site.register 进行注册
xadmin.site.register(CityDict,CityDictAdmin)

class CourseOrganizationAdmin(object):
    list_display = ['Organization','OrganizationDescribe','ClickNumber','FavoriteNumber','OrganizationImage','Address','City','AddTime']
    search_fields = ['Organization','OrganizationDescribe','ClickNumber','FavoriteNumber','OrganizationImage','Address','City']
    list_filter = ['Organization','OrganizationDescribe','ClickNumber','FavoriteNumber','OrganizationImage','Address','City','AddTime']

#利用 admin.site.register 进行注册
xadmin.site.register(CourseOrganization,CourseOrganizationAdmin)

class TeacherAdmin(object):
    list_display = ['BelongOrganization','TeacherName','WorkLife','WorkCompany','WorkPosition','Point','ClickNumber','FavoriteNumber','AddTime']
    search_fields = ['BelongOrganization','TeacherName','WorkLife','WorkCompany','WorkPosition','Point','ClickNumber','FavoriteNumber']
    list_filter = ['BelongOrganization','TeacherName','WorkLife','WorkCompany','WorkPosition','Point','ClickNumber','FavoriteNumber','AddTime']

#利用 admin.site.register 进行注册
xadmin.site.register(Teacher,TeacherAdmin)

