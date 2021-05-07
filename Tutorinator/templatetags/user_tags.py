from django import template 

#this file will allow us to hide/show parts of the file depending on user groups, don't know why it works
#but it does and that's good enough for me


register = template.Library()

@register.filter('in_group')
def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()