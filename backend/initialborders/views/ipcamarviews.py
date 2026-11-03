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
from initialborders.models.ipcamar import (
    IpcAmarEkteshaf,
    IpcBarnamehEkteshaf,
)

delete_logger = logging.getLogger('delete_activity_logger')
api_activity_logger = logging.getLogger('api_activity_logger')


class IpcAmarEkteshafListApiView(APIView):
    """
        list of all IpcAmarEkteshaf instances for ONE Initialborder
    """

    class IpcAmarEkteshafInPutSerializer(serializers.ModelSerializer):
        doure = serializers.IntegerField(
            min_value=1,
            max_value=12,
            error_messages={
                'min_value': 'دوره نمی‌تواند کمتر از 1 باشد.',
                'max_value': 'دوره نمی‌تواند بیشتر از 12 باشد.',
            }
        )

        class Meta:
            model = IpcAmarEkteshaf
            fields = [
                'sal', 'doure', 'faz', 'shakhes', 'vahed',
                'meghdar', 'descriptions'
            ]
            # validators = [
            #     serializers.UniqueTogetherValidator(
            #         queryset=IpcAmarEkteshaf.objects.all(),
            #         fields=['initialborder', 'sal', 'doure', 'faz', 'shakhes'],
            #         message='ترکیب سال، دوره، فاز و شاخص قبلاً ثبت شده است.'
            #     )
            # ]

        def validate(self, attrs):
            initialborder = self.context.get('initialborder')

            sal = attrs.get('sal')
            doure = attrs.get('doure')
            faz = attrs.get('faz')
            shakhes = attrs.get('shakhes')

            if initialborder and IpcAmarEkteshaf.objects.filter(
                initialborder=initialborder,
                sal=sal,
                doure=doure,
                faz=faz,
                shakhes=shakhes
            ).exists():
                raise serializers.ValidationError(
                    'ترکیب سال، دوره، فاز و شاخص برای این محدوده قبلاً ثبت شده است.'
                )

            return attrs

    class IpcAmarEkteshafOutPutSerializer(serializers.ModelSerializer):
        class IpcAmarEkteshafOutPutSerializerInitialborder(serializers.ModelSerializer):
            class Meta:
                model = InitialBorder
                fields = ['id', 'title']

        initialborder = IpcAmarEkteshafOutPutSerializerInitialborder()

        class Meta:
            model = IpcAmarEkteshaf
            fields = [
                'id', 'initialborder', 'sal', 'doure', 'faz', 'shakhes',
                'vahed', 'meghdar', 'descriptions'
            ]

    def get(self, request: Request, initialborderid: int):
        try:
            user: User = request.user

            initialborder_instance: InitialBorder = InitialBorder.objects.get(pk=initialborderid)

            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                api_activity_logger.warning(f"تلاش غیرمجاز برای گرفتن لیست آمار اکتشاف محدوده اولیه {initialborder_instance.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            all_ipcamarekteshaf_of_this_initborder = IpcAmarEkteshaf.objects.filter(initialborder=initialborder_instance)

            if not all_ipcamarekteshaf_of_this_initborder.exists():
                return Response({"detail": "آمار اکتشافی برای این محدوده اولیه وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)
            
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(all_ipcamarekteshaf_of_this_initborder, request)
            serializer = self.IpcAmarEkteshafOutPutSerializer(paginated_queryset,many=True,context={'request': request})

            api_activity_logger.info("خواندن لیست آمار اکتشاف", extra=get_details_from_request(request))
            return paginator.get_paginated_response(serializer.data)

        except InitialBorder.DoesNotExist as e:
            api_activity_logger.error(f"محدوده اولیه با این شناسه یافت نشد {str(e)}", extra=get_details_from_request(request))
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

            serializer = self.IpcAmarEkteshafInPutSerializer(
                data=request.data,
                context={'initialborder': initialborder_instance}
            )
            if not serializer.is_valid():
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            validated_data = serializer.validated_data

            ipcamarekteshaf_new_instance = IpcAmarEkteshaf.objects.create(
                initialborder=initialborder_instance,
                **validated_data
            )

            output_serializer = self.IpcAmarEkteshafOutPutSerializer(ipcamarekteshaf_new_instance)
            api_activity_logger.info(f"ساخت آمار اکتشاف جدید برای محدوده {initialborder_instance.title}", extra=get_details_from_request(request))
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except InitialBorder.DoesNotExist as e:
            api_activity_logger.error(f"محدوده اولیه با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "محدوده اولیه با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در ساخت آمار اکتشاف محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در ساخت آمار اکتشاف محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IpcAmarEkteshafDetailsApiView(APIView):
    """
        Details of One IpcAmarEkteshaf Instance
    """

    class IpcAmarEkteshafDetailsInputSerializer(serializers.ModelSerializer):
        doure = serializers.IntegerField(
            min_value=1,
            max_value=12,
            error_messages={
                'min_value': 'دوره نمی‌تواند کمتر از 1 باشد.',
                'max_value': 'دوره نمی‌تواند بیشتر از 12 باشد.',
            }
        )

        class Meta:
            model = IpcAmarEkteshaf
            fields = [
                'sal', 'doure', 'faz', 'shakhes', 'vahed',
                'meghdar', 'descriptions'
            ]

        def validate(self, attrs):
            initialborder = self.context.get('initialborder')

            sal = attrs.get('sal')
            doure = attrs.get('doure')
            faz = attrs.get('faz')
            shakhes = attrs.get('shakhes')

            queryset = IpcAmarEkteshaf.objects.filter(
                initialborder=initialborder,
                sal=sal,
                doure=doure,
                faz=faz,
                shakhes=shakhes
            )

            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            if initialborder and queryset.exists():
                raise serializers.ValidationError(
                    'ترکیب سال، دوره، فاز و شاخص برای این محدوده قبلاً ثبت شده است.'
                )

            return attrs

    class IpcAmarEkteshafDetailsOutPutSerializer(serializers.ModelSerializer):
        class IpcAmarEkteshafDetailsOutPutSerializerInitialborder(serializers.ModelSerializer):
            class Meta:
                model = InitialBorder
                fields = ['id', 'title']

        initialborder = IpcAmarEkteshafDetailsOutPutSerializerInitialborder()

        class Meta:
            model = IpcAmarEkteshaf
            fields = [
                'id', 'initialborder', 'sal', 'doure', 'faz', 'shakhes',
                'vahed', 'meghdar', 'descriptions'
            ]

    def get(self, request: Request, ipcamarekteshafid: int):
        try:
            user: User = request.user
            ipcamarekteshaf_instance: IpcAmarEkteshaf = IpcAmarEkteshaf.objects.get(pk=ipcamarekteshafid)
            related_initborder: InitialBorder = ipcamarekteshaf_instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای گرفتن آمار اکتشاف محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.IpcAmarEkteshafDetailsOutPutSerializer(ipcamarekteshaf_instance)
            api_activity_logger.info(f"خواندن جزئیات آمار اکتشاف {ipcamarekteshaf_instance.id}", extra=get_details_from_request(request))
            return Response(serializer.data, status=status.HTTP_200_OK)

        except IpcAmarEkteshaf.DoesNotExist:
            api_activity_logger.error("آمار اکتشاف با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمار اکتشاف با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن آمار اکتشاف محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن آمار اکتشاف محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request: Request, ipcamarekteshafid: int):
        try:
            user: User = request.user
            ipcamarekteshaf_instance: IpcAmarEkteshaf = IpcAmarEkteshaf.objects.get(pk=ipcamarekteshafid)
            related_initborder: InitialBorder = ipcamarekteshaf_instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای ویرایش آمار اکتشاف محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.IpcAmarEkteshafDetailsInputSerializer(
                ipcamarekteshaf_instance,
                data=request.data,
                context={'initialborder': related_initborder}
            )
            if not serializer.is_valid():
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            output_serializer = self.IpcAmarEkteshafDetailsOutPutSerializer(ipcamarekteshaf_instance)
            api_activity_logger.info(f"ویرایش آمار اکتشاف {ipcamarekteshaf_instance.id}", extra=get_details_from_request(request))
            return Response(output_serializer.data, status=status.HTTP_200_OK)

        except IpcAmarEkteshaf.DoesNotExist:
            api_activity_logger.error("آمار اکتشاف با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمار اکتشاف با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در ویرایش آمار اکتشاف محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در ویرایش آمار اکتشاف محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request: Request, ipcamarekteshafid: int):
        try:
            user: User = request.user
            ipcamarekteshaf_instance: IpcAmarEkteshaf = IpcAmarEkteshaf.objects.get(pk=ipcamarekteshafid)
            related_initborder: InitialBorder = ipcamarekteshaf_instance.initialborder

            if not user.is_superuser and not user.has_access_to_initialborder(related_initborder):
                api_activity_logger.warning(f"تلاش غیرمجاز برای حذف آمار اکتشاف محدوده اولیه {related_initborder.title}", extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            ipcamarekteshaf_instance.delete()
            delete_logger.warning(f"حذف آمار اکتشاف {ipcamarekteshafid}", extra=get_details_from_request(request))
            return Response({"detail": "آمار اکتشاف با موفقیت حذف شد"}, status=status.HTTP_204_NO_CONTENT)

        except IpcAmarEkteshaf.DoesNotExist:
            api_activity_logger.error("آمار اکتشاف با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "آمار اکتشاف با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در حذف آمار اکتشاف محدوده {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در حذف آمار اکتشاف محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IpcBarnamehEkteshafListApiView(APIView):
    """
        list of all IpcBarnamehEkteshaf instances
        NOTE: this model has no initialborder relation, so unlike
        AmarKarKhaneh / IpcAmarEkteshaf this view is not scoped per
        initialborder and does not use has_access_to_initialborder.
        Adjust permission logic below if a different access rule applies.
    """

    class IpcBarnamehEkteshafInPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = IpcBarnamehEkteshaf
            fields = [
                'sal', 'faz', 'shakhes', 'vahed', 'meghdar', 'descriptions'
            ]
            # validators = [
            #     serializers.UniqueTogetherValidator(
            #         queryset=IpcBarnamehEkteshaf.objects.all(),
            #         fields=['sal', 'faz', 'shakhes'],
            #         message='ترکیب سال، فاز و شاخص قبلاً ثبت شده است.'
            #     )
            # ]

        def validate(self, attrs):
            sal = attrs.get('sal')
            faz = attrs.get('faz')
            shakhes = attrs.get('shakhes')

            if IpcBarnamehEkteshaf.objects.filter(
                sal=sal,
                faz=faz,
                shakhes=shakhes
            ).exists():
                raise serializers.ValidationError(
                    'ترکیب سال، فاز و شاخص قبلاً ثبت شده است.'
                )

            return attrs

    class IpcBarnamehEkteshafOutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = IpcBarnamehEkteshaf
            fields = [
                'id', 'sal', 'faz', 'shakhes',
                'vahed', 'meghdar', 'descriptions'
            ]

    def get(self, request: Request):
        try:
            user: User = request.user

            all_ipcbarnamehekteshaf = IpcBarnamehEkteshaf.objects.all()

            if not all_ipcbarnamehekteshaf.exists():
                return Response({"detail": "برنامه عملکرد اکتشافی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.IpcBarnamehEkteshafOutPutSerializer(all_ipcbarnamehekteshaf, many=True)
            api_activity_logger.info("خواندن لیست برنامه عملکرد اکتشاف", extra=get_details_from_request(request))
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن لیست برنامه عملکرد اکتشاف {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن لیست برنامه عملکرد اکتشاف"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request: Request):
        try:
            user: User = request.user

            serializer = self.IpcBarnamehEkteshafInPutSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            ipcbarnamehekteshaf_new_instance = IpcBarnamehEkteshaf.objects.create(**serializer.validated_data)

            output_serializer = self.IpcBarnamehEkteshafOutPutSerializer(ipcbarnamehekteshaf_new_instance)
            api_activity_logger.info("ساخت برنامه عملکرد اکتشاف جدید", extra=get_details_from_request(request))
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            api_activity_logger.error(f"خطا در ساخت برنامه عملکرد اکتشاف {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در ساخت برنامه عملکرد اکتشاف"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IpcBarnamehEkteshafDetailsApiView(APIView):
    """
        Details of One IpcBarnamehEkteshaf Instance
    """

    class IpcBarnamehEkteshafDetailsInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = IpcBarnamehEkteshaf
            fields = [
                'sal', 'faz', 'shakhes', 'vahed', 'meghdar', 'descriptions'
            ]

        def validate(self, attrs):
            sal = attrs.get('sal')
            faz = attrs.get('faz')
            shakhes = attrs.get('shakhes')

            queryset = IpcBarnamehEkteshaf.objects.filter(
                sal=sal,
                faz=faz,
                shakhes=shakhes
            )

            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            if queryset.exists():
                raise serializers.ValidationError(
                    'ترکیب سال، فاز و شاخص قبلاً ثبت شده است.'
                )

            return attrs

    class IpcBarnamehEkteshafDetailsOutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = IpcBarnamehEkteshaf
            fields = [
                'id', 'sal', 'faz', 'shakhes', 'vahed', 'meghdar', 'descriptions'
            ]

    def get(self, request: Request, ipcbarnamehekteshafid: int):
        try:
            user: User = request.user
            ipcbarnamehekteshaf_instance: IpcBarnamehEkteshaf = IpcBarnamehEkteshaf.objects.get(pk=ipcbarnamehekteshafid)

            serializer = self.IpcBarnamehEkteshafDetailsOutPutSerializer(ipcbarnamehekteshaf_instance)
            api_activity_logger.info(f"خواندن جزئیات برنامه عملکرد اکتشاف {ipcbarnamehekteshaf_instance.id}", extra=get_details_from_request(request))
            return Response(serializer.data, status=status.HTTP_200_OK)

        except IpcBarnamehEkteshaf.DoesNotExist:
            api_activity_logger.error("برنامه عملکرد اکتشاف با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "برنامه عملکرد اکتشاف با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن برنامه عملکرد اکتشاف {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن برنامه عملکرد اکتشاف"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request: Request, ipcbarnamehekteshafid: int):
        try:
            user: User = request.user
            ipcbarnamehekteshaf_instance: IpcBarnamehEkteshaf = IpcBarnamehEkteshaf.objects.get(pk=ipcbarnamehekteshafid)

            serializer = self.IpcBarnamehEkteshafDetailsInputSerializer(
                ipcbarnamehekteshaf_instance,
                data=request.data
            )
            if not serializer.is_valid():
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            output_serializer = self.IpcBarnamehEkteshafDetailsOutPutSerializer(ipcbarnamehekteshaf_instance)
            api_activity_logger.info(f"ویرایش برنامه عملکرد اکتشاف {ipcbarnamehekteshaf_instance.id}", extra=get_details_from_request(request))
            return Response(output_serializer.data, status=status.HTTP_200_OK)

        except IpcBarnamehEkteshaf.DoesNotExist:
            api_activity_logger.error("برنامه عملکرد اکتشاف با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "برنامه عملکرد اکتشاف با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در ویرایش برنامه عملکرد اکتشاف {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در ویرایش برنامه عملکرد اکتشاف"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request: Request, ipcbarnamehekteshafid: int):
        try:
            ipcbarnamehekteshaf_instance: IpcBarnamehEkteshaf = IpcBarnamehEkteshaf.objects.get(pk=ipcbarnamehekteshafid)

            ipcbarnamehekteshaf_instance.delete()
            delete_logger.warning(f"حذف برنامه عملکرد اکتشاف {ipcbarnamehekteshafid}", extra=get_details_from_request(request))
            return Response({"detail": "برنامه عملکرد اکتشاف با موفقیت حذف شد"}, status=status.HTTP_204_NO_CONTENT)

        except IpcBarnamehEkteshaf.DoesNotExist:
            api_activity_logger.error("برنامه عملکرد اکتشاف با این شناسه یافت نشد", extra=get_details_from_request(request))
            return Response({"detail": "برنامه عملکرد اکتشاف با این شناسه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            api_activity_logger.error(f"خطا در حذف برنامه عملکرد اکتشاف {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در حذف برنامه عملکرد اکتشاف"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
from collections import defaultdict
from django.db.models import Sum


# Optional: just for consistent ordering in the response, not model-related
FAZ_ORDER = ["تفصیلی", "پی‌جویی", "عمومی"]
SHAKHES_ORDER = [
    "حفاری",
    "نمونه‌برداری",
    "زمین‌شناسی (تهیه نقشه)",
    "ژئوشیمی",
    "ژئوفیزیک پهپادی",
    "ژئوفیزیک زمینی",
    "ژئوفیزیک چاه‌پیمایی",
    "ترانشه و چاهک",
]


class IpcTafazolByYear(APIView):

    def post(self, request: Request, sal: int):
        try:
            doure_list = request.data.get("doure", [])

            print(doure_list , type(doure_list))

            if not isinstance(doure_list, list):
                return Response(
                    {"detail": "دوره باید به صورت آرایه از اعداد ارسال شود"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                doure_list = [int(d) for d in doure_list]
            except (TypeError, ValueError):
                return Response(
                    {"detail": "مقادیر دوره باید عدد صحیح باشند"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            invalid_doure = [d for d in doure_list if d < 1 or d > 12]
            if invalid_doure:
                return Response(
                    {"detail": f"دوره باید بین 1 تا 12 باشد. مقادیر نامعتبر: {invalid_doure}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # de-dupe while keeping validation simple
            doure_list = sorted(set(doure_list))

            barnameh_qs: QuerySet[IpcBarnamehEkteshaf] = IpcBarnamehEkteshaf.objects.filter(sal=sal)

            if not barnameh_qs.exists():
                api_activity_logger.error(
                    "برنامه عملکرد اکتشاف برای این سال یافت نشد",
                    extra=get_details_from_request(request)
                )
                return Response(
                    {"detail": "برنامه عملکرد اکتشاف برای این سال یافت نشد"},
                    status=status.HTTP_404_NOT_FOUND
                )

            amar_qs: QuerySet[IpcAmarEkteshaf] = IpcAmarEkteshaf.objects.filter(sal=sal)

            # doure is only meaningful for amar (barnameh has no doure field)
            if doure_list:
                amar_qs = amar_qs.filter(doure__in=doure_list)

            if not amar_qs.exists():
                return Response(
                    {"detail": "هیچ آماری برای این سال / دوره(های) انتخاب‌شده یافت نشد"},
                    status=status.HTTP_404_NOT_FOUND
                )

            amar_map = {
                (row["shakhes"], row["faz"], row["vahed"]): row["total"] or 0
                for row in amar_qs.values("shakhes", "faz", "vahed").annotate(total=Sum("meghdar"))
            }
            barnameh_map = {
                (row["shakhes"], row["faz"], row["vahed"]): row["total"] or 0
                for row in barnameh_qs.values("shakhes", "faz", "vahed").annotate(total=Sum("meghdar"))
            }

            # union so combos reported only in amar (or only in barnameh) still show up
            all_keys = set(amar_map.keys()) | set(barnameh_map.keys())

            shakhes_map = defaultdict(list)
            for shakhes, faz, vahed in all_keys:
                meghdar_barnameh = barnameh_map.get((shakhes, faz, vahed), 0)
                meghdar_amar = amar_map.get((shakhes, faz, vahed), 0)
                shakhes_map[shakhes].append({
                    "faz": faz,
                    "vahed": vahed,
                    "meghdar_barnameh": meghdar_barnameh,
                    "meghdar_amar": meghdar_amar,
                    "tafazol": meghdar_amar - meghdar_barnameh,
                })

            result = []
            for shakhes, faz_details in shakhes_map.items():
                # subtotal per vahed — a shakhes can mix units
                # e.g. "ترانشه و چاهک" has both "نقطه" and "مترمکعب"
                vahed_totals = defaultdict(lambda: {"meghdar_barnameh": 0, "meghdar_amar": 0})
                for row in faz_details:
                    vahed_totals[row["vahed"]]["meghdar_barnameh"] += row["meghdar_barnameh"]
                    vahed_totals[row["vahed"]]["meghdar_amar"] += row["meghdar_amar"]

                totals_by_vahed = [
                    {
                        "vahed": vahed,
                        "meghdar_barnameh": t["meghdar_barnameh"],
                        "meghdar_amar": t["meghdar_amar"],
                        "tafazol": t["meghdar_amar"] - t["meghdar_barnameh"],
                    }
                    for vahed, t in vahed_totals.items()
                ]

                result.append({
                    "shakhes": shakhes,
                    "totals_by_vahed": totals_by_vahed,
                    "faz_details": sorted(
                        faz_details,
                        key=lambda r: FAZ_ORDER.index(r["faz"]) if r["faz"] in FAZ_ORDER else 999
                    ),
                })

            result.sort(
                key=lambda r: SHAKHES_ORDER.index(r["shakhes"]) if r["shakhes"] in SHAKHES_ORDER else 999
            )

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            api_activity_logger.error(
                f"خطا در خواندن تفاضل آمار برنامه عملکرد اکتشاف {str(e)}",
                extra=get_details_from_request(request)
            )
            return Response(
                {"detail": "خطا در خواندن تفاضل آمار برنامه عملکرد اکتشاف"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )