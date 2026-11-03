import logging
from logs.utils import get_details_from_request
from django.db import transaction
from django.db.models import QuerySet , Prefetch

from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework import serializers
from rest_framework.permissions import AllowAny , IsAuthenticated

from common.pagination import CustomPagination

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.models import User
from initialborders.models.models import InitialBorder
from initialborders.models.amar import (
    AmarKarKhaneh,
    AmarEstekhraj,
    HSEPASMAND,
    HSEHADESE,
    AmarEkteshaf,
    AmarAmalkardTajhizCoal,
    AmarAmalkardBahrebardariCoal
)

delete_logger = logging.getLogger('delete_activity_logger')
api_activity_logger = logging.getLogger('api_activity_logger')

class AmarKarKhanehListApiView(APIView):
    """
        list of all AmarKarKhaneh instances for ONE Initialborder
    """

    class AmarKarKhanehInPutSerializer(serializers.ModelSerializer):
        doure = serializers.IntegerField(
            min_value=1,
            max_value=12,
            error_messages={
                'min_value': 'دوره نمی‌تواند کمتر از 1 باشد.',
                'max_value': 'دوره نمی‌تواند بیشتر از 12 باشد.',
            }
        )
        class Meta:
            model = AmarKarKhaneh
            fields = [
                'sal', 'doure', 'name_mahsoul', 'zarfiyat_amaliyati',
                'zarfiyat_amaliyati' , 'mahsoul_kham_daryafti', 'mizain_toulid' , 'hazine_toulid',
                'masraf_ab', 'masraf_bargh', 'masraf_soukht',
                'masraf_gaz', 'masraf_mavad'
            ]
            # validators = [
            #     serializers.UniqueTogetherValidator(
            #         queryset=AmarKarKhaneh.objects.all(),
            #         fields=['initialborder','sal', 'doure', 'name_mahsoul'],
            #         message='ترکیب سال، دوره و نام محصول قبلاً ثبت شده است.'
            #     )
            # ]
    
        def validate(self, attrs):            
            # Get initialborder from context (you'll pass it from the view)
            initialborder = self.context.get('initialborder')
            if initialborder and initialborder.dtyp:
                if initialborder.dtyp.code not in AmarKarKhaneh.ALLOWED_INITBORDER_CODES:
                    raise serializers.ValidationError({
                        'initialborder': f'فقط محدوده اولیه با کدهای {AmarKarKhaneh.ALLOWED_INITBORDER_CODES} مجاز هستند.'
                    })
                
            sal = attrs.get('sal')
            doure = attrs.get('doure')
            name_mahsoul = attrs.get('name_mahsoul')
            
            if initialborder and AmarKarKhaneh.objects.filter(
                initialborder=initialborder,
                sal=sal,
                doure=doure,
                name_mahsoul=name_mahsoul
            ).exists():
                raise serializers.ValidationError(
                    'ترکیب سال و دوره و نام محصول برای این محدوده قبلاً ثبت شده است.'
                )
            
            return attrs

    class AmarKarKhanehOutPutSerializer(serializers.ModelSerializer):
        class AmarKarKhanehOutPutSerializerInitialborder(serializers.ModelSerializer):
            class Meta:
                model = InitialBorder
                fields = ['id','title']

        initialborder = AmarKarKhanehOutPutSerializerInitialborder()        
        
        class Meta:
            model = AmarKarKhaneh
            fields = [
                'id', 'initialborder', 'sal', 'doure', 'name_mahsoul',
                'zarfiyat_amaliyati' , 'mahsoul_kham_daryafti', 'mizain_toulid' , 'hazine_toulid',
                'masraf_ab', 'masraf_bargh','masraf_soukht', 'masraf_gaz', 'masraf_mavad',
            ]

    def get(self , request:Request , initialborderid:int):
        try:
            user : User = request.user
            
            initialborder_instance : InitialBorder = InitialBorder.objects.get(pk = initialborderid)

            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                api_activity_logger.warning(f"تلاش  غیرمجاز برای گرفتن لیست آمارکارخانه محدوده اولیه {initialborder_instance.title}" , extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)

            all_amarkarkhaneh_of_this_initborder = AmarKarKhaneh.objects.filter(initialborder = initialborder_instance)
            
            if not all_amarkarkhaneh_of_this_initborder.exists():
                return Response({"detail": "امار کارخانه‌ایی برای این محدوده اولیه وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.AmarKarKhanehOutPutSerializer(all_amarkarkhaneh_of_this_initborder, many=True)
            api_activity_logger.info("خواندن لیست آمار کارخانه" , extra=get_details_from_request(request))
            return Response(serializer.data, status=status.HTTP_200_OK)

        except InitialBorder.DoesNotExist as e:
            api_activity_logger.error(f"محدوده اولیه با این شناسه یافت نشد {str(e)}" , extra=get_details_from_request(request))
            return Response({"detail": "محدوده اولیه با این شناسه یافت نشد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن لیست آمار کارخانه محدوده {str(e)}" , extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن لیست آمار کارخانه محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self , request:Request , initialborderid:int):
        try:
            user : User = request.user
            initialborder_instance : InitialBorder = InitialBorder.objects.get(pk = initialborderid)

            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                api_activity_logger.warning(f"تلاش  غیرمجاز برای ساخت آمارکارخانه محدوده اولیه {initialborder_instance.title}" , extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)

            
            serializer = self.AmarKarKhanehInPutSerializer(
                data=request.data,
                context={'initialborder': initialborder_instance}
            )
            if not serializer.is_valid():
                return Response({"detail": serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data

            amarkarkhaneh_new_instance = AmarKarKhaneh.objects.create(
                initialborder=initialborder_instance,
                **validated_data
            )

            output_serializer = self.AmarKarKhanehOutPutSerializer(amarkarkhaneh_new_instance)
            api_activity_logger.info(f"ساخت آمار کارخانه جدید برای محدوده {initialborder_instance.title}", extra=get_details_from_request(request))
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except InitialBorder.DoesNotExist as e:
            api_activity_logger.error(f"محدوده اولیه با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "محدوده اولیه با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در ساخت آمار کارخانه محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در ساخت آمار کارخانه محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AmarKarKhanehDetailsApiView(APIView):
    """
        Details of One AmarKarkhaneh Instance
    """

    class AmarKarKhanehDetailsInputSerializer(serializers.ModelSerializer):
        doure = serializers.IntegerField(
            min_value=1,
            max_value=12,
            error_messages={
                'min_value': 'دوره نمی‌تواند کمتر از 1 باشد.',
                'max_value': 'دوره نمی‌تواند بیشتر از 12 باشد.',
            }
        )
        class Meta:
            model = AmarKarKhaneh
            fields = [
                'sal', 'doure', 'name_mahsoul',
                'zarfiyat_amaliyati' , 'mahsoul_kham_daryafti', 'mizain_toulid' , 'hazine_toulid',
                'masraf_ab', 'masraf_bargh', 'masraf_soukht','masraf_gaz', 'masraf_mavad'
            ]
            # validators = [
            #     serializers.UniqueTogetherValidator(
            #         queryset=AmarKarKhaneh.objects.all(),
            #         fields=['initialborder','sal', 'doure', 'name_mahsoul'],
            #         message='ترکیب سال، دوره و نام محصول قبلاً ثبت شده است.'
            #     )
            # ]

        
        def validate(self, attrs):
            initialborder = self.context.get('initialborder')
            
            if initialborder and initialborder.dtyp:
                if initialborder.dtyp.code not in AmarKarKhaneh.ALLOWED_INITBORDER_CODES:
                    raise serializers.ValidationError({
                        'initialborder': f'فقط محدوده اولیه با کدهای {AmarKarKhaneh.ALLOWED_INITBORDER_CODES} مجاز هستند.'
                    })
                
            sal = attrs.get('sal')
            doure = attrs.get('doure')
            name_mahsoul = attrs.get('name_mahsoul')
            
            # Build the filter query
            queryset = AmarKarKhaneh.objects.filter(
                initialborder=initialborder,
                sal=sal,
                doure=doure,
                name_mahsoul=name_mahsoul
            )

            # If updating (instance exists), exclude the current instance
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            if initialborder and queryset.exists():
                raise serializers.ValidationError(
                    'ترکیب سال و دوره و نام محصول برای این محدوده قبلاً ثبت شده است.'
                )
            
            return attrs

    class AmarKarKhanehDetailsOuputSerializer(serializers.ModelSerializer):
        class AmarKarKhanehDetailsOuputSerializerInitialborder(serializers.ModelSerializer):
            class Meta:
                model = InitialBorder
                fields = ['id','title']

        initialborder = AmarKarKhanehDetailsOuputSerializerInitialborder()        
        
        class Meta:
            model = AmarKarKhaneh
            fields = [
                'id', 'initialborder', 'sal', 'doure', 'name_mahsoul',
                'zarfiyat_amaliyati' , 'mahsoul_kham_daryafti', 'mizain_toulid' , 'hazine_toulid',                
                'masraf_ab', 'masraf_bargh','masraf_soukht', 'masraf_gaz', 'masraf_mavad',
            ]

    def get(self, request: Request, amarkarkhanehid: int):
        try:
            user: User = request.user
            amarkarkhaneh_instance: AmarKarKhaneh = AmarKarKhaneh.objects.get(pk=amarkarkhanehid)
            related_initborder: InitialBorder = amarkarkhaneh_instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای گرفتن آمارکارخانه محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.AmarKarKhanehDetailsOuputSerializer(amarkarkhaneh_instance)
            api_activity_logger.info(f"خواندن جزئیات آمار کارخانه {amarkarkhaneh_instance.id}", extra=get_details_from_request(request))
            return Response(serializer.data, status=status.HTTP_200_OK)

        except AmarKarKhaneh.DoesNotExist:
            api_activity_logger.error(f"آمارکارخانه با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمارکارخانه با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن آمار کارخانه محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن آمار کارخانه محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request: Request, amarkarkhanehid: int):
        try:
            user: User = request.user
            amarkarkhaneh_instance: AmarKarKhaneh = AmarKarKhaneh.objects.get(pk=amarkarkhanehid)
            related_initborder: InitialBorder = amarkarkhaneh_instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای ویرایش آمارکارخانه محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.AmarKarKhanehDetailsInputSerializer(
                amarkarkhaneh_instance,
                data=request.data,
                context={'initialborder': related_initborder}
            )
            if not serializer.is_valid():
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            output_serializer = self.AmarKarKhanehDetailsOuputSerializer(amarkarkhaneh_instance)
            api_activity_logger.info(f"ویرایش آمار کارخانه {amarkarkhaneh_instance.id}", extra=get_details_from_request(request))
            return Response(output_serializer.data, status=status.HTTP_200_OK)

        except AmarKarKhaneh.DoesNotExist:
            api_activity_logger.error(f"آمارکارخانه با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمارکارخانه با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در ویرایش آمار کارخانه محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در ویرایش آمار کارخانه محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request: Request, amarkarkhanehid: int):
        try:
            user: User = request.user
            amarkarkhaneh_instance: AmarKarKhaneh = AmarKarKhaneh.objects.get(pk=amarkarkhanehid)
            related_initborder: InitialBorder = amarkarkhaneh_instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای حذف آمارکارخانه محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            amarkarkhaneh_instance.delete()
            delete_logger.warning(f"حذف آمار کارخانه {amarkarkhanehid}", extra=get_details_from_request(request))
            return Response({"detail": "آمار کارخانه با موفقیت حذف شد"}, status=status.HTTP_204_NO_CONTENT)

        except AmarKarKhaneh.DoesNotExist:
            api_activity_logger.error(f"آمارکارخانه با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمارکارخانه با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در حذف آمار کارخانه محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در حذف آمار کارخانه محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AmarEstekhrajListApiView(APIView):
    """
        list of all AmarEstekhraj instances for ONE Initialborder
    """

    class AmarEstekhrajInPutSerializer(serializers.ModelSerializer):
        doure = serializers.IntegerField(
            min_value=1,
            max_value=12,
            error_messages={
                'min_value': 'دوره نمی‌تواند کمتر از 1 باشد.',
                'max_value': 'دوره نمی‌تواند بیشتر از 12 باشد.',
            }
        )
        class Meta:
            model = AmarEstekhraj
            fields = [
                'sal', 'doure', 'estekhraj_vaghei', 'motavaset_ayar_estekhraji',
                'made_madani_estekhraji' , 'ayar_made_madani',
                'mizan_batele_bardari', 'hazine_estekhraj', 'darsad_amalkard'
            ]
            # validators = [
            #     serializers.UniqueTogetherValidator(
            #         queryset=AmarEstekhraj.objects.all(),
            #         fields=['initialborder','sal', 'doure',],
            #         message='ترکیب سال، دوره قبلاً ثبت شده است.'
            #     )
            # ]

        def validate(self, attrs):
            initialborder = self.context.get('initialborder')
            if initialborder and initialborder.dtyp:
                if initialborder.dtyp.code not in AmarEstekhraj.ALLOWED_INITBORDER_CODES:
                    raise serializers.ValidationError({
                        'initialborder': f'فقط محدوده اولیه با کدهای {AmarEstekhraj.ALLOWED_INITBORDER_CODES} مجاز هستند.'
                    })
                
            sal = attrs.get('sal')
            doure = attrs.get('doure')
            
            if initialborder and AmarEstekhraj.objects.filter(
                initialborder=initialborder,
                sal=sal,
                doure=doure,
            ).exists():
                raise serializers.ValidationError(
                    'ترکیب سال و دوره و نام محصول برای این محدوده قبلاً ثبت شده است.'
                )

            
            return attrs

    class AmarEstekhrajOutPutSerializer(serializers.ModelSerializer):
        class AmarEstekhrajOutPutSerializerInitialborder(serializers.ModelSerializer):
            class Meta:
                model = InitialBorder
                fields = ['id','title']

        initialborder = AmarEstekhrajOutPutSerializerInitialborder()        
        
        class Meta:
            model = AmarEstekhraj
            fields = [
                'id', 'initialborder', 'sal', 'doure', 'estekhraj_vaghei',
                'made_madani_estekhraji' , 'ayar_made_madani',
                'motavaset_ayar_estekhraji', 'mizan_batele_bardari', 'hazine_estekhraj',
                'darsad_amalkard',
            ]

    def get(self, request: Request, initialborderid: int):
        try:
            user: User = request.user
            
            initialborder_instance: InitialBorder = InitialBorder.objects.get(pk=initialborderid)

            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                api_activity_logger.warning(f"تلاش غیرمجاز برای گرفتن لیست آمار استخراج محدوده اولیه {initialborder_instance.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            all_amarestekhraj_of_this_initborder = AmarEstekhraj.objects.filter(initialborder=initialborder_instance)
            
            if not all_amarestekhraj_of_this_initborder.exists():
                return Response({"detail": "امار استخراجی برای این محدوده اولیه وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.AmarEstekhrajOutPutSerializer(all_amarestekhraj_of_this_initborder, many=True)
            api_activity_logger.info("خواندن لیست آمار استخراج", extra=get_details_from_request(request))
            return Response(serializer.data, status=status.HTTP_200_OK)

        except InitialBorder.DoesNotExist:
            api_activity_logger.error(f"محدوده اولیه با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "محدوده اولیه با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن لیست آمار استخراج محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن لیست آمار استخراج محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request: Request, initialborderid: int):
        try:
            user: User = request.user
            initialborder_instance: InitialBorder = InitialBorder.objects.get(pk=initialborderid)

            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                api_activity_logger.warning(f"تلاش غیرمجاز برای ساخت آمار استخراج محدوده اولیه {initialborder_instance.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.AmarEstekhrajInPutSerializer(
                data=request.data,
                context={'initialborder': initialborder_instance}
            )
            if not serializer.is_valid():
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data

            amarestekhraj_new_instance = AmarEstekhraj.objects.create(
                initialborder=initialborder_instance,
                **validated_data
            )

            output_serializer = self.AmarEstekhrajOutPutSerializer(amarestekhraj_new_instance)
            api_activity_logger.info(f"ساخت آمار استخراج جدید برای محدوده {initialborder_instance.title}", extra=get_details_from_request(request))
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except InitialBorder.DoesNotExist:
            api_activity_logger.error(f"محدوده اولیه با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "محدوده اولیه با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(e)
            api_activity_logger.error(f"خطا در ساخت آمار استخراج محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در ساخت آمار استخراج محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AmarEstekhrajDetailsApiView(APIView):
    """
        Details of One AmarEstekhraj Instance
    """

    class AmarEstekhrajDetailsInputSerializer(serializers.ModelSerializer):
        doure = serializers.IntegerField(
            min_value=1,
            max_value=12,
            error_messages={
                'min_value': 'دوره نمی‌تواند کمتر از 1 باشد.',
                'max_value': 'دوره نمی‌تواند بیشتر از 12 باشد.',
            }
        )

        class Meta:
            model = AmarEstekhraj
            fields = [
                'sal', 'doure', 'estekhraj_vaghei', 'motavaset_ayar_estekhraji',
                'made_madani_estekhraji' , 'ayar_made_madani',
                'mizan_batele_bardari', 'hazine_estekhraj', 'darsad_amalkard'
            ]
            # validators = [
            #     serializers.UniqueTogetherValidator(
            #         queryset=AmarEstekhraj.objects.all(),
            #         fields=['initialborder','sal', 'doure',],
            #         message='ترکیب سال، دوره قبلاً ثبت شده است.'
            #     )
            # ]
     
        def validate(self, attrs):
            initialborder = self.context.get('initialborder')
            
            if initialborder and initialborder.dtyp:
                if initialborder.dtyp.code not in AmarEstekhraj.ALLOWED_INITBORDER_CODES:
                    raise serializers.ValidationError({
                        'initialborder': f'فقط محدوده اولیه با کدهای {AmarEstekhraj.ALLOWED_INITBORDER_CODES} مجاز هستند.'
                    })
                
            sal = attrs.get('sal')
            doure = attrs.get('doure')
            
            # Build the filter query
            queryset = AmarEstekhraj.objects.filter(
                initialborder=initialborder,
                sal=sal,
                doure=doure
            )

            # If updating (instance exists), exclude the current instance
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            if initialborder and queryset.exists():
                raise serializers.ValidationError(
                    'ترکیب سال و دوره برای این محدوده قبلاً ثبت شده است.'
            )
            
            return attrs

    class AmarEstekhrajDetailsOuputSerializer(serializers.ModelSerializer):
        class AmarEstekhrajDetailsOuputSerializerInitialborder(serializers.ModelSerializer):
            class Meta:
                model = InitialBorder
                fields = ['id','title']

        initialborder = AmarEstekhrajDetailsOuputSerializerInitialborder()        
        
        class Meta:
            model = AmarEstekhraj
            fields = [
                'id', 'initialborder', 'sal', 'doure', 'estekhraj_vaghei',
                'made_madani_estekhraji' , 'ayar_made_madani',
                'motavaset_ayar_estekhraji', 'mizan_batele_bardari', 'hazine_estekhraj',
                'darsad_amalkard',
            ]

    def get(self, request: Request, amarestekhrajid: int):
        try:
            user: User = request.user
            amarestekhraj_instance: AmarEstekhraj = AmarEstekhraj.objects.get(pk=amarestekhrajid)
            related_initborder: InitialBorder = amarestekhraj_instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای گرفتن آمار استخراج محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.AmarEstekhrajDetailsOuputSerializer(amarestekhraj_instance)
            api_activity_logger.info(f"خواندن جزئیات آمار استخراج {amarestekhraj_instance.id}", extra=get_details_from_request(request))
            return Response(serializer.data, status=status.HTTP_200_OK)

        except AmarEstekhraj.DoesNotExist:
            api_activity_logger.error(f"آمار استخراج با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمار استخراج با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن آمار استخراج محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن آمار استخراج محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request: Request, amarestekhrajid: int):
        try:
            user: User = request.user
            amarestekhraj_instance: AmarEstekhraj = AmarEstekhraj.objects.get(pk=amarestekhrajid)
            related_initborder: InitialBorder = amarestekhraj_instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای ویرایش آمار استخراج محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.AmarEstekhrajDetailsInputSerializer(
                amarestekhraj_instance,
                data=request.data,
                context={'initialborder': related_initborder}
            )
            if not serializer.is_valid():
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            output_serializer = self.AmarEstekhrajDetailsOuputSerializer(amarestekhraj_instance)
            api_activity_logger.info(f"ویرایش آمار استخراج {amarestekhraj_instance.id}", extra=get_details_from_request(request))
            return Response(output_serializer.data, status=status.HTTP_200_OK)

        except AmarEstekhraj.DoesNotExist:
            api_activity_logger.error(f"آمار استخراج با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمار استخراج با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در ویرایش آمار استخراج محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در ویرایش آمار استخراج محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request: Request, amarestekhrajid: int):
        try:
            user: User = request.user
            amarestekhraj_instance: AmarEstekhraj = AmarEstekhraj.objects.get(pk=amarestekhrajid)
            related_initborder: InitialBorder = amarestekhraj_instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای حذف آمار استخراج محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            amarestekhraj_instance.delete()
            delete_logger.warning(f"حذف آمار استخراج {amarestekhrajid}", extra=get_details_from_request(request))
            return Response({"detail": "آمار استخراج با موفقیت حذف شد"}, status=status.HTTP_204_NO_CONTENT)

        except AmarEstekhraj.DoesNotExist:
            api_activity_logger.error(f"آمار استخراج با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمار استخراج با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در حذف آمار استخراج محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در حذف آمار استخراج محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HSEPASMANDListApiView(APIView):
    """
        list of all HSEPASMAND instances for ONE Initialborder
    """

    class HSEPASMANDInPutSerializer(serializers.ModelSerializer):
        doure = serializers.IntegerField(
            min_value=1,
            max_value=12,
            error_messages={
                'min_value': 'دوره نمی‌تواند کمتر از 1 باشد.',
                'max_value': 'دوره نمی‌تواند بیشتر از 12 باشد.',
            }
        )

        class Meta:
            model = HSEPASMAND
            fields = [
                'sal', 'doure', 'onvan_pasmand', 'noe_passmand', 'vazn'
            ]
            # validators = [
            #     serializers.UniqueTogetherValidator(
            #         queryset=HSEPASMAND.objects.all(),
            #         fields=['initialborder','sal', 'doure',],
            #         message='ترکیب سال، دوره قبلاً ثبت شده است.'
            #     )
            # ]

        def validate(self, attrs):
            initialborder = self.context.get('initialborder')                
            sal = attrs.get('sal')
            doure = attrs.get('doure')
            
            if initialborder and HSEPASMAND.objects.filter(
                initialborder=initialborder,
                sal=sal,
                doure=doure,
            ).exists():
                raise serializers.ValidationError(
                    'ترکیب سال و دوره برای این محدوده قبلاً ثبت شده است.'
                )
            
            return attrs

    class HSEPASMANDOutPutSerializer(serializers.ModelSerializer):
        class HSEPASMANDOutPutSerializerInitialborder(serializers.ModelSerializer):
            class Meta:
                model = InitialBorder
                fields = ['id','title']

        initialborder = HSEPASMANDOutPutSerializerInitialborder()        
        
        class Meta:
            model = HSEPASMAND
            fields = [
                'id', 'initialborder', 'sal', 'doure', 'onvan_pasmand',
                'noe_passmand', 'vazn',
            ]

    def get(self, request: Request, initialborderid: int):
        try:
            user: User = request.user
            
            initialborder_instance: InitialBorder = InitialBorder.objects.get(pk=initialborderid)

            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                api_activity_logger.warning(f"تلاش غیرمجاز برای گرفتن لیست آمار HSE پسماند محدوده اولیه {initialborder_instance.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            all_hsepasmand_of_this_initborder = HSEPASMAND.objects.filter(initialborder=initialborder_instance)
            
            if not all_hsepasmand_of_this_initborder.exists():
                return Response({"detail": "امار HSE پسماند برای این محدوده اولیه وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.HSEPASMANDOutPutSerializer(all_hsepasmand_of_this_initborder, many=True)
            api_activity_logger.info("خواندن لیست آمار HSE پسماند", extra=get_details_from_request(request))
            return Response(serializer.data, status=status.HTTP_200_OK)

        except InitialBorder.DoesNotExist:
            api_activity_logger.error(f"محدوده اولیه با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "محدوده اولیه با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن لیست آمار HSE پسماند محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن لیست آمار HSE پسماند محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request: Request, initialborderid: int):
        try:
            user: User = request.user
            initialborder_instance: InitialBorder = InitialBorder.objects.get(pk=initialborderid)

            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                api_activity_logger.warning(f"تلاش غیرمجاز برای ساخت آمار HSE پسماند محدوده اولیه {initialborder_instance.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.HSEPASMANDInPutSerializer(
                data=request.data,
                context={'initialborder': initialborder_instance}
            )
            if not serializer.is_valid():
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data

            hsepasmand_new_instance = HSEPASMAND.objects.create(
                initialborder=initialborder_instance,
                **validated_data
            )

            output_serializer = self.HSEPASMANDOutPutSerializer(hsepasmand_new_instance)
            api_activity_logger.info(f"ساخت آمار HSE پسماند جدید برای محدوده {initialborder_instance.title}", extra=get_details_from_request(request))
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except InitialBorder.DoesNotExist:
            api_activity_logger.error(f"محدوده اولیه با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "محدوده اولیه با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در ساخت آمار HSE پسماند محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در ساخت آمار HSE پسماند محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HSEPASMANDDetailsApiView(APIView):
    """
        Details of One HSEPASMAND Instance
    """

    class HSEPASMANDDetailsInputSerializer(serializers.ModelSerializer):
        doure = serializers.IntegerField(
            min_value=1,
            max_value=12,
            error_messages={
                'min_value': 'دوره نمی‌تواند کمتر از 1 باشد.',
                'max_value': 'دوره نمی‌تواند بیشتر از 12 باشد.',
            }
        )

        class Meta:
            model = HSEPASMAND
            fields = [
                'sal', 'doure', 'onvan_pasmand', 'noe_passmand', 'vazn'
            ]
            validators = [
                serializers.UniqueTogetherValidator(
                    queryset=HSEPASMAND.objects.all(),
                    fields=['sal', 'doure',],
                    message='ترکیب سال، دوره قبلاً ثبت شده است.'
                )
            ]

        def validate(self, attrs):
            initialborder = self.context.get('initialborder')                
            sal = attrs.get('sal')
            doure = attrs.get('doure')
            
            # Build the filter query
            queryset = HSEPASMAND.objects.filter(
                initialborder=initialborder,
                sal=sal,
                doure=doure
            )

            # If updating (instance exists), exclude the current instance
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            if initialborder and queryset.exists():
                raise serializers.ValidationError(
                    'ترکیب سال و دوره برای این محدوده قبلاً ثبت شده است.'
            )

            
            return attrs

        
    class HSEPASMANDDetailsOuputSerializer(serializers.ModelSerializer):
        class HSEPASMANDDetailsOuputSerializerInitialborder(serializers.ModelSerializer):
            class Meta:
                model = InitialBorder
                fields = ['id','title']

        initialborder = HSEPASMANDDetailsOuputSerializerInitialborder()        
        
        class Meta:
            model = HSEPASMAND
            fields = [
                'id', 'initialborder', 'sal', 'doure', 'onvan_pasmand',
                'noe_passmand', 'vazn',
            ]

    def get(self, request: Request, hsepasmandid: int):
        try:
            user: User = request.user
            hsepasmand_instance: HSEPASMAND = HSEPASMAND.objects.get(pk=hsepasmandid)
            related_initborder: InitialBorder = hsepasmand_instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای گرفتن آمار HSE پسماند محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.HSEPASMANDDetailsOuputSerializer(hsepasmand_instance)
            api_activity_logger.info(f"خواندن جزئیات آمار HSE پسماند {hsepasmand_instance.id}", extra=get_details_from_request(request))
            return Response(serializer.data, status=status.HTTP_200_OK)

        except HSEPASMAND.DoesNotExist:
            api_activity_logger.error(f"آمار HSE پسماند با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمار HSE پسماند با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن آمار HSE پسماند محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن آمار HSE پسماند محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request: Request, hsepasmandid: int):
        try:
            user: User = request.user
            hsepasmand_instance: HSEPASMAND = HSEPASMAND.objects.get(pk=hsepasmandid)
            related_initborder: InitialBorder = hsepasmand_instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای ویرایش آمار HSE پسماند محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.HSEPASMANDDetailsInputSerializer(
                hsepasmand_instance,
                data=request.data,
                context={'initialborder': related_initborder}
            )
            if not serializer.is_valid():
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            output_serializer = self.HSEPASMANDDetailsOuputSerializer(hsepasmand_instance)
            api_activity_logger.info(f"ویرایش آمار HSE پسماند {hsepasmand_instance.id}", extra=get_details_from_request(request))
            return Response(output_serializer.data, status=status.HTTP_200_OK)

        except HSEPASMAND.DoesNotExist:
            api_activity_logger.error(f"آمار HSE پسماند با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمار HSE پسماند با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در ویرایش آمار HSE پسماند محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در ویرایش آمار HSE پسماند محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request: Request, hsepasmandid: int):
        try:
            user: User = request.user
            hsepasmand_instance: HSEPASMAND = HSEPASMAND.objects.get(pk=hsepasmandid)
            related_initborder: InitialBorder = hsepasmand_instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای حذف آمار HSE پسماند محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            hsepasmand_instance.delete()
            delete_logger.warning(f"حذف آمار HSE پسماند {hsepasmandid}", extra=get_details_from_request(request))
            return Response({"detail": "آمار HSE پسماند با موفقیت حذف شد"}, status=status.HTTP_204_NO_CONTENT)

        except HSEPASMAND.DoesNotExist:
            api_activity_logger.error(f"آمار HSE پسماند با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمار HSE پسماند با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در حذف آمار HSE پسماند محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در حذف آمار HSE پسماند محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HSEHADESEListApiView(APIView):
    """
        list of all HSEHADESE instances for ONE Initialborder
    """

    class HSEHADESEInPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = HSEHADESE
            fields = [
                'sal', 'shadid', 'fout', 'elat'
            ]

    class HSEHADESEOutPutSerializer(serializers.ModelSerializer):
        class HSEHADESEOutPutSerializerInitialborder(serializers.ModelSerializer):
            class Meta:
                model = InitialBorder
                fields = ['id','title']

        initialborder = HSEHADESEOutPutSerializerInitialborder()        
        
        class Meta:
            model = HSEHADESE
            fields = [
                'id', 'initialborder', 'sal', 'shadid', 'fout',
                'elat', 'created_at', 'updated_at'
            ]

    def get(self, request: Request, initialborderid: int):
        try:
            user: User = request.user
            
            initialborder_instance: InitialBorder = InitialBorder.objects.get(pk=initialborderid)

            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                api_activity_logger.warning(f"تلاش غیرمجاز برای گرفتن لیست آمار HSE حادثه محدوده اولیه {initialborder_instance.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            all_hsehadese_of_this_initborder = HSEHADESE.objects.filter(initialborder=initialborder_instance)
            
            if not all_hsehadese_of_this_initborder.exists():
                return Response({"detail": "امار HSE حادثه برای این محدوده اولیه وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.HSEHADESEOutPutSerializer(all_hsehadese_of_this_initborder, many=True)
            api_activity_logger.info("خواندن لیست آمار HSE حادثه", extra=get_details_from_request(request))
            return Response(serializer.data, status=status.HTTP_200_OK)

        except InitialBorder.DoesNotExist:
            api_activity_logger.error(f"محدوده اولیه با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "محدوده اولیه با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن لیست آمار HSE حادثه محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن لیست آمار HSE حادثه محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request: Request, initialborderid: int):
        try:
            user: User = request.user
            initialborder_instance: InitialBorder = InitialBorder.objects.get(pk=initialborderid)

            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                api_activity_logger.warning(f"تلاش غیرمجاز برای ساخت آمار HSE حادثه محدوده اولیه {initialborder_instance.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.HSEHADESEInPutSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data

            hsehadese_new_instance = HSEHADESE.objects.create(
                initialborder=initialborder_instance,
                **validated_data
            )

            output_serializer = self.HSEHADESEOutPutSerializer(hsehadese_new_instance)
            api_activity_logger.info(f"ساخت آمار HSE حادثه جدید برای محدوده {initialborder_instance.title}", extra=get_details_from_request(request))
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except InitialBorder.DoesNotExist:
            api_activity_logger.error(f"محدوده اولیه با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "محدوده اولیه با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در ساخت آمار HSE حادثه محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در ساخت آمار HSE حادثه محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HSEHADESEDetailsApiView(APIView):
    """
        Details of One HSEHADESE Instance
    """

    class HSEHADESEDetailsInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = HSEHADESE
            fields = [
                'sal', 'shadid', 'fout', 'elat'
            ]

    class HSEHADESEDetailsOuputSerializer(serializers.ModelSerializer):
        class HSEHADESEDetailsOuputSerializerInitialborder(serializers.ModelSerializer):
            class Meta:
                model = InitialBorder
                fields = ['id','title']

        initialborder = HSEHADESEDetailsOuputSerializerInitialborder()        
        
        class Meta:
            model = HSEHADESE
            fields = [
                'id', 'initialborder',
                'sal', 'shadid', 'fout','elat',
            ]

    def get(self, request: Request, hsehadeseid: int):
        try:
            user: User = request.user
            hsehadese_instance: HSEHADESE = HSEHADESE.objects.get(pk=hsehadeseid)
            related_initborder: InitialBorder = hsehadese_instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای گرفتن آمار HSE حادثه محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.HSEHADESEDetailsOuputSerializer(hsehadese_instance)
            api_activity_logger.info(f"خواندن جزئیات آمار HSE حادثه {hsehadese_instance.id}", extra=get_details_from_request(request))
            return Response(serializer.data, status=status.HTTP_200_OK)

        except HSEHADESE.DoesNotExist:
            api_activity_logger.error(f"آمار HSE حادثه با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمار HSE حادثه با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن آمار HSE حادثه محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن آمار HSE حادثه محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request: Request, hsehadeseid: int):
        try:
            user: User = request.user
            hsehadese_instance: HSEHADESE = HSEHADESE.objects.get(pk=hsehadeseid)
            related_initborder: InitialBorder = hsehadese_instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای ویرایش آمار HSE حادثه محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.HSEHADESEDetailsInputSerializer(
                hsehadese_instance,
                data=request.data
            )
            if not serializer.is_valid():
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            output_serializer = self.HSEHADESEDetailsOuputSerializer(hsehadese_instance)
            api_activity_logger.info(f"ویرایش آمار HSE حادثه {hsehadese_instance.id}", extra=get_details_from_request(request))
            return Response(output_serializer.data, status=status.HTTP_200_OK)

        except HSEHADESE.DoesNotExist:
            api_activity_logger.error(f"آمار HSE حادثه با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمار HSE حادثه با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در ویرایش آمار HSE حادثه محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در ویرایش آمار HSE حادثه محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request: Request, hsehadeseid: int):
        try:
            user: User = request.user
            hsehadese_instance: HSEHADESE = HSEHADESE.objects.get(pk=hsehadeseid)
            related_initborder: InitialBorder = hsehadese_instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای حذف آمار HSE حادثه محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            hsehadese_instance.delete()
            delete_logger.warning(f"حذف آمار HSE حادثه {hsehadeseid}", extra=get_details_from_request(request))
            return Response({"detail": "آمار HSE حادثه با موفقیت حذف شد"}, status=status.HTTP_204_NO_CONTENT)

        except HSEHADESE.DoesNotExist:
            api_activity_logger.error(f"آمار HSE حادثه با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمار HSE حادثه با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در حذف آمار HSE حادثه محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در حذف آمار HSE حادثه محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AmarEkteshafListApiView(APIView):
    """
        list of all AmarEkteshaf instances for ONE Initialborder
    """

    class AmarEkteshafInPutSerializer(serializers.ModelSerializer):
        doure = serializers.IntegerField(
            min_value=1,
            max_value=12,
            error_messages={
                'min_value': 'دوره نمی‌تواند کمتر از 1 باشد.',
                'max_value': 'دوره نمی‌تواند بیشتر از 12 باشد.',
            }
        )

        class Meta:
            model = AmarEkteshaf
            fields = [
                'sal', 'doure', 'masahat_mored_ekteshaf', 'darsad_pishraft',
                'hazine_kol', 'ayar_made_madani'
            ]

        def validate(self, attrs):
            initialborder = self.context.get('initialborder')                
            sal = attrs.get('sal')
            doure = attrs.get('doure')
            
            if initialborder and AmarEkteshaf.objects.filter(
                initialborder=initialborder,
                sal=sal,
                doure=doure,
            ).exists():
                raise serializers.ValidationError(
                    'ترکیب سال و دوره برای این محدوده قبلاً ثبت شده است.'
                )
            
            return attrs

    class AmarEkteshafOutPutSerializer(serializers.ModelSerializer):
        class AmarEkteshafOutPutSerializerInitialborder(serializers.ModelSerializer):
            class Meta:
                model = InitialBorder
                fields = ['id','title']

        initialborder = AmarEkteshafOutPutSerializerInitialborder()        
        
        class Meta:
            model = AmarEkteshaf
            fields = [
                'id', 'initialborder', 'sal', 'doure', 'masahat_mored_ekteshaf',
                'darsad_pishraft', 'hazine_kol', 'ayar_made_madani',
            ]

    def get(self, request: Request, initialborderid: int):
        try:
            user: User = request.user
            
            initialborder_instance: InitialBorder = InitialBorder.objects.get(pk=initialborderid)

            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                api_activity_logger.warning(f"تلاش غیرمجاز برای گرفتن لیست آمار اکتشاف محدوده اولیه {initialborder_instance.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            all_amarekteshaf_of_this_initborder = AmarEkteshaf.objects.filter(initialborder=initialborder_instance)
            
            if not all_amarekteshaf_of_this_initborder.exists():
                return Response({"detail": "امار اکتشاف برای این محدوده اولیه وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.AmarEkteshafOutPutSerializer(all_amarekteshaf_of_this_initborder, many=True)
            api_activity_logger.info("خواندن لیست آمار اکتشاف", extra=get_details_from_request(request))
            return Response(serializer.data, status=status.HTTP_200_OK)

        except InitialBorder.DoesNotExist:
            api_activity_logger.error(f"محدوده اولیه با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "محدوده اولیه با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن لیست آمار اکتشاف محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن لیست آمار اکتشاف محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request: Request, initialborderid: int):
        try:
            user: User = request.user
            initialborder_instance: InitialBorder = InitialBorder.objects.get(pk=initialborderid)

            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                api_activity_logger.warning(f"تلاش غیرمجاز برای ساخت آمار اکتشاف محدوده اولیه {initialborder_instance.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.AmarEkteshafInPutSerializer(
                data=request.data,
                context={'initialborder': initialborder_instance}
            )
            if not serializer.is_valid():
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data

            amarekteshaf_new_instance = AmarEkteshaf.objects.create(
                initialborder=initialborder_instance,
                **validated_data
            )

            output_serializer = self.AmarEkteshafOutPutSerializer(amarekteshaf_new_instance)
            api_activity_logger.info(f"ساخت آمار اکتشاف جدید برای محدوده {initialborder_instance.title}", extra=get_details_from_request(request))
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except InitialBorder.DoesNotExist:
            api_activity_logger.error(f"محدوده اولیه با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "محدوده اولیه با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در ساخت آمار اکتشاف محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در ساخت آمار اکتشاف محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AmarEkteshafDetailsApiView(APIView):
    """
        Details of One AmarEkteshaf Instance
    """

    class AmarEkteshafDetailsInputSerializer(serializers.ModelSerializer):
        doure = serializers.IntegerField(
            min_value=1,
            max_value=12,
            error_messages={
                'min_value': 'دوره نمی‌تواند کمتر از 1 باشد.',
                'max_value': 'دوره نمی‌تواند بیشتر از 12 باشد.',
            }
        )

        class Meta:
            model = AmarEkteshaf
            fields = [
                'sal', 'doure', 'masahat_mored_ekteshaf', 'darsad_pishraft',
                'hazine_kol', 'ayar_made_madani'
            ]

        def validate(self, attrs):
            initialborder = self.context.get('initialborder')                
            sal = attrs.get('sal')
            doure = attrs.get('doure')
            
            # Build the filter query
            queryset = AmarEkteshaf.objects.filter(
                initialborder=initialborder,
                sal=sal,
                doure=doure
            )

            # If updating (instance exists), exclude the current instance
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            if initialborder and queryset.exists():
                raise serializers.ValidationError(
                    'ترکیب سال و دوره برای این محدوده قبلاً ثبت شده است.'
                )

            return attrs

        
    class AmarEkteshafDetailsOuputSerializer(serializers.ModelSerializer):
        class AmarEkteshafDetailsOuputSerializerInitialborder(serializers.ModelSerializer):
            class Meta:
                model = InitialBorder
                fields = ['id','title']

        initialborder = AmarEkteshafDetailsOuputSerializerInitialborder()        
        
        class Meta:
            model = AmarEkteshaf
            fields = [
                'id', 'initialborder', 'sal', 'doure', 'masahat_mored_ekteshaf',
                'darsad_pishraft', 'hazine_kol', 'ayar_made_madani',
            ]

    def get(self, request: Request, amarekteshafid: int):
        try:
            user: User = request.user
            amarekteshaf_instance: AmarEkteshaf = AmarEkteshaf.objects.get(pk=amarekteshafid)
            related_initborder: InitialBorder = amarekteshaf_instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای گرفتن آمار اکتشاف محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.AmarEkteshafDetailsOuputSerializer(amarekteshaf_instance)
            api_activity_logger.info(f"خواندن جزئیات آمار اکتشاف {amarekteshaf_instance.id}", extra=get_details_from_request(request))
            return Response(serializer.data, status=status.HTTP_200_OK)

        except AmarEkteshaf.DoesNotExist:
            api_activity_logger.error(f"آمار اکتشاف با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمار اکتشاف با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن آمار اکتشاف محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن آمار اکتشاف محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request: Request, amarekteshafid: int):
        try:
            user: User = request.user
            amarekteshaf_instance: AmarEkteshaf = AmarEkteshaf.objects.get(pk=amarekteshafid)
            related_initborder: InitialBorder = amarekteshaf_instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای ویرایش آمار اکتشاف محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.AmarEkteshafDetailsInputSerializer(
                amarekteshaf_instance,
                data=request.data,
                context={'initialborder': related_initborder}
            )
            if not serializer.is_valid():
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            output_serializer = self.AmarEkteshafDetailsOuputSerializer(amarekteshaf_instance)
            api_activity_logger.info(f"ویرایش آمار اکتشاف {amarekteshaf_instance.id}", extra=get_details_from_request(request))
            return Response(output_serializer.data, status=status.HTTP_200_OK)

        except AmarEkteshaf.DoesNotExist:
            api_activity_logger.error(f"آمار اکتشاف با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمار اکتشاف با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در ویرایش آمار اکتشاف محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در ویرایش آمار اکتشاف محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request: Request, amarekteshafid: int):
        try:
            user: User = request.user
            amarekteshaf_instance: AmarEkteshaf = AmarEkteshaf.objects.get(pk=amarekteshafid)
            related_initborder: InitialBorder = amarekteshaf_instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای حذف آمار اکتشاف محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            amarekteshaf_instance.delete()
            delete_logger.warning(f"حذف آمار اکتشاف {amarekteshafid}", extra=get_details_from_request(request))
            return Response({"detail": "آمار اکتشاف با موفقیت حذف شد"}, status=status.HTTP_204_NO_CONTENT)

        except AmarEkteshaf.DoesNotExist:
            api_activity_logger.error(f"آمار اکتشاف با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمار اکتشاف با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در حذف آمار اکتشاف محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در حذف آمار اکتشاف محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AmarAmalkardTajhizCoalListApiView(APIView):
    """
        list of all AmarAmalkardTajhizCoal instances for ONE Initialborder
    """

    class AmarAmalkardTajhizCoalInPutSerializer(serializers.ModelSerializer):
        doure = serializers.IntegerField(
            min_value=1,
            max_value=12,
            error_messages={
                'min_value': 'دوره نمی‌تواند کمتر از 1 باشد.',
                'max_value': 'دوره نمی‌تواند بیشتر از 12 باشد.',
            }
        )
        class Meta:
            model = AmarAmalkardTajhizCoal
            fields = [
                'sal', 'doure', 'zamanstarttajhiz', 'reveshejraamaliyatmadani',
                'raveshehdastasisat', 'namepeymankar', 'peymankar_typ',
                'pishraft_pi_amal_madani_tadoureghabl', 'pishraft_pi_amal_ehdassathi_tadoureghabl',
                'pishraft_pi_amal_taminabobargh_tadoureghabl', 'pishraft_pi_kol_tadoureghabl',
                'amouzehkarkonano_tadoureghabl', 'meghdar_zoghal_estekhraj', 'meghdar_zoghal_zakhire'
            ]

        def validate(self, attrs):
            initialborder = self.context.get('initialborder')
            if initialborder and initialborder.dtyp:
                if initialborder.dtyp.code not in AmarAmalkardTajhizCoal.ALLOWED_INITBORDER_CODES:
                    raise serializers.ValidationError({
                        'initialborder': f'فقط محدوده اولیه با کدهای {AmarAmalkardTajhizCoal.ALLOWED_INITBORDER_CODES} مجاز هستند.'
                    })

            sal = attrs.get('sal')
            doure = attrs.get('doure')

            if initialborder and AmarAmalkardTajhizCoal.objects.filter(
                initialborder=initialborder,
                sal=sal,
                doure=doure,
            ).exists():
                raise serializers.ValidationError(
                    'ترکیب سال و دوره برای این محدوده قبلاً ثبت شده است.'
                )

            return attrs

    class AmarAmalkardTajhizCoalOutPutSerializer(serializers.ModelSerializer):
        class AmarAmalkardTajhizCoalOutPutSerializerInitialborder(serializers.ModelSerializer):
            class Meta:
                model = InitialBorder
                fields = ['id', 'title']

        initialborder = AmarAmalkardTajhizCoalOutPutSerializerInitialborder()

        class Meta:
            model = AmarAmalkardTajhizCoal
            fields = [
                'id', 'initialborder', 'sal', 'doure', 'zamanstarttajhiz',
                'reveshejraamaliyatmadani', 'raveshehdastasisat', 'namepeymankar', 'peymankar_typ',
                'pishraft_pi_amal_madani_tadoureghabl', 'pishraft_pi_amal_ehdassathi_tadoureghabl',
                'pishraft_pi_amal_taminabobargh_tadoureghabl', 'pishraft_pi_kol_tadoureghabl',
                'amouzehkarkonano_tadoureghabl', 'meghdar_zoghal_estekhraj', 'meghdar_zoghal_zakhire'
            ]

    def get(self, request: Request, initialborderid: int):
        try:
            user: User = request.user

            initialborder_instance: InitialBorder = InitialBorder.objects.get(pk=initialborderid)

            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                api_activity_logger.warning(f"تلاش غیرمجاز برای گرفتن لیست آمار عملکرد تجهیز زغال محدوده اولیه {initialborder_instance.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            all_instances = AmarAmalkardTajhizCoal.objects.filter(initialborder=initialborder_instance)

            if not all_instances.exists():
                return Response({"detail": "آمار عملکرد تجهیز زغالی برای این محدوده اولیه وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.AmarAmalkardTajhizCoalOutPutSerializer(all_instances, many=True)
            api_activity_logger.info("خواندن لیست آمار عملکرد تجهیز زغال", extra=get_details_from_request(request))
            return Response(serializer.data, status=status.HTTP_200_OK)

        except InitialBorder.DoesNotExist as e:
            api_activity_logger.error(f"محدوده اولیه با این شناسه یافت نشد {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "محدوده اولیه با این شناسه یافت نشد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن لیست آمار عملکرد تجهیز زغال محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن لیست آمار عملکرد تجهیز زغال محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request: Request, initialborderid: int):
        try:
            user: User = request.user
            initialborder_instance: InitialBorder = InitialBorder.objects.get(pk=initialborderid)

            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                api_activity_logger.warning(f"تلاش غیرمجاز برای ساخت آمار عملکرد تجهیز زغال محدوده اولیه {initialborder_instance.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.AmarAmalkardTajhizCoalInPutSerializer(
                data=request.data,
                context={'initialborder': initialborder_instance}
            )
            if not serializer.is_valid():
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            validated_data = serializer.validated_data

            new_instance = AmarAmalkardTajhizCoal.objects.create(
                initialborder=initialborder_instance,
                **validated_data
            )

            output_serializer = self.AmarAmalkardTajhizCoalOutPutSerializer(new_instance)
            api_activity_logger.info(f"ساخت آمار عملکرد تجهیز زغال جدید برای محدوده {initialborder_instance.title}", extra=get_details_from_request(request))
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except InitialBorder.DoesNotExist as e:
            api_activity_logger.error(f"محدوده اولیه با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "محدوده اولیه با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در ساخت آمار عملکرد تجهیز زغال محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در ساخت آمار عملکرد تجهیز زغال محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AmarAmalkardTajhizCoalDetailsApiView(APIView):
    """
        Details of One AmarAmalkardTajhizCoal Instance
    """

    class AmarAmalkardTajhizCoalDetailsInputSerializer(serializers.ModelSerializer):
        doure = serializers.IntegerField(
            min_value=1,
            max_value=12,
            error_messages={
                'min_value': 'دوره نمی‌تواند کمتر از 1 باشد.',
                'max_value': 'دوره نمی‌تواند بیشتر از 12 باشد.',
            }
        )
        class Meta:
            model = AmarAmalkardTajhizCoal
            fields = [
                'sal', 'doure', 'zamanstarttajhiz', 'reveshejraamaliyatmadani',
                'raveshehdastasisat', 'namepeymankar', 'peymankar_typ',
                'pishraft_pi_amal_madani_tadoureghabl', 'pishraft_pi_amal_ehdassathi_tadoureghabl',
                'pishraft_pi_amal_taminabobargh_tadoureghabl', 'pishraft_pi_kol_tadoureghabl',
                'amouzehkarkonano_tadoureghabl', 'meghdar_zoghal_estekhraj', 'meghdar_zoghal_zakhire'
            ]

        def validate(self, attrs):
            initialborder = self.context.get('initialborder')

            if initialborder and initialborder.dtyp:
                if initialborder.dtyp.code not in AmarAmalkardTajhizCoal.ALLOWED_INITBORDER_CODES:
                    raise serializers.ValidationError({
                        'initialborder': f'فقط محدوده اولیه با کدهای {AmarAmalkardTajhizCoal.ALLOWED_INITBORDER_CODES} مجاز هستند.'
                    })

            sal = attrs.get('sal')
            doure = attrs.get('doure')

            queryset = AmarAmalkardTajhizCoal.objects.filter(
                initialborder=initialborder,
                sal=sal,
                doure=doure,
            )

            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            if initialborder and queryset.exists():
                raise serializers.ValidationError(
                    'ترکیب سال و دوره برای این محدوده قبلاً ثبت شده است.'
                )

            return attrs

    class AmarAmalkardTajhizCoalDetailsOuputSerializer(serializers.ModelSerializer):
        class AmarAmalkardTajhizCoalDetailsOuputSerializerInitialborder(serializers.ModelSerializer):
            class Meta:
                model = InitialBorder
                fields = ['id', 'title']

        initialborder = AmarAmalkardTajhizCoalDetailsOuputSerializerInitialborder()

        class Meta:
            model = AmarAmalkardTajhizCoal
            fields = [
                'id', 'initialborder', 'sal', 'doure', 'zamanstarttajhiz',
                'reveshejraamaliyatmadani', 'raveshehdastasisat', 'namepeymankar', 'peymankar_typ',
                'pishraft_pi_amal_madani_tadoureghabl', 'pishraft_pi_amal_ehdassathi_tadoureghabl',
                'pishraft_pi_amal_taminabobargh_tadoureghabl', 'pishraft_pi_kol_tadoureghabl',
                'amouzehkarkonano_tadoureghabl', 'meghdar_zoghal_estekhraj', 'meghdar_zoghal_zakhire'
            ]

    def get(self, request: Request, amaramalkardtajhizcoalid: int):
        try:
            user: User = request.user
            instance: AmarAmalkardTajhizCoal = AmarAmalkardTajhizCoal.objects.get(pk=amaramalkardtajhizcoalid)
            related_initborder: InitialBorder = instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای گرفتن آمار عملکرد تجهیز زغال محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.AmarAmalkardTajhizCoalDetailsOuputSerializer(instance)
            api_activity_logger.info(f"خواندن جزئیات آمار عملکرد تجهیز زغال {instance.id}", extra=get_details_from_request(request))
            return Response(serializer.data, status=status.HTTP_200_OK)

        except AmarAmalkardTajhizCoal.DoesNotExist:
            api_activity_logger.error(f"آمار عملکرد تجهیز زغال با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمار عملکرد تجهیز زغال با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن آمار عملکرد تجهیز زغال محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن آمار عملکرد تجهیز زغال محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request: Request, amaramalkardtajhizcoalid: int):
        try:
            user: User = request.user
            instance: AmarAmalkardTajhizCoal = AmarAmalkardTajhizCoal.objects.get(pk=amaramalkardtajhizcoalid)
            related_initborder: InitialBorder = instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای ویرایش آمار عملکرد تجهیز زغال محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.AmarAmalkardTajhizCoalDetailsInputSerializer(
                instance,
                data=request.data,
                context={'initialborder': related_initborder}
            )
            if not serializer.is_valid():
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            output_serializer = self.AmarAmalkardTajhizCoalDetailsOuputSerializer(instance)
            api_activity_logger.info(f"ویرایش آمار عملکرد تجهیز زغال {instance.id}", extra=get_details_from_request(request))
            return Response(output_serializer.data, status=status.HTTP_200_OK)

        except AmarAmalkardTajhizCoal.DoesNotExist:
            api_activity_logger.error(f"آمار عملکرد تجهیز زغال با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمار عملکرد تجهیز زغال با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در ویرایش آمار عملکرد تجهیز زغال محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در ویرایش آمار عملکرد تجهیز زغال محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request: Request, amaramalkardtajhizcoalid: int):
        try:
            user: User = request.user
            instance: AmarAmalkardTajhizCoal = AmarAmalkardTajhizCoal.objects.get(pk=amaramalkardtajhizcoalid)
            related_initborder: InitialBorder = instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای حذف آمار عملکرد تجهیز زغال محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            instance.delete()
            delete_logger.warning(f"حذف آمار عملکرد تجهیز زغال {amaramalkardtajhizcoalid}", extra=get_details_from_request(request))
            return Response({"detail": "آمار عملکرد تجهیز زغال با موفقیت حذف شد"}, status=status.HTTP_204_NO_CONTENT)

        except AmarAmalkardTajhizCoal.DoesNotExist:
            api_activity_logger.error(f"آمار عملکرد تجهیز زغال با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمار عملکرد تجهیز زغال با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در حذف آمار عملکرد تجهیز زغال محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در حذف آمار عملکرد تجهیز زغال محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AmarAmalkardBahrebardariCoalListApiView(APIView):
    """
        list of all AmarAmalkardBahrebardariCoal instances for ONE Initialborder
    """

    class AmarAmalkardBahrebardariCoalInPutSerializer(serializers.ModelSerializer):
        doure = serializers.IntegerField(
            min_value=1,
            max_value=12,
            error_messages={
                'min_value': 'دوره نمی‌تواند کمتر از 1 باشد.',
                'max_value': 'دوره نمی‌تواند بیشتر از 12 باشد.',
            }
        )
        class Meta:
            model = AmarAmalkardBahrebardariCoal
            fields = [
                'sal', 'doure', 'reveshejraamaliyatmadani', 'namepeymankar',
                'peymankar_typ', 'meghdarestekhraj', 'karkonan_amani_avg',
                'karkonan_peymani_avg', 'hajmbatelebardari', 'hajmmasrafchoub_avg',
                'mavadnarie', 'masrafab_avg', 'masrafbargh_avg', 'masrafsoukht_avg',
                'zakhireestekhrajbaghimande', 'zakhireamadesazishode',
                'amouzeshkarkonan', 'mahaltahvilyaforoush'
            ]

        def validate(self, attrs):
            initialborder = self.context.get('initialborder')
            if initialborder and initialborder.dtyp:
                if initialborder.dtyp.code not in AmarAmalkardBahrebardariCoal.ALLOWED_INITBORDER_CODES:
                    raise serializers.ValidationError({
                        'initialborder': f'فقط محدوده اولیه با کدهای {AmarAmalkardBahrebardariCoal.ALLOWED_INITBORDER_CODES} مجاز هستند.'
                    })

            sal = attrs.get('sal')
            doure = attrs.get('doure')

            if initialborder and AmarAmalkardBahrebardariCoal.objects.filter(
                initialborder=initialborder,
                sal=sal,
                doure=doure,
            ).exists():
                raise serializers.ValidationError(
                    'ترکیب سال و دوره برای این محدوده قبلاً ثبت شده است.'
                )

            return attrs

    class AmarAmalkardBahrebardariCoalOutPutSerializer(serializers.ModelSerializer):
        class AmarAmalkardBahrebardariCoalOutPutSerializerInitialborder(serializers.ModelSerializer):
            class Meta:
                model = InitialBorder
                fields = ['id', 'title']

        initialborder = AmarAmalkardBahrebardariCoalOutPutSerializerInitialborder()

        class Meta:
            model = AmarAmalkardBahrebardariCoal
            fields = [
                'id', 'initialborder', 'sal', 'doure', 'reveshejraamaliyatmadani',
                'namepeymankar', 'peymankar_typ', 'meghdarestekhraj',
                'karkonan_amani_avg', 'karkonan_peymani_avg', 'hajmbatelebardari',
                'hajmmasrafchoub_avg', 'mavadnarie', 'masrafab_avg', 'masrafbargh_avg',
                'masrafsoukht_avg', 'zakhireestekhrajbaghimande', 'zakhireamadesazishode',
                'amouzeshkarkonan', 'mahaltahvilyaforoush'
            ]

    def get(self, request: Request, initialborderid: int):
        try:
            user: User = request.user

            initialborder_instance: InitialBorder = InitialBorder.objects.get(pk=initialborderid)

            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                api_activity_logger.warning(f"تلاش غیرمجاز برای گرفتن لیست آمار عملکرد بهره برداری زغال محدوده اولیه {initialborder_instance.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            all_instances = AmarAmalkardBahrebardariCoal.objects.filter(initialborder=initialborder_instance)

            if not all_instances.exists():
                return Response({"detail": "آمار عملکرد بهره برداری زغالی برای این محدوده اولیه وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.AmarAmalkardBahrebardariCoalOutPutSerializer(all_instances, many=True)
            api_activity_logger.info("خواندن لیست آمار عملکرد بهره برداری زغال", extra=get_details_from_request(request))
            return Response(serializer.data, status=status.HTTP_200_OK)

        except InitialBorder.DoesNotExist as e:
            api_activity_logger.error(f"محدوده اولیه با این شناسه یافت نشد {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "محدوده اولیه با این شناسه یافت نشد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن لیست آمار عملکرد بهره برداری زغال محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن لیست آمار عملکرد بهره برداری زغال محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request: Request, initialborderid: int):
        try:
            user: User = request.user
            initialborder_instance: InitialBorder = InitialBorder.objects.get(pk=initialborderid)

            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                api_activity_logger.warning(f"تلاش غیرمجاز برای ساخت آمار عملکرد بهره برداری زغال محدوده اولیه {initialborder_instance.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.AmarAmalkardBahrebardariCoalInPutSerializer(
                data=request.data,
                context={'initialborder': initialborder_instance}
            )
            if not serializer.is_valid():
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            validated_data = serializer.validated_data

            new_instance = AmarAmalkardBahrebardariCoal.objects.create(
                initialborder=initialborder_instance,
                **validated_data
            )

            output_serializer = self.AmarAmalkardBahrebardariCoalOutPutSerializer(new_instance)
            api_activity_logger.info(f"ساخت آمار عملکرد بهره برداری زغال جدید برای محدوده {initialborder_instance.title}", extra=get_details_from_request(request))
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except InitialBorder.DoesNotExist as e:
            api_activity_logger.error(f"محدوده اولیه با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "محدوده اولیه با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در ساخت آمار عملکرد بهره برداری زغال محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در ساخت آمار عملکرد بهره برداری زغال محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AmarAmalkardBahrebardariCoalDetailsApiView(APIView):
    """
        Details of One AmarAmalkardBahrebardariCoal Instance
    """

    class AmarAmalkardBahrebardariCoalDetailsInputSerializer(serializers.ModelSerializer):
        doure = serializers.IntegerField(
            min_value=1,
            max_value=12,
            error_messages={
                'min_value': 'دوره نمی‌تواند کمتر از 1 باشد.',
                'max_value': 'دوره نمی‌تواند بیشتر از 12 باشد.',
            }
        )
        class Meta:
            model = AmarAmalkardBahrebardariCoal
            fields = [
                'sal', 'doure', 'reveshejraamaliyatmadani', 'namepeymankar',
                'peymankar_typ', 'meghdarestekhraj', 'karkonan_amani_avg',
                'karkonan_peymani_avg', 'hajmbatelebardari', 'hajmmasrafchoub_avg',
                'mavadnarie', 'masrafab_avg', 'masrafbargh_avg', 'masrafsoukht_avg',
                'zakhireestekhrajbaghimande', 'zakhireamadesazishode',
                'amouzeshkarkonan', 'mahaltahvilyaforoush'
            ]

        def validate(self, attrs):
            initialborder = self.context.get('initialborder')

            if initialborder and initialborder.dtyp:
                if initialborder.dtyp.code not in AmarAmalkardBahrebardariCoal.ALLOWED_INITBORDER_CODES:
                    raise serializers.ValidationError({
                        'initialborder': f'فقط محدوده اولیه با کدهای {AmarAmalkardBahrebardariCoal.ALLOWED_INITBORDER_CODES} مجاز هستند.'
                    })

            sal = attrs.get('sal')
            doure = attrs.get('doure')

            queryset = AmarAmalkardBahrebardariCoal.objects.filter(
                initialborder=initialborder,
                sal=sal,
                doure=doure,
            )

            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            if initialborder and queryset.exists():
                raise serializers.ValidationError(
                    'ترکیب سال و دوره برای این محدوده قبلاً ثبت شده است.'
                )

            return attrs

    class AmarAmalkardBahrebardariCoalDetailsOuputSerializer(serializers.ModelSerializer):
        class AmarAmalkardBahrebardariCoalDetailsOuputSerializerInitialborder(serializers.ModelSerializer):
            class Meta:
                model = InitialBorder
                fields = ['id', 'title']

        initialborder = AmarAmalkardBahrebardariCoalDetailsOuputSerializerInitialborder()

        class Meta:
            model = AmarAmalkardBahrebardariCoal
            fields = [
                'id', 'initialborder', 'sal', 'doure', 'reveshejraamaliyatmadani',
                'namepeymankar', 'peymankar_typ', 'meghdarestekhraj',
                'karkonan_amani_avg', 'karkonan_peymani_avg', 'hajmbatelebardari',
                'hajmmasrafchoub_avg', 'mavadnarie', 'masrafab_avg', 'masrafbargh_avg',
                'masrafsoukht_avg', 'zakhireestekhrajbaghimande', 'zakhireamadesazishode',
                'amouzeshkarkonan', 'mahaltahvilyaforoush'
            ]

    def get(self, request: Request, amaramalkardbahrebardaricoalid: int):
        try:
            user: User = request.user
            instance: AmarAmalkardBahrebardariCoal = AmarAmalkardBahrebardariCoal.objects.get(pk=amaramalkardbahrebardaricoalid)
            related_initborder: InitialBorder = instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای گرفتن آمار عملکرد بهره برداری زغال محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.AmarAmalkardBahrebardariCoalDetailsOuputSerializer(instance)
            api_activity_logger.info(f"خواندن جزئیات آمار عملکرد بهره برداری زغال {instance.id}", extra=get_details_from_request(request))
            return Response(serializer.data, status=status.HTTP_200_OK)

        except AmarAmalkardBahrebardariCoal.DoesNotExist:
            api_activity_logger.error(f"آمار عملکرد بهره برداری زغال با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمار عملکرد بهره برداری زغال با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن آمار عملکرد بهره برداری زغال محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن آمار عملکرد بهره برداری زغال محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request: Request, amaramalkardbahrebardaricoalid: int):
        try:
            user: User = request.user
            instance: AmarAmalkardBahrebardariCoal = AmarAmalkardBahrebardariCoal.objects.get(pk=amaramalkardbahrebardaricoalid)
            related_initborder: InitialBorder = instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای ویرایش آمار عملکرد بهره برداری زغال محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.AmarAmalkardBahrebardariCoalDetailsInputSerializer(
                instance,
                data=request.data,
                context={'initialborder': related_initborder}
            )
            if not serializer.is_valid():
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            output_serializer = self.AmarAmalkardBahrebardariCoalDetailsOuputSerializer(instance)
            api_activity_logger.info(f"ویرایش آمار عملکرد بهره برداری زغال {instance.id}", extra=get_details_from_request(request))
            return Response(output_serializer.data, status=status.HTTP_200_OK)

        except AmarAmalkardBahrebardariCoal.DoesNotExist:
            api_activity_logger.error(f"آمار عملکرد بهره برداری زغال با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمار عملکرد بهره برداری زغال با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در ویرایش آمار عملکرد بهره برداری زغال محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در ویرایش آمار عملکرد بهره برداری زغال محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request: Request, amaramalkardbahrebardaricoalid: int):
        try:
            user: User = request.user
            instance: AmarAmalkardBahrebardariCoal = AmarAmalkardBahrebardariCoal.objects.get(pk=amaramalkardbahrebardaricoalid)
            related_initborder: InitialBorder = instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای حذف آمار عملکرد بهره برداری زغال محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            instance.delete()
            delete_logger.warning(f"حذف آمار عملکرد بهره برداری زغال {amaramalkardbahrebardaricoalid}", extra=get_details_from_request(request))
            return Response({"detail": "آمار عملکرد بهره برداری زغال با موفقیت حذف شد"}, status=status.HTTP_204_NO_CONTENT)

        except AmarAmalkardBahrebardariCoal.DoesNotExist:
            api_activity_logger.error(f"آمار عملکرد بهره برداری زغال با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمار عملکرد بهره برداری زغال با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در حذف آمار عملکرد بهره برداری زغال محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در حذف آمار عملکرد بهره برداری زغال محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)