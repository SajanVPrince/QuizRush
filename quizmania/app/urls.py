from django.urls import path
from . import views

urlpatterns = [
# ---------------Login -----------

    path('login',views.q_login, name='login'),
    path('logout',views.q_logout , name='logout'),
    path('register',views.register , name='register'),
    path('verifyotp',views.verify_otp, name='verify_otp'),
    path('resend',views.resend_otp, name='resend_otp'),
    path('forget',views.forgetpassword , name='forgetpassword'),
    path('reset',views.resetpassword , name='resetpassword'),
    path('verify_otp_reg',views.verify_otp_reg, name='verify_otp_reg'),
    path('resend_otp_reg',views.resend_otp_reg, name='resend_otp_reg'),

# --------------Admin------------------

    path('adhome', views.adhome, name='adhome'),
    path('viewqst', views.viewqst, name='viewqst'),
    path('editqst/<int:question_id>', views.editqst, name='editqst'),
    path('adleader', views.adleaderboard),
    path('adpro', views.adpro),
    path('viewuser', views.player_list, name='player_list'),




    # ----------- User -----------
    path('', views.home, name='home'),
    path('home', views.home,),
    path('userpro', views.userpro,),
    path('start', views.start_quiz, name='start_quiz'),
    path('question', views.question, name='question'),
    path('check', views.check_answer, name='check_answer'),
    path('gameover', views.game_over, name='game_over'),
    path('edit_player/<int:id>', views.edit_player, name='edit_player'),
    path('leader', views.leaderboard),
    path('select_level', views.select_level, name='select_level'),

]