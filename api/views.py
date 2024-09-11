
from rest_framework.views import APIView
from rest_framework.response import Response
from google.cloud import vision
from transactions.models import Transactions
from .serializer import TransactionsSerializer, NotificationsSerializer
from rest_framework import status
import re
from datetime import datetime
from notifications.models import Notifications


class TransactionsListView(APIView):
  def get(self, request):
        transactions = Transactions.objects.all()
        serializer = TransactionsSerializer(transactions, many=True)
        return Response(serializer.data)
  def post(self,request):
    if 'file' not in request.FILES:
        return Response({"error": "No file provided"}, status=400)
    image_file = request.FILES['file']
    client = vision.ImageAnnotatorClient()
    try:
        image_content = image_file.read()
    except Exception as e:
        return Response({"error": f"Failed to read file: {str(e)}"}, status=500)
    
    image = vision.Image(content=image_content)
    try:
        response = client.text_detection(image=image)
        texts = response.text_annotations
        extracted_text = texts[0].description if texts else ""
    except Exception as e:
        return Response({"error": f"Failed to process image: {str(e)}"}, status=500)
    
    print(f"Extracted Text: {extracted_text}")
    patterns = {
        'amount': [r'KES ([\d,]+\.\d{2})', r'Ksh([\d,.]+)sent to'],
        'date': [r'(\d{2}/\d{2}/\d{4})', r'on (\d{1,2}/\d{1,2}/\d{2})'],
        'code': [r'([A-Z0-9]{10})', r'([A-Z0-9]{10})']
    }
    matches = {}
    for key, regex_list in patterns.items():
        for pattern in regex_list:
            match = re.search(pattern, extracted_text)
            if match:
                matches[key] = match.group(1) if key == 'amount' else match.group(0)
                break
    if all(k in matches for k in ['amount', 'date', 'code']):
        amount = float(matches['amount'].replace(',', ''))
        date = matches['date']
        try:
            date_obj = datetime.strptime(date, '%d/%m/%Y')
            date = date_obj.strftime('%Y-%m-%d')
        except ValueError:
            return Response({"error": "Date format is incorrect"}, status=400)
        unique_code = matches['code']
        try:
            transaction = Transactions.objects.create(
                unique_code=unique_code,
                amount=amount,
                date=date
            )
        except Exception as e:
            return Response({"error": f"Failed to save transaction: {str(e)}"}, status=500)
        return Response({"message": "Transaction saved successfully"}, status=201)
    else:
        return Response({"error": "Could not extract all required information"}, status=400)

class TransactionsSearchView(APIView):
    def get(self, request):
        amount = request.GET.get('amount', None)
        date = request.GET.get('date', None)
        transactions = Transactions.objects.all()
        if amount:
            transactions = transactions.filter(amount=amount)
        if date:
            transactions = transactions.filter(date=date)
        serializer = TransactionsSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TransactionsDetailView(APIView):
    def get(self,request,id):
            transactionss = Transactions.objects.get(id=id)
            serializer = TransactionsSerializer(transactionss)
            return Response(serializer.data)
    def delete(self,request,id):
            transactions =Transactions.objects.get(id=id)
            transactions.delete()
            return Response(status=status.HTTP_202_ACCEPTED)

class DashboardListView(APIView):
  def get(self, request):
        transactions = Transactions.objects.all()
        serializer = TransactionsSerializer(transactions, many=True)
        return Response(serializer.data)

class NotificationsListView(APIView):
    def get(self, request):
        notifications = Notifications.objects.all()
        serializer = NotificationsSerializer(notifications, many=True)
        return Response(serializer.data)
   
    def post(self, request):
        custom_message = "John is interested"#f"Buyer {interest.buyer.username} is interested in your land {interest.land.name}."
        data = request.data.copy()  
        data['message'] = custom_message 
        serializer = NotificationsSerializer(data=data)
        if serializer.is_valid():
            notifications = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


     
        