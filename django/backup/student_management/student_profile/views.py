from django.shortcuts import render, redirect
from .models import StudentProfile
from .forms import StudentProfileForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from student_profile.models import StudentProfile  # Import from the full module path


from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import UserSignupForm


def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            # Create the profile and associate it with the user
            StudentProfile.objects.create(
                user=user,
                full_name=form.cleaned_data.get('full_name'),
                date_of_birth=form.cleaned_data.get('date_of_birth'),
                address=form.cleaned_data.get('address'),
                phone_number=form.cleaned_data.get('phone_number'),
                email=user.email,  # Use the email from the User object
                start_date=form.cleaned_data.get('start_date')  # Capture start_date from the form
            )
            login(request, user)  # Log in the user automatically
            return redirect('profile_detail', pk=user.pk)
    else:
        form = UserSignupForm()
    
    return render(request, 'registration/signup.html', {'form': form})
@login_required
def create_profile(request):
    # Check if the user already has a profile
    try:
        profile = StudentProfile.objects.get(user=request.user)
        return redirect('profile_detail', pk=profile.pk)
    except StudentProfile.DoesNotExist:
        if request.method == 'POST':
            form = StudentProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                return redirect('profile_detail', pk=profile.pk)
        else:
            form = StudentProfileForm()
    return render(request, 'student_profile/create_profile.html', {'form': form})



def profile_detail(request, pk):
    from student_profile.models import StudentProfile  # Import inside the function
    profile = get_object_or_404(StudentProfile, pk=pk)
    return render(request, 'student_profile/profile_detail.html', {'profile': profile})


@login_required
def update_profile(request, pk):
    profile = get_object_or_404(StudentProfile, pk=pk)
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail', pk=profile.pk)
    else:
        form = StudentProfileForm(instance=profile)
    
    return render(request, 'student_profile/update_profile.html', {'form': form})
