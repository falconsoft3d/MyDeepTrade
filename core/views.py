from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Model, Agent, Transaction, UserProfile, WorkOrder
import requests
import json


def home(request):
    """Vista de la página principal"""
    return render(request, 'home.html')


def register_view(request):
    """Vista de registro de usuarios"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """Vista de inicio de sesión"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome {username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


@login_required
def dashboard_view(request):
    """Vista del dashboard (requiere autenticación)"""
    # Get KPI counts
    agents_count = Agent.objects.count()
    models_count = Model.objects.count()
    transactions_count = Transaction.objects.count()
    active_agents_count = Agent.objects.filter(is_active=True).count()
    
    context = {
        'user': request.user,
        'agents_count': agents_count,
        'models_count': models_count,
        'transactions_count': transactions_count,
        'active_agents_count': active_agents_count,
    }
    return render(request, 'dashboard.html', context)


def logout_view(request):
    """Logout view"""
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('home')


@login_required
def user_list(request):
    """User list view"""
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'users/user_list.html', {'users': users})


@login_required
def user_create(request):
    """Create user view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully!')
            return redirect('user_list')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = UserCreationForm()
    
    return render(request, 'users/user_create.html', {'form': form})


@login_required
def profile_view(request):
    """User profile view"""
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update user data
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        # Update profile data
        profile.bio = request.POST.get('bio', '')
        profile.phone = request.POST.get('phone', '')
        
        # Handle avatar upload
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'profile.html', {'profile': profile})


@login_required
def change_password_view(request):
    """Change password view"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {'form': form})


@login_required
def transaction_list(request):
    """Transaction list view"""
    transactions = Transaction.objects.all()
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions})


@login_required
def transaction_create(request):
    """Create transaction view"""
    if request.method == 'POST':
        type = request.POST.get('type')
        cant = request.POST.get('cant')
        price = request.POST.get('price')
        
        if type and cant and price:
            Transaction.objects.create(
                type=type,
                cant=cant,
                price=price
            )
            messages.success(request, 'Transaction created successfully!')
            return redirect('transaction_list')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'transactions/transaction_create.html')


@login_required
def transaction_edit(request, pk):
    """Edit transaction view"""
    transaction = get_object_or_404(Transaction, pk=pk)
    
    if request.method == 'POST':
        transaction.type = request.POST.get('type')
        transaction.cant = request.POST.get('cant')
        transaction.price = request.POST.get('price')
        transaction.save()
        messages.success(request, 'Transaction updated successfully!')
        return redirect('transaction_list')
    
    return render(request, 'transactions/transaction_edit.html', {'transaction': transaction})


@login_required
def transaction_delete(request, pk):
    """Delete transaction view"""
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()
    messages.success(request, 'Transaction deleted successfully!')
    return redirect('transaction_list')


@login_required
def workorder_list(request):
    """Work order list view"""
    workorders = WorkOrder.objects.all()
    return render(request, 'workorders/workorder_list.html', {'workorders': workorders})


@login_required
def workorder_create(request):
    """Create work order view"""
    if request.method == 'POST':
        agent_id = request.POST.get('agent')
        prompt = request.POST.get('prompt')
        status = request.POST.get('status')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        
        if agent_id and prompt and status and start_time and end_time:
            WorkOrder.objects.create(
                agent_id=agent_id,
                prompt=prompt,
                status=status,
                start_time=start_time,
                end_time=end_time
            )
            messages.success(request, 'Work order created successfully!')
            return redirect('workorder_list')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    agents = Agent.objects.all()
    return render(request, 'workorders/workorder_create.html', {'agents': agents})


@login_required
def workorder_edit(request, pk):
    """Edit work order view"""
    workorder = get_object_or_404(WorkOrder, pk=pk)
    
    if request.method == 'POST':
        workorder.agent_id = request.POST.get('agent')
        workorder.prompt = request.POST.get('prompt')
        workorder.status = request.POST.get('status')
        workorder.start_time = request.POST.get('start_time')
        workorder.end_time = request.POST.get('end_time')
        workorder.save()
        messages.success(request, 'Work order updated successfully!')
        return redirect('workorder_list')
    
    agents = Agent.objects.all()
    return render(request, 'workorders/workorder_edit.html', {'workorder': workorder, 'agents': agents})


@login_required
def workorder_delete(request, pk):
    """Delete work order view"""
    workorder = get_object_or_404(WorkOrder, pk=pk)
    workorder.delete()
    messages.success(request, 'Work order deleted successfully!')
    return redirect('workorder_list')


@login_required
def model_list(request):
    """Model list view"""
    models = Model.objects.all()
    return render(request, 'models/model_list.html', {'models': models})


@login_required
def model_create(request):
    """Create model view"""
    if request.method == 'POST':
        name = request.POST.get('name')
        type = request.POST.get('type')
        apikey = request.POST.get('apikey', '')
        paikey = request.POST.get('paikey', '')
        
        if name and type:
            Model.objects.create(name=name, type=type, apikey=apikey, paikey=paikey)
            messages.success(request, 'Model created successfully!')
            return redirect('model_list')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'models/model_create.html')


