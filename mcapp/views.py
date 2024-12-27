from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import RegisteredUser, Airdrops
from .serializers import RegisteredUserSerializer, AirdropSerializer
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny
from .models import BlogPost
from .serializers import BlogPostSerializer
# Register user email

class RegisterEmailView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        serializer = RegisteredUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Email registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Add a new airdrop
class AirdropCreateView(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        serializer = AirdropSerializer(data=request.data)
        if serializer.is_valid():
            airdrop = serializer.save()
            self.notify_users(airdrop)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def notify_users(self, airdrop):
        users = RegisteredUser.objects.all()
        recipient_list = [user.email for user in users]
        if recipient_list:
            send_mail(
                subject=f"New Airdrop: {airdrop.name}",
                message=f"""
                A new airdrop is available!
                
                Name: {airdrop.name}
                Description: {airdrop.description}
                Link: {airdrop.link}
                Reward Date: {airdrop.reward_date}

                Don't miss out on this opportunity!
                """,
                from_email="abelbk06@gmail.com",
                recipient_list=recipient_list,
                fail_silently=False,
            )


# List all airdrops
class AirdropListView(APIView):
    permission_classes = [AllowAny] 
    def get(self, request):
        airdrops = Airdrops.objects.all()
        serializer = AirdropSerializer(airdrops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AirdropDetailView(generics.RetrieveAPIView):
    queryset = Airdrops.objects.all()
    serializer_class = AirdropSerializer
class BlogPostList(generics.ListAPIView):
    queryset = BlogPost.objects.all().order_by('-date')
    serializer_class = BlogPostSerializer

class BlogPostDetail(generics.RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
# Define the feedback endpoint
@csrf_exempt
def feedback(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            name = data.get('name', '')
            email = data.get('email', '')
            message = data.get('message', '')

            # Validate the required fields
            if not name or not email or not message:
                return JsonResponse({"error": "All fields are required."}, status=400)

            # Construct the email content
            subject = f"Feedback from {name}"
            body = f"You have received new feedback.\n\nName: {name}\nEmail: {email}\n\nMessage:\n{message}"

            # Send the email
            send_mail(
                subject,
                body,
                'abelbk06@gmail.com',  # Sender email (replace with your own domain or email)
                ['abelbk06@gmail.com'],     # Admin email to receive feedback
                fail_silently=False,
            )

            # Return a success response
            return JsonResponse({"message": "Feedback sent successfully."})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)