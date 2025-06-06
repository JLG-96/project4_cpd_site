from django.urls import path
from .views import (home,
                    results_view,
                    fixtures_view,
                    league_table,
                    manager_dashboard,
                    player_dashboard,
                    edit_manager_post,
                    edit_comment,
                    delete_comment,
                    mark_notification_read,
                    edit_manager_message,
                    delete_manager_message,
                    delete_manager_post,
                    add_comment,
                    register_user
                    )
from django.contrib.auth.views import LogoutView


urlpatterns = [
     path('', home, name='home'),
     path('results/', results_view, name='results'),
     path('fixtures/', fixtures_view, name='fixtures'),
     path('table/', league_table, name='league_table'),
     path("manager-dashboard/", manager_dashboard, name="manager_dashboard"),
     path("player-dashboard/", player_dashboard, name="player_dashboard"),
     path("accounts/logout/", LogoutView.as_view(next_page="home"),
          name="logout"),
     path("manager_post/edit/<int:post_id>/", edit_manager_post,
          name="edit_manager_post"),
     path("comment/edit/<int:comment_id>/", edit_comment, name="edit_comment"),
     path("comment/delete/<int:comment_id>/", delete_comment,
          name="delete_comment"),
     path("notification/read/<int:notification_id>/", mark_notification_read,
          name="mark_notification_read"),
     path("manager-message/edit/<int:message_id>/", edit_manager_message,
          name="edit_manager_message"),
     path("manager-message/delete/<int:message_id>/", delete_manager_message,
          name="delete_manager_message"),
     path("delete-manager-post/<int:post_id>/", delete_manager_post,
          name="delete_manager_post"),
     path("add-comment/<int:message_id>/", add_comment, name="add_comment"),
     path("register/", register_user, name="register"),

    ]