@login_required
def model_edit(request, pk):
    """Edit model view"""
    model = get_object_or_404(Model, pk=pk)
    
    if request.method == 'POST':
        model.name = request.POST.get('name')
        model.type = request.POST.get('type')
        model.apikey = request.POST.get('apikey', '')
        model.paikey = request.POST.get('paikey', '')
        model.save()
        messages.success(request, 'Model updated successfully!')
        return redirect('model_list')
    
    return render(request, 'models/model_edit.html', {'model': model})


@login_required
def model_delete(request, pk):
    """Delete model view"""
    model = get_object_or_404(Model, pk=pk)
    model.delete()
    messages.success(request, 'Model deleted successfully!')
    return redirect('model_list')


@login_required
def agent_list(request):
    """Agent list view"""
    agents = Agent.objects.all().select_related('ai_model')
    return render(request, 'agents/agent_list.html', {'agents': agents})


@login_required
def agent_create(request):
    """Create agent view"""
    if request.method == 'POST':
        name = request.POST.get('name')
        descripcion = request.POST.get('descripcion')
        ai_model_id = request.POST.get('ai_model')
        prompt = request.POST.get('prompt')
        is_active = request.POST.get('is_active') == 'on'
        periodicity_value = request.POST.get('periodicity_value')
        periodicity_unit = request.POST.get('periodicity_unit')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        
        if name and descripcion and ai_model_id and prompt and periodicity_value and start_time and end_time:
            Agent.objects.create(
                name=name,
                descripcion=descripcion,
                ai_model_id=ai_model_id,
                prompt=prompt,
                is_active=is_active,
                periodicity_value=periodicity_value,
                periodicity_unit=periodicity_unit,
                start_time=start_time,
                end_time=end_time
            )
            messages.success(request, 'Agent created successfully!')
            return redirect('agent_list')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    models = Model.objects.all()
    return render(request, 'agents/agent_create.html', {'models': models})


@login_required
def agent_edit(request, pk):
    """Edit agent view"""
    agent = get_object_or_404(Agent, pk=pk)
    
    if request.method == 'POST':
        agent.name = request.POST.get('name')
        agent.descripcion = request.POST.get('descripcion')
        agent.ai_model_id = request.POST.get('ai_model')
        agent.prompt = request.POST.get('prompt')
        agent.is_active = request.POST.get('is_active') == 'on'
        agent.periodicity_value = request.POST.get('periodicity_value')
        agent.periodicity_unit = request.POST.get('periodicity_unit')
        agent.start_time = request.POST.get('start_time')
        agent.end_time = request.POST.get('end_time')
        agent.save()
        messages.success(request, 'Agent updated successfully!')
        return redirect('agent_list')
    
    models = Model.objects.all()
    return render(request, 'agents/agent_edit.html', {'agent': agent, 'models': models})


@login_required
def agent_delete(request, pk):
    """Delete agent view"""
    agent = get_object_or_404(Agent, pk=pk)
    agent.delete()
    messages.success(request, 'Agent deleted successfully!')
    return redirect('agent_list')


@login_required
def model_test(request, pk):
    """Test model API key"""
    model = get_object_or_404(Model, pk=pk)
    
    if model.type == 'chatgpt':
        if not model.apikey:
            return JsonResponse({
                'success': False,
                'message': 'No API key configured for this model.'
            })
        
        try:
            # Test ChatGPT API with a simple request
            headers = {
                'Authorization': f'Bearer {model.apikey}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {'role': 'user', 'content': 'Say "API key is working" in 3 words'}
                ],
                'max_tokens': 10
            }
            
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                message = result['choices'][0]['message']['content']
                return JsonResponse({
                    'success': True,
                    'message': f'✓ Connection successful! Response: {message}',
                    'model_name': model.name
                })
            elif response.status_code == 401:
                return JsonResponse({
                    'success': False,
                    'message': '✗ Invalid API key. Please check your credentials.'
                })
            elif response.status_code == 429:
                return JsonResponse({
                    'success': False,
                    'message': '✗ Rate limit exceeded. Please try again later.'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': f'✗ API error: {response.status_code} - {response.text[:100]}'
                })
                
        except requests.exceptions.Timeout:
            return JsonResponse({
                'success': False,
                'message': '✗ Request timeout. Please try again.'
            })
        except requests.exceptions.RequestException as e:
            return JsonResponse({
                'success': False,
                'message': f'✗ Connection error: {str(e)[:100]}'
            })
    
    elif model.type == 'ollama':
        # For Ollama, we'll just return a message for now
        return JsonResponse({
            'success': True,
            'message': 'ℹ Ollama models are tested locally. Make sure Ollama is running on your system.',
            'model_name': model.name
        })
    
    return JsonResponse({
        'success': False,
        'message': 'Unknown model type.'
    })
