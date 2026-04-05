import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import ChatMessage
from django.db import transaction

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time chat functionality."""
    
    async def connect(self):
        """Handle WebSocket connection."""
        try:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.user = self.scope['user']
            self.room_group_name = f'chat_{self.room_name}'
            
            logger.info(f"User {self.user.username} connecting to room {self.room_name}")
            
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        except Exception as e:
            logger.error(f"Error in connect: {str(e)}")
            await self.close()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        try:
            logger.info(f"User {self.user.username} disconnecting from {self.room_name}")
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        except Exception as e:
            logger.error(f"Error in disconnect: {str(e)}")

    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(text_data)
            message = data.get('message', '').strip()
            sender_username = self.user.username

            if not message:
                logger.warning(f"Empty message from {sender_username}")
                return
            
            # Save the message in DB with transaction
            try:
                friend = User.objects.get(username=self.room_name)
                ChatMessage.objects.create(
                    sender=self.user,
                    receiver=friend,
                    message=message
                )
                logger.debug(f"Message saved from {sender_username} to {self.room_name}")
            except User.DoesNotExist:
                logger.error(f"User {self.room_name} not found")
                return
            except Exception as e:
                logger.error(f"Error saving message: {str(e)}")
                return

            # Broadcast to group
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender_username,
                    'timestamp': self.get_timestamp()
                }
            )
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON received from {self.user.username}")
        except Exception as e:
            logger.error(f"Error in receive: {str(e)}")

    async def chat_message(self, event):
        """Send chat message to WebSocket."""
        try:
            message = event['message']
            sender = event['sender']
            timestamp = event.get('timestamp', '')

            await self.send(text_data=json.dumps({
                'message': message,
                'sender': sender,
                'timestamp': timestamp
            }))
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
    
    @staticmethod
    def get_timestamp():
        """Get current timestamp."""
        from django.utils import timezone
        return timezone.now().strftime("%H:%M %d/%m/%Y")
