from django.db import transaction
from django.utils import timezone
from django.contrib.auth import authenticate
from courier_app.filters import ProductFilter, OrderFilter
from courier_app.courier_serializer import *
from courier_app.models import Product
from utils.reusable_methods import get_first_error_message, generate_six_length_random_number
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg, F
from utils.helper import create_response, paginate_data
from utils.response_messages import *
# from vehicle.serializer import serializer

from courier_site.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from datetime import date, timedelta



class ProductController:
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

 
    def create(self, request):
        try:
            request.POST._mutable = True
            request.data["created_by"] = request.user.guid
            request.POST._mutable = False

            if request.user.role in ['admin', 'manager'] or request.user.is_superuser:  # roles
                validated_data = ProductSerializer(data=request.data)
                if validated_data.is_valid():
                    response = validated_data.save()
                    response_data = ProductSerializer(response).data
                    return Response({'data': response_data}, 200)
                else:
                    error_message = get_first_error_message(validated_data.errors, "UNSUCCESSFUL")
                    return Response({'data': error_message}, 400)
            else:
                return Response({'data': "Permission Denaied"}, 400)
        except Exception as e:
            return Response({'error': str(e)}, 500)

    # mydata = Member.objects.filter(firstname__endswith='s').values()
    def get_product(self, request):
        try:

            instances = self.serializer_class.Meta.model.objects.all()

            filtered_data = self.filterset_class(request.GET, queryset=instances)
            data = filtered_data.qs

            paginated_data, count = paginate_data(data, request)

            serialized_data = self.serializer_class(paginated_data, many=True).data
            response_data = {
                "count": count,
                "data": serialized_data,
            }
            return create_response(response_data, "SUCCESSFUL", 200)


        except Exception as e:
            return Response({'error': str(e)}, 500)

    def update_product(self, request):
        try:
            if "id" in request.data:
                # finding instance
                instance = Product.objects.filter(id=request.data["id"]).first()

                if instance:
                    request.POST._mutable = True
                    request.data["updated_by"] = request.user.guid
                    request.POST._mutable = False

                    # updating the instance/record
                    serialized_data = ProductSerializer(instance, data=request.data, partial=True)
                    if request.user.role in ['admin', 'manager'] or request.user.is_superuser:  # roles
                        if serialized_data.is_valid():
                            response = serialized_data.save()
                            response_data = ProductSerializer(response).data
                            return Response({"data": response_data}, 200)
                        else:
                            error_message = get_first_error_message(serialized_data.errors, "UNSUCCESSFUL")
                            return Response({'data': error_message}, 400)
                    else:
                        return Response({'data': "Permission Denaied"}, 400)
                else:
                    return Response({"data": "NOT FOUND"}, 404)
            else:
                return Response({"data": "ID NOT PROVIDED"}, 400)

        except Exception as e:
            return Response({'error': str(e)}, 500)

    def delete_product(self, request):
        try:
            if "id" in request.query_params:
                instance = Product.objects.filter(id=request.query_params['id']).first()

                if instance:
                    instance.delete()
                    return Response({"data": "SUCESSFULL"}, 200)
                else:
                    return Response({"data": "RECORD NOT FOUND"}, 404)
            else:
                return Response({"data": "ID NOT PROVIDED"}, 400)
        except Exception as e:
            return Response({'error': str(e)}, 500)


