from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Group, Cluster, Messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import HttpResponse
from .forms import GroupForm, UserForm

# Create your views here.

# groups = [
#     {'id': 1, 'name': 'Friends'},
#     {'id': 2, 'name': 'Family'},
#     {'id': 3, 'name': 'Colleagues'}
# ]

def loginForm(request):
    pageType = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if(request.method == "POST"):
        usern = request.POST.get("un").lower()
        passw = request.POST.get("pw")
        """
        try:
            currentUser =  User.objects.get(username = usern)
        except:
            messages.error(request, "User doesn't exist!!")
        """
        currentUser = authenticate(request, username = usern, password = passw)
        if currentUser is not None:
            login(request, currentUser)
            return redirect('home')
        else:
            return HttpResponse("Invalid credentials")

    context = {'pageType': pageType}
    return render(request, 'baseApp/registerAndLogin.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            newUser = form.save(commit = False)
            newUser.username = newUser.username.lower()
            newUser.save()
            login(request, newUser)
            return redirect('home')
        else:
            return HttpResponse("OOps! An error occured...")

    context = {'form':form}
    return render(request, 'baseApp/registerAndLogin.html', context)

def home(request):

    query = ''

    if(request.GET.get('f') != None):

        query = request.GET.get('f')
    
    groups = Group.objects.filter(Q(cluster__clusterName__icontains = query) | Q(GroupName__icontains = query) | Q(GroupDescription__icontains = query))
    grpCount = groups.count() 
    clusters = Cluster.objects.all()

    recent_msgs = Messages.objects.all().order_by("-created")[:5]

    context = {'grps': groups, 'clusters':clusters, 'group_count': grpCount, "feed":recent_msgs}
    #allows us to send the groups dictionary to homepage.html using context parameter.
    return render(request, 'baseApp/homepage.html', context)

def group(request, pk):
    grp = Group.objects.get(id = pk)
    msgs = grp.messages_set.all().order_by('-created')

    if request.method == "POST":
        newMessage = Messages.objects.create(
            user = request.user,
            group = grp,
            content = request.POST.get('newMessage')
        )
        return redirect('group', pk = grp.id)

    context = {"groups":grp, "messgs":msgs}
    return render(request, 'baseApp/group.html', context)

def userPage(request, pk):
    person = User.objects.get(id = pk)
    created_groups = person.group_set.all()
    clss = Cluster.objects.all()
    recent_msgs = person.messages_set.all().order_by("-created")[:5]
    context = {'persoon':person, 'createdGs':created_groups, 'feed': recent_msgs, 'clusters':clss}
    return render(request, 'baseApp/profilePage.html', context)

@login_required(login_url = 'userLogin')
def create_group(request):
    form = GroupForm()
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            temporary_grp = form.save(commit = False)
            temporary_grp.admin = request.user
            temporary_grp.save()
            return redirect('home')
    context = {'groupForm':form}
    return render(request, 'baseApp/create_group.html', context)

@login_required(login_url = 'userLogin')
def edit_group(request, pk):
    grp = Group.objects.get(id = pk)
    form = GroupForm(instance = grp)
    if(request.method == "POST"):
        form = GroupForm(request.POST, instance = grp)
        if(form.is_valid()):
            form.save()
            return redirect('home')
    context = {'groupForm':form}
    return render(request, 'baseApp/create_group.html', context)

@login_required(login_url = 'userLogin')
def deleteGroup(request, pk):
    obj = "group"
    group = Group.objects.get(id = pk)
    if(request.method == "POST"):
        group.delete()
        return redirect('home')
    context = {'entity':group, "obj":obj}
    return render(request, 'baseApp/delObjects.html', context)

@login_required(login_url = 'userLogin')
def deleteMessage(request, pk):
    message = Messages.objects.get(id = pk)
    if(request.method == "POST"):
        message.delete()
        return redirect('home')
    context = {'entity':message}
    return render(request, 'baseApp/delObjects.html', context)

@login_required(login_url = 'userLogin')
def editUser(request):
    user = UserForm(instance = request.user)
    if(request.method == "POST"):
        user = UserForm(request.POST, instance = request.user)
        if(user.is_valid()):
            user.save()
            return redirect('user_profile', pk = request.user.id)
    context = {'userData':user}
    return render(request, 'baseApp/editUser.html', context)