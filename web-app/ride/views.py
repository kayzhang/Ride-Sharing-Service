from django.contrib import messages
from .models import Post
from django.shortcuts import redirect, render
from .forms import RideCreationForm, ShareUpdateForm
from .models import Ride, Share
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.mail import send_mail
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'ride/home.html', context)

def about(request):
    return render(request, 'ride/about.html', {'title': 'About'})

def owner(request):
    return render(request, 'ride/owner.html')

def sharer(request):
    return render(request, 'ride/sharer.html')

def driver(request):
    return render(request, 'ride/driver.html')

class RideListView(ListView):
    model = Ride

class OwnerRideListView(ListView):
    template_name = 'ride/ride_list.html'
    def get_queryset(self):
        return Ride.objects.filter(owner=self.request.user).exclude(status=2).order_by('-start_date')

class ShareRideListView(ListView):
    def get_queryset(self):
        return Ride.objects.filter(share_name=self.request.user.username).exclude(status=2).order_by('-start_date')

class DriverListView(ListView):
    template_name = 'ride/driver_list.html'
    def get_queryset(self):
        return Ride.objects.filter(status=0, pas_num__lte=self.request.user.profile.max_pas_num).order_by('-start_date')

def share_view(request):
    context = {
        'object_list': Ride.objects.filter(share_name=request.user.username).exclude(status=2).order_by('-start_date')
    }
    return render(request, 'ride/share_view.html', context)

def driver_view(request):
    context = {
        'object_list': Ride.objects.filter(driver_name=request.user.username).exclude(status=2).order_by('-start_date')
    }
    return render(request, 'ride/driver_view.html', context)

class SharePickRideListView(ListView):
    template_name = 'ride/share_list.html' # <app>/<model>_<viewtype>.html
    def get_queryset(self):
        share = self.request.user.share_set.last()
        return Ride.objects.filter(share_valid=True,
                                   des=share.des,
                                   start_date__gte=share.start_date_0,
                                   start_date__lte=share.start_date_1,
                                   arrive_date__gte=share.arrive_date_0,
                                   arrive_date__lte=share.arrive_date_1,
                                   pas_num__gte=share.pas_num,
                                   status=0
                                   ).exclude(owner=self.request.user).order_by('-start_date')

class ShareCreateView(LoginRequiredMixin, CreateView):
    model = Share
    fields = ['des', 'start_date_0', 'start_date_1', 'arrive_date_0', 'arrive_date_1', 'pas_num']
    #success_url = "{% url 'ride:share-list' %}"

    def form_valid(self, form):
        form.instance.sharer = self.request.user
        return super().form_valid(form)

class ShareRideListView(ListView):
    def get_queryset(self):
        return Ride.objects.filter(owner=self.request.user).exclude(status=2).order_by('-start_date')

class RideDetailView(DetailView):
    model = Ride

class RideCreateView(LoginRequiredMixin, CreateView):
    model = Ride
    fields = ['des', 'start_date', 'arrive_date', 'pas_num', 'share_valid', 'share_max_num']

    # def get_form(self):
    #     form = super(RideCreateView, self).get_form()
    #     form.fields['start_date'].widget.attrs.update({'class': 'datepicker'})
    #     return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class RideUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ride
    fields = ['des', 'start_date', 'arrive_date', 'pas_num', 'share_valid', 'share_max_num']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        ride = self.get_object()
        if self.request.user == ride.owner:
            return True
        return False

class ShareUpdateView(LoginRequiredMixin, UpdateView):
    model = Ride
    fields = ['share_number']

class RideDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ride
    success_url = '/owner/view/'

    def test_func(self):
        ride = self.get_object()
        if self.request.user == ride.owner:
            return True
        return False

def owner_request(request):
    if request.method == 'POST':
        form = RideCreationForm(request.POST)
        if form.is_valid():
            #form.owner_name = request.user.username
            form.save()
            #record = RequestRide.objects.last()
            #record.owner_name = request.user.username
            #form.save()
            messages.success(request, f'Your request has been created!')
            return redirect('ride:owner-home')
    else:
        form = RideCreationForm(request.POST)
    context = {
        'form': form,
    }
    return render(request, 'ride/owner_request.html', context)


def share_update(request, ride_id):
    if request.method == 'POST':
        form = ShareUpdateForm(request.POST)
        if form.is_valid():
            #form.owner_name = request.user.username
            form.save()
            #record = RequestRide.objects.last()
            #record.owner_name = request.user.username
            #form.save()
            messages.success(request, f'Your ride has been updated!')
            return redirect('ride:share-view')
    else:
        form = ShareUpdateForm(request.POST)
    context = {
        'form': form,
    }
    return render(request, 'ride/share_update.html', context)

def owner_view(request):
    Records = RequestRide.objects.filter(owner_name=request.user.username).exclude(status = 2)
    #Records = RequestRide.objects.exclude(status = 2)
    return render(request, 'ride/owner_view.html', {'Records': Records})

def owner_edit(request, request_id):
    record = RequestRide.objects.filter(pk = request_id).first()
    if request.method == 'POST':
        form = RideCreationForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your request has been updated!')
            return redirect('ride:owner_view')
    else:
        form = RideCreationForm(instance=record)
    context = {
        'form': form,
    }
    return render(request, 'ride/owner_edit.html', context)

def share_join(request, ride_id):
    ride = Ride.objects.filter(pk=ride_id).first()
    share = Share.objects.all().last()
    ride.share_number = share.pas_num
    ride.share_name = request.user.username
    ride.save()
    return redirect('ride:share-list')

def share_cancel(request, ride_id):
    ride = Ride.objects.filter(pk=ride_id).first()
    share = Share.objects.all().last()
    ride.share_number = 0
    ride.share_name = 0
    ride.save()
    return redirect('ride:share-view')

def driver_confirm(request, ride_id):
    ride = Ride.objects.filter(pk=ride_id).first()
    sharer = User.objects.filter(username=ride.share_name).first()
    ride.driver_name = request.user.username
    ride.status = 1  # 1: confirmed
    ride.vehicle_type = request.user.profile.vehicle_type
    ride.license_plate_number = request.user.profile.license_plate_number
    ride.max_pas_num = request.user.profile.max_pas_num
    ride.save()
    send_mail(
        'Ride Confirmation Reminder',
        'Hi. You picked the ride successfully. Have a good trip!',
        'Duke myuber team',
        [request.user.email],
        fail_silently=False,
    )
    send_mail(
        'Ride Confirmation Reminder',
        'Hi. The ride that you requested has been confirmed by a driver successfully. Have a good trip!',
        'Duke myuber team',
        [ride.owner.email],
        fail_silently=False,
    )
    if sharer:
        send_mail(
            'Ride Confirmation Reminder',
            'Hi. The ride that you want to share has been confirmed by a driver successfully. Have a good trip!',
            'Duke myuber team',
            [sharer.email],
            fail_silently=False,
        )
    return redirect('ride:driver-request')

def driver_complete(request, ride_id):
    ride = Ride.objects.filter(pk=ride_id).first()
    ride.driver_name = request.user.username
    ride.status = 2  # 2: complete
    ride.save()
    return redirect('ride:driver-view')
