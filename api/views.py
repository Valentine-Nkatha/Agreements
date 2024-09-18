# transactions/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from google.cloud import vision
from transactions.models import Transactions
from agreements.models import Agreements
from rest_framework import status
from .serializer import TransactionsSerializer, AgreementsSerializer, BlockchainValidationSerializer
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.utils import timezone
import re
from datetime import datetime
from django.http import JsonResponse
from transactions.blockchain import Blockchain

class TransactionsListView(APIView):

    def post(self, request):
        if 'file1' not in request.FILES or 'file2' not in request.FILES:
            return Response({"error": "Both files (file1 and file2) must be provided"}, status=400)

        image_file1 = request.FILES['file1']
        image_file2 = request.FILES['file2']
        client = vision.ImageAnnotatorClient()

        def extract_data_from_image(image_file):
            try:
                image_content = image_file.read()
                image = vision.Image(content=image_content)
                response = client.text_detection(image=image)
                texts = response.text_annotations
                extracted_text = texts[0].description if texts else ""
            except Exception as e:
                raise ValueError(f"Failed to process image: {str(e)}")
            patterns = {
                'amount': [r'Ksh\s*([\d,]+\.\d{2})', r'KES\s*([\d,]+\.\d{2})'],
                'date': [r'on\s*(\d{1,2}/\d{1,2}/\d{2})', r'(\d{1,2}/\d{1,2}/\d{4})'],
                'code': [r'\b([A-Z0-9]{10})\b']
            }
            matches = {}
            for key, regex_list in patterns.items():
                for pattern in regex_list:
                    match = re.search(pattern, extracted_text)
                    if match:
                        matches[key] = match.group(1)
                        break
            return matches

        try:
            data1 = extract_data_from_image(image_file1)
            data2 = extract_data_from_image(image_file2)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
        if all(k in data1 and k in data2 for k in ['amount', 'date', 'code']):
            try:
                amount1 = float(data1['amount'].replace(',', ''))
                amount2 = float(data2['amount'].replace(',', ''))
            except ValueError:
                return Response({"error": "Invalid amount format in one of the images"}, status=400)

            date1, date2 = data1['date'], data2['date']
            date_formats = ['%d/%m/%y', '%d/%m/%Y']
            date_obj1 = date_obj2 = None

            for fmt in date_formats:
                try:
                    date_obj1 = datetime.strptime(date1, fmt)
                    date_obj2 = datetime.strptime(date2, fmt)
                    break
                except ValueError:
                    continue

            if date_obj1 is None or date_obj2 is None:
                return Response({"error": "Date format is incorrect"}, status=400)

            formatted_date1 = date_obj1.strftime('%Y-%m-%d')
            formatted_date2 = date_obj2.strftime('%Y-%m-%d')

            if (amount1 == amount2 and
                formatted_date1 == formatted_date2 and
                data1['code'] == data2['code']):
                
                agreement_id = request.data.get('agreement_id')
                agreement = get_object_or_404(Agreements, id=agreement_id)

                try:
                    transaction, created = Transactions.objects.update_or_create(
                        unique_code=data1['code'],  
                        defaults={
                            'amount': amount1,  
                            'date': timezone.now(),
                            'status': 'complete'
                        }
                    )
                    agreement.update_on_transaction(amount1)

                    message = "Transaction created and marked as complete" if created else "Transaction updated and marked as complete"
                except Exception as e:
                    return Response({"error": f"Failed to save transaction: {str(e)}"}, status=500)

                return Response({"message": message, "amount": amount1}, status=201)
            else:
                return Response({
                    "error": "The amounts, dates, or unique codes do not match",
                    "amount1": amount1,
                    "amount2": amount2,
                    "date1": formatted_date1,
                    "date2": formatted_date2,
                    "code1": data1['code'],
                    "code2": data2['code']
                }, status=400)
        else:
            return Response({"error": "Could not extract all required information from both images"}, status=400)
    

class AgreementsView(APIView):
    def get(self, request):
        agreements = Agreements.objects.all()
        serializer = AgreementsSerializer(agreements, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            agreement = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AgreementDetailView(APIView):
    def get_object(self, request, id):
        agreements = Agreements.objects.get(id=id)
        serializer = AgreementsSerializer(agreements)
        return Response(serializer.data)

class CheckBlockchainView(APIView):
    def get(self, request):
        blockchain = Blockchain() 
        validation_result = blockchain.is_valid()

        serializer = BlockchainValidationSerializer(data={'validation_result': validation_result})
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