class OrderController:
    serializer_class = OrderSerializer
    order_detail_serializer = OrderDetailSerializer
    filterset_class = OrderFilter

    def create(self, request):
        try:
            request.POST._mutable = True
            order_details = request.data.pop('OrderDetail') if 'OrderDetail' in request.data else None
            request.data['customer'] = request.user.guid
            today = date.today()
            if today.weekday() in [3,4]:
                delivery_days = timedelta(4)
            elif today.weekday() == 5:
                delivery_days = timedelta(3)
            else:
                delivery_days = timedelta(2)
            request.data['delivery_date'] = today + delivery_days
            request.data['status'] = 'booked'
            request.POST._mutable = False

            if request.user.role in ['admin', 'manager'] or request.user.is_superuser:  # roles
                serialized_data = self.serializer_class(data=request.data)
                if serialized_data.is_valid():
                    with transaction.atomic():
                        response_data = serialized_data.save()
                        bill = 0
                        if order_details:
                            for i in order_details:
                                i['order'] = response_data.id
                                i['total_price'] = i['quantity'] * i['unit_price']
                                bill += i['total_price']
                                serialized_detail = self.order_detail_serializer(data=i)
                                if serialized_detail.is_valid():
                                    serialized_detail.save()
                                else:
                                    transaction.set_rollback(True)
                                    return create_response({}, get_first_error_message(serialized_detail.errors, UNSUCCESSFUL),400)
                            response_data.bill = bill
                            response_data.save()
            
                    return create_response(self.serializer_class(response_data).data, SUCCESSFUL, 200)
                else:
                    return create_response({}, get_first_error_message(serialized_data.errors,UNSUCCESSFUL), 400)
            else:
                return Response({'data': "Permission Denaied"}, 400)
        except Exception as e:
            return create_response({'error':str(e)}, UNSUCCESSFUL, 500)
        
    def get_order(self, request):
        try:
            instances = self.serializer_class.Meta.model.objects.all()
            filtered_data = self.filterset_class(request.GET, queryset=instances)
            data = filtered_data.qs
            paginated_data, count = paginate_data(data, request)
            serialized_data = self.serializer_class(paginated_data, many=True).data
            response_data = {
                "count": count,
                "data": serialized_data,
            }
            return create_response(response_data, "SUCCESSFUL", 200)

        except Exception as e:
            return Response({'error': str(e)}, 500)

    def update_order(self, request):
        try:
            if 'id' in request.data:
                instance = Order.objects.filter(id=request.data['id']).first()

                if instance:
                    request.POST._mutable = True
                    order_details = request.data.pop('OrderDetail') if "OrderDetail" in request.data else None
                    delete_order_details = request.data.pop('DeleteOrderDetail') if 'DeleteOrderDetail' in request.data else None
                    request.POST._mutable = False

                    serialized_data = self.serializer_class(instance, data=request.data, partial=True)
                    if serialized_data.is_valid():
                        response_data = serialized_data.save()
                        bill = 0

# if order_details === if order_details is not None
                        if order_details:
                            for i in order_details:
                                i['order'] = response_data.id
                                i['total_price'] = i['quantity'] * i['unit_price']
                                bill += i['total_price']
                                serialized_detail = self.order_detail_serializer(data=i)
                                if serialized_detail.is_valid():
                                    serialized_detail.save()
                                else:
                                    transaction.set_rollback(True)
                                    return create_response({}, get_first_error_message(serialized_detail.errors, UNSUCCESSFUL),400)
                            response_data.bill = bill
                            response_data.save()

                        if delete_order_details:
                            od = instance.order_detail_order.filter(id__in=delete_order_details)
                            # od = OrderDetails.objects.filter(id__in=delete_order_details)
                            if od:
                                od.delete()
                        return create_response(self.serializer_class(response_data).data, SUCCESSFUL, 200)
                    else:
                        return create_response({}, get_first_error_message(serialized_data.errors, UNSUCCESSFUL), 400)
                else:
                    return create_response({}, NOT_FOUND, 404)
            else:
                return create_response({}, ID_NOT_PROVIDED, 400)
        except Exception as e:
            return create_response({'error':str(e)}, UNSUCCESSFUL, 500)

    def delete_order(self, request):
        try:
            if "id" in request.query_params:
                instance = Order.objects.filter(id=request.query_params['id']).first()
                if instance:
                    instance.delete()
                    return Response({"data": "SUCESSFULL"}, 200)
                else:
                    return Response({"data": "RECORD NOT FOUND"}, 404)
            else:
                return Response({"data": "ID NOT PROVIDED"}, 400)

        except Exception as e:
            return Response({'error': str(e)}, 500)


