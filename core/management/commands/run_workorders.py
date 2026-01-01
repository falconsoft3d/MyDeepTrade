import time
import requests
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import WorkOrder, Agent


class Command(BaseCommand):
    help = 'Runs work orders based on their schedule and agent periodicity'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Work Order Scheduler started...'))
        
        # Keep track of last execution times
        last_execution = {}
        
        while True:
            try:
                current_time = timezone.now()
                current_hour_minute = current_time.time()
                
                # Get all work orders that are not completed
                workorders = WorkOrder.objects.filter(status__in=['draft', 'working']).select_related('agent', 'agent__ai_model')
                
                for workorder in workorders:
                    agent = workorder.agent
                    
                    # Check if current time is within work order schedule
                    if not (workorder.start_time <= current_hour_minute <= workorder.end_time):
                        continue
                    
                    # Check if current time is within agent schedule
                    if not (agent.start_time <= current_hour_minute <= agent.end_time):
                        continue
                    
                    # Check if agent is active
                    if not agent.is_active:
                        continue
                    
                    # Check periodicity
                    wo_key = f"wo_{workorder.id}"
                    if wo_key in last_execution:
                        last_exec_time = last_execution[wo_key]
                        
                        # Calculate time difference based on periodicity unit
                        if agent.periodicity_unit == 'minutes':
                            time_diff = timedelta(minutes=agent.periodicity_value)
                        elif agent.periodicity_unit == 'hours':
                            time_diff = timedelta(hours=agent.periodicity_value)
                        else:  # days
                            time_diff = timedelta(days=agent.periodicity_value)
                        
                        # Skip if not enough time has passed
                        if current_time - last_exec_time < time_diff:
                            continue
                    
                    # Execute work order
                    self.stdout.write(f'Executing work order {workorder.sequence}...')
                    
                    # Update status to working
                    if workorder.status == 'draft':
                        workorder.status = 'working'
                        workorder.save()
                    
                    # Execute the work order based on AI model
                    result = self.execute_workorder(workorder)
                    
                    if result:
                        self.stdout.write(self.style.SUCCESS(
                            f'Work order {workorder.sequence} executed successfully'
                        ))
                        last_execution[wo_key] = current_time
                    else:
                        self.stdout.write(self.style.ERROR(
                            f'Work order {workorder.sequence} execution failed'
                        ))
                
                # Sleep for 30 seconds before next check
                time.sleep(30)
                
            except KeyboardInterrupt:
                self.stdout.write(self.style.WARNING('Shutting down scheduler...'))
                break
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
                time.sleep(30)
    
    def execute_workorder(self, workorder):
        """Execute a work order based on its agent's AI model"""
        try:
            agent = workorder.agent
            ai_model = agent.ai_model
            
            # Log the execution
            self.stdout.write(f'  Agent: {agent.name}')
            self.stdout.write(f'  Model: {ai_model.name} ({ai_model.get_type_display()})')
            self.stdout.write(f'  Prompt: {workorder.prompt[:100]}...')
            
            # Execute based on model type
            if ai_model.type == 'chatgpt' and ai_model.apikey:
                return self.execute_chatgpt(workorder, ai_model)
            elif ai_model.type == 'ollama':
                return self.execute_ollama(workorder, ai_model)
            else:
                self.stdout.write(self.style.WARNING(
                    f'  Model type {ai_model.type} not configured or missing API key'
                ))
                return False
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  Execution error: {str(e)}'))
            return False
    
    def execute_chatgpt(self, workorder, ai_model):
        """Execute work order using ChatGPT API"""
        try:
            headers = {
                'Authorization': f'Bearer {ai_model.apikey}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {
                        'role': 'system',
                        'content': workorder.agent.prompt
                    },
                    {
                        'role': 'user',
                        'content': workorder.prompt
                    }
                ],
                'max_tokens': 500,
                'temperature': 0.7
            }
            
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                message = result['choices'][0]['message']['content']
                self.stdout.write(self.style.SUCCESS(f'  Response: {message[:100]}...'))
                return True
            else:
                self.stdout.write(self.style.ERROR(
                    f'  API Error: {response.status_code} - {response.text}'
                ))
                return False
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ChatGPT error: {str(e)}'))
            return False
    
    def execute_ollama(self, workorder, ai_model):
        """Execute work order using Ollama (local model)"""
        try:
            # Ollama typically runs on localhost:11434
            data = {
                'model': 'llama2',  # Default model, can be configured
                'prompt': f"{workorder.agent.prompt}\n\n{workorder.prompt}",
                'stream': False
            }
            
            response = requests.post(
                'http://localhost:11434/api/generate',
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                message = result.get('response', '')
                self.stdout.write(self.style.SUCCESS(f'  Response: {message[:100]}...'))
                return True
            else:
                self.stdout.write(self.style.ERROR(
                    f'  Ollama Error: {response.status_code}'
                ))
                return False
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  Ollama error: {str(e)}'))
            return False
