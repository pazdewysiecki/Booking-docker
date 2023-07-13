 
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from core.models import PricingRule, Booking, Properties
from core.filter import PropertyFilter
from django_filters.rest_framework import DjangoFilterBackend
from core.api.serializers.general_serializers import (
    PricingRuleSerializer, BookingSerializer,BookingRetrievSerializer
)
from datetime import datetime, timedelta


class PricingRuleViewSet(viewsets.GenericViewSet):
    model = PricingRule
    serializer_class = PricingRuleSerializer


    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter()

    def get_object(self):
        return self.get_serializer().Meta.model.objects.filter(id=self.kwargs['pk'])


    def list(self, request):
        data = self.get_queryset()
        data = self.get_serializer(data, many=True)
        data = {
            "total": self.get_queryset().count(),
            "totalNotFiltered": self.get_queryset().count(),
            "rows": data.data
        }
        return Response(data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Pricing rule succesfully created!'}, status=status.HTTP_201_CREATED)
        return Response({'message':'', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        if self.get_object().exists():
            data = self.get_object().get()
            data = self.get_serializer(data)
            return Response(data.data)
        return Response({'message':'', 'error':'Pricing rule not found!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if self.get_object().exists():
            serializer = self.serializer_class(instance=self.get_object().get(), data=request.data)       
            if serializer.is_valid():       
                serializer.save()       
                return Response({'message':'Pricing rule succesfully updated!'}, status=status.HTTP_200_OK)       
        return Response({'message':'', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)    

    def destroy(self, request, pk=None):       
        if self.get_object().exists():       
            self.get_object().get().delete()       
            return Response({'message':'Pricing rule succesfully deleted!'}, status=status.HTTP_200_OK)       
        return Response({'message':'', 'error':'Pricing rule not found!'}, status=status.HTTP_400_BAD_REQUEST)



class BookingViewSet(viewsets.GenericViewSet):
    model = Booking
    serializer_class = BookingSerializer
    serializer_class_create = BookingRetrievSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter()

    def get_object(self):
        return self.get_serializer().Meta.model.objects.filter(id=self.kwargs['pk'])

    @action(detail=False, methods=['get'])
    def get_Booking(self, request):
        data = Booking.objects.filter()
        data = BookingSerializer(data, many=True)
        return Response(data.data)
    


    def list(self, request):
        data = self.get_queryset()
        #data = self.get_serializer(data, many=True)
        data = BookingRetrievSerializer(data, many=True)
        data = {
            "total": self.get_queryset().count(),
            "totalNotFiltered": self.get_queryset().count(),
            "rows": data.data
        }
        return Response(data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        #print(serializer)
        if serializer.is_valid():

            # Obtaining days 
            date_start = serializer.data['date_start']
            date_end = serializer.data['date_end']
            date_start = datetime.strptime(request.data["date_start"], '%Y-%m-%d')
            date_end = datetime.strptime(request.data["date_end"], '%Y-%m-%d')
            days = (date_end - date_start)/ timedelta(days=1) + 1 # Se suma 1 para que el ejemplo sea correcto, para que el ultimo dia sea considerado una noche 
      
            # Obtaining base_price 
            base_price= Properties.objects.filter(
                id=serializer.data['properties'], 
            ).first()
            print(base_price.base_price)

            #Obtaining pricing_rule 
            pricing_rules= PricingRule.objects.filter(
                properties=serializer.data['properties'], 
            )

            #Rule Specific days      
            fixed_price_ = 0
            count_specific_days = 0
            for pricing_rule in pricing_rules:
                try:
                        fixed_price = pricing_rule.fixed_price
                        specific_day = pricing_rule.specific_day
      
                        # Obtaining final price
                        try:
                            date_start_ = date_start.timestamp()
                            date_end_ = date_end.timestamp()
                            specific_day_ = datetime.strptime(str(specific_day), '%Y-%m-%d')
                            specific_day_ = specific_day_.timestamp()
                            #If specific day between date start and date end:
                            if specific_day_ >= date_start_ and specific_day_ <= date_end_: 

                                fixed_price_ += fixed_price
                                count_specific_days += 1
                        except Exception as e:
                            print(e)
                            pass

                            
                except Exception as e:
                    print(e)
                    pass
                
            #Final price with Rule specific price
            final_price__ = fixed_price_

            price_modifier_ = None
            #Rule min_stay_length
            for pricing_rule in pricing_rules:
                try:
                    price_modifier = pricing_rule.price_modifier
                    min_stay_length =pricing_rule.min_stay_length
                    if days >= min_stay_length:
                        price_modifier_ = price_modifier

                except Exception as e:
                    print(e)
                    pass


            # Calculate final_price
            if price_modifier_ == None:                 
                price_modifier_ = 1

            if fixed_price_ == None:   
                fixed_price_ = 0
            if count_specific_days == None:
                count_specific_days = 0
              
            
            final_price = final_price__ + base_price.base_price * (days- count_specific_days) * price_modifier_ 
            #print(f"final_price__ ´{final_price__} + base_price.base_price {base_price.base_price} * (days {days}- count_specific_days{count_specific_days}) * price_modifier_ {price_modifier_}")


            booking= Booking.objects.create(
            properties_id=serializer.data['properties'],
            date_start=serializer.data['date_start'],
            date_end=serializer.data['date_end'],
            final_price=(final_price)
            )
            
            return Response({'message':'Booking succesfully created!', 'final_price':final_price}, status=status.HTTP_201_CREATED)
        return Response({'message':'', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        if self.get_object().exists():
            data = self.get_object().get()
            data = self.get_serializer(data)
            #data = BookingRetrievSerializer(data)
            return Response(data.data)
        return Response({'message':'', 'error':'Booking not found!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if self.get_object().exists():
            serializer = self.serializer_class(instance=self.get_object().get(), data=request.data)       
            if serializer.is_valid():  

                # Obtaining days 
                date_start = serializer.data['date_start']
                date_end = serializer.data['date_end']
                date_start = datetime.strptime(request.data["date_start"], '%Y-%m-%d')
                date_end = datetime.strptime(request.data["date_end"], '%Y-%m-%d')
                days = (date_end - date_start)/ timedelta(days=1) + 1 # Se suma 1 para que el ejemplo sea correcto, para que el ultimo dia sea considerado una noche 
        
                # Obtaining base_price 
                base_price= Properties.objects.filter(
                    id=serializer.data['properties'], 
                ).first()
                print(base_price.base_price)

                #Obtaining pricing_rule 
                pricing_rules= PricingRule.objects.filter(
                    properties=serializer.data['properties'], 
                )

                #Rule Specific days      
                fixed_price_ = 0
                count_specific_days = 0
                for pricing_rule in pricing_rules:
                    try:
                            fixed_price = pricing_rule.fixed_price
                            specific_day = pricing_rule.specific_day
        
                            # Obtaining final price
                            try:
                                date_start_ = date_start.timestamp()
                                date_end_ = date_end.timestamp()
                                specific_day_ = datetime.strptime(str(specific_day), '%Y-%m-%d')
                                specific_day_ = specific_day_.timestamp()
                                #If specific day between date start and date end:
                                if specific_day_ >= date_start_ and specific_day_ <= date_end_: 

                                    fixed_price_ += fixed_price
                                    count_specific_days += 1
                            except Exception as e:
                                print(e)
                                pass

                                
                    except Exception as e:
                        print(e)
                        pass
                    
                #Final price with Rule specific price
                final_price__ = fixed_price_

                price_modifier_ = None
                #Rule min_stay_length
                for pricing_rule in pricing_rules:
                    try:
                        price_modifier = pricing_rule.price_modifier
                        min_stay_length =pricing_rule.min_stay_length
                        if days >= min_stay_length:
                            price_modifier_ = price_modifier

                    except Exception as e:
                        print(e)
                        pass


                # Calculate final_price
                if price_modifier_ == None:                 
                    price_modifier_ = 1

                if fixed_price_ == None:   
                    fixed_price_ = 0
                if count_specific_days == None:
                    count_specific_days = 0
                
                
                final_price = final_price__ + base_price.base_price * (days- count_specific_days) * price_modifier_ 
                #print(f"final_price__ ´{final_price__} + base_price.base_price {base_price.base_price} * (days {days}- count_specific_days{count_specific_days}) * price_modifier_ {price_modifier_}")

                print(serializer.data['id'])
                booking= Booking.objects.filter(id=serializer.data['id']).update(
                properties_id=request.data['properties'],
                date_start=request.data['date_start'],
                date_end=request.data['date_end'],
                final_price=(final_price)
                )
                print(request.data)


              
                return Response({'message':'Booking succesfully updated!'}, status=status.HTTP_200_OK)       
        return Response({'message':'', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)    

    def destroy(self, request, pk=None):       
        if self.get_object().exists():       
            self.get_object().get().delete()       
            return Response({'message':'Booking succesfully deleted!'}, status=status.HTTP_200_OK)       
        return Response({'message':'', 'error':'Booking not found!'}, status=status.HTTP_400_BAD_REQUEST)




























