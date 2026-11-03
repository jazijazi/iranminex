from django.urls import path, include

from ticket.views import (
    TicketListApiView , 
    TicketDetailApiView , 
    TicketChangeStatusApiView ,

    TicketCommentListApiView , 
    TicketCommentDetailApiView , 
)

# perifix is /ticket
urlpatterns = [
    path('' , TicketListApiView.as_view(), name='ticket-list'),
    path('<int:pk>/' , TicketDetailApiView.as_view(), name='ticket-detail'),
    path('<int:pk>/changestatus/' , TicketChangeStatusApiView.as_view(), name='ticket-changestatus'),

    path('<int:ticketid>/comment/' , TicketCommentListApiView.as_view(), name='ticket-comment-list'),
    path('comment/<int:pk>/' , TicketCommentDetailApiView.as_view(), name='ticket-comment-detail'),

]