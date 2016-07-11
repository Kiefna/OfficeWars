from ajax_select import register, LookupChannel
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Office


@register('username')
class PlayersLookup(LookupChannel):
    model = User

    def check_auth(self, request):
        if request.user.is_authenticated():
            return True

    def get_query(self, q, request):
        return self.model.objects.filter(Q(username__icontains=q)).order_by('username')[:5]

    def format_item_display(self, item):
        return u"<span>%s</span>" % item.username

    def get_result(self, obj):
        """ result is the simple text that is the completion of what the person typed """
        return obj.username

    def get_objects(self, ids):
        return self.model.objects.filter(pk__in=ids).order_by('username')

    # def format_item_display(self, item):
    #     """ (HTML) formatted item for displaying item in the selected deck area """
    #     return u"<span>%s</span>" % (escape(item.username))

    def format_match(self, obj):
        return self.format_item_display(obj)

        # def check_auth(self, request):
        #     if not request.user.is_authenticated() or not request.user.has_beta_access:
        #         raise PermissionDenied

        # def check_auth(self, request):
        #     if request.user.get_profile():
        #         return True


@register('office')
class OfficeLookup(LookupChannel):
    model = Office

    def check_auth(self, request):
        if request.user.is_authenticated():
            return True

    def get_query(self, q, request):
        return self.model.objects.filter(Q(officeName__icontains=q)).order_by('officeName')[:5]

    def format_item_display(self, item):
        return u"""
            <a href='../officeView/%s'>
                <div style='border-radius: 0; vertical-align:top; display: inline-block; overflow: hidden; margin-top: 0'>
                    <img style='float: left; height: 40px; width: 40px; margin: 5px; border: solid black 1px; border-radius: 20px;' src='../media/%s'>
                    <div style='float: left; font-family: SF-Laundromat; margin-top: 5px;'>
                        <p style='color: antiquewhite; text-shadow: -1px 0 black, 0 1px black, 1px 0 black, 0 -1px black;'>Name : %s</p>
                        <p style='color: aquamarine; text-shadow: -1px 0 black, 0 1px black, 1px 0 black, 0 -1px black;'>Type : %s</p>
                    </div>
                </div>
            </a>
            """ % (item.slug, item.officeShield, item.officeName, item.officeType)

    def get_result(self, obj):
        """ result is the simple text that is the completion of what the person typed """
        return obj.officeName

    def get_objects(self, ids):
        return self.model.objects.filter(pk__in=ids).order_by('officeName')

    # def format_item_display(self, item):
    #     """ (HTML) formatted item for displaying item in the selected deck area """
    #     return u"<span>%s</span>" % (escape(item.username))

    def format_match(self, obj):
        return self.format_item_display(obj)

        # def check_auth(self, request):
        #     if not request.user.is_authenticated() or not request.user.has_beta_access:
        #         raise PermissionDenied

        # def check_auth(self, request):
        #     if request.user.get_profile():
        #         return True
