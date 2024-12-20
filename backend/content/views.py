from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *
# from products.models import Product
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .utils import *
from django.conf import settings  
 

class SettingView(APIView):
    def get(self, request):
      settings = Settings.objects.first()   
      serializer = Settings_Serializer(settings)
      return Response(serializer.data)


 
class PageView(viewsets.ReadOnlyModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    
    # Override get_queryset to allow fetching by ID
    def get_queryset(self):
        # Get the 'id' parameter from the URL
        page_id = self.kwargs.get('pk')
        if page_id:
            return Page.objects.filter(id=page_id)  # Filter by ID
        return Page.objects.all()  # Return all pages if no ID is provided


class PageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Page.objects.all()
    serializer_class = PageSerializer
 

class LinksViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Links.objects.all()
    serializer_class = LinksSerializer
  
class LinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Links
        fields = '__all__'


# https://yourdomain.com/?utm_source=facebook&utm_medium=social&utm_campaign=spring_sale

class PageLinksView(APIView):
    def get(self, request, pk=None):
        current_site = settings.DOMAIN  # Replace with your actual domain

        if not pk:
            return Response({"error": "Page ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the page by ID
            page = Page.objects.get(id=pk)
        except Page.DoesNotExist:
            return Response({"error": "Invalid Page ID"}, status=status.HTTP_404_NOT_FOUND)

        # Fetch related links
        links = Links.objects.filter(page_id=pk)

        # Prepare response data
        data = []
        for link in links:
            # Extract UTM parameters from related fields
            utm_source = link.source.dictionary_source.name if link.source else None
            utm_medium = link.medium.dictionary_medium.name if link.medium else None
            utm_campaign = link.campaign.dictionary_campaign.name if link.campaign else None

            # Construct base link
            base_link = f"{current_site}/page/{page.title}/{page.id}/"

            # Add UTM parameters to the link
            utm_params = []
            if utm_source:
                utm_params.append(f"utm_source={utm_source}")
            if utm_medium:
                utm_params.append(f"utm_medium={utm_medium}")
            if utm_campaign:
                utm_params.append(f"utm_campaign={utm_campaign}")

            # Final UTM link
            utm_link = f"{base_link}?{'&'.join(utm_params)}" if utm_params else base_link

            # Assuming there is a 'platform' field in the Link model
            platform = utm_source if utm_source is not None else "Unknown"

            # Add to response data
            data.append({
                "id": link.id,
                "url": utm_link,
                "platform": platform,
            })

        return Response(data, status=status.HTTP_200_OK)





class SettingsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        settings = Settings.objects.first()   
        serializer = SettingsSerializer(settings)
        return Response(serializer.data)

    def post(self, request):
        serializer = SettingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        settings = Settings.objects.first()  # Update first settings entry
        serializer = SettingsSerializer(settings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 







class SectionViewSet(viewsets.ModelViewSet):
     permission_classes = [IsAuthenticated]
     queryset = Section.objects.all().prefetch_related('modules')
     serializer_class = SectionSerializer
 

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
 
class AddModuleToPage(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        # Retrieve data from the request body
        page_id = request.data.get('pageId')
        section_id = request.data.get('sectionId')
        module_name = request.data.get('moduleName')
        module_related_id = request.data.get('Id')

        try:
            # Use the helper function to link and save the module
            new_module = link_and_save_module(page_id, section_id, module_name, module_related_id)
            
            # Return a success response
            return Response({'message': 'Module added successfully to the page.','module_id': new_module.id},status=status.HTTP_201_CREATED)
                             
        except Section.DoesNotExist:
            return Response({'error': 'Section not found for the provided page and section IDs.'},status=status.HTTP_404_NOT_FOUND)
                            
        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # General error handling

            return Response({'error': 'An error occurred while adding the module to the page.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


  
class CloneSectionView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def create(self, request, pk=None):
        try:
            # احصل على القسم الأصلي
            original_section = Section.objects.get(pk=pk)
            # احصل على ID الصفحة من الطلب
            new_page_id = request.data.get('page_id')
            # انسخ بيانات القسم الأصلي
            new_section_data = {
                'title': original_section.title,
                'mobile_order': original_section.mobile_order,
                'tablet_order': original_section.tablet_order,
                'desktop_order': original_section.desktop_order,
                'page_id': new_page_id,   
            }

            # أنشئ قسم جديد
            new_section = Section.objects.create(**new_section_data)

            # انسخ جميع الموديولات المرتبطة بالقسم الأصلي
            for module in original_section.modules.all():
                new_module_data = {
                    'section': new_section,
                    'module_type': module.module_type,
                    'mobile_order': module.mobile_order,
                    'tablet_order': module.tablet_order,
                    'desktop_order': module.desktop_order,
                }
                new_module = Module.objects.create(**new_module_data)

                # انسخ تفاصيل الموديول بناءً على نوعه
                try:
                    if module.module_type == 'header':
                        HeaderModule.objects.create(
                            # module=new_module,
                            # device_Types=module.header.device_Types,
                            themes_desktop_Types=module.header.themes_desktop_Types,
                            themes_tablet_Types=module.header.themes_tablet_Types,
                            themes_mobile_Types=module.header.themes_mobile_Types,
                            is_mobile=module.header.is_mobile,
                            is_tablet=module.header.is_tablet,
                            is_desktop=module.header.is_desktop,
                            content=module.header.content,
                        )
                    elif module.module_type == 'slider':
                        SliderModule.objects.create(
                            # module=new_module,
                            # device_Types=module.slider.device_Types,
                            themes_desktop_Types=module.slider.themes_desktop_Types,
                            themes_tablet_Types=module.slider.themes_tablet_Types,
                            themes_mobile_Types=module.slider.themes_mobile_Types,
                            is_mobile=module.slider.is_mobile,
                            is_tablet=module.slider.is_tablet,
                            is_desktop=module.slider.is_desktop,
                            images=module.slider.images,  # تأكد من التعامل مع الصور بشكل صحيح
                        )
                    elif module.module_type == 'content':
                        ContentModule.objects.create(
                            # module=new_module,
                            # device_Types=module.content.device_Types,
                            themes_desktop_Types=module.content.themes_desktop_Types,
                            themes_tablet_Types=module.content.themes_tablet_Types,
                            themes_mobile_Types=module.content.themes_mobile_Types,
                            is_mobile=module.content.is_mobile,
                            is_tablet=module.content.is_tablet,
                            is_desktop=module.content.is_desktop,
                            text=module.content.text,
                        )
                    elif module.module_type == 'footer':
                        FooterModule.objects.create(
                            # module=new_module,
                            # device_Types=module.footer.device_Types,
                            themes_desktop_Types=module.footer.themes_desktop_Types,
                            themes_tablet_Types=module.footer.themes_tablet_Types,
                            themes_mobile_Types=module.footer.themes_mobile_Types,
                            is_mobile=module.footer.is_mobile,
                            is_tablet=module.footer.is_tablet,
                            is_desktop=module.footer.is_desktop,
                            content=module.footer.content,
                        )
                except Exception as e:
                    # إذا كان هناك استثناء، يمكنك إما تسجيله أو تجاهله
                    print(f"Error copying module {module.id}: {str(e)}")
                    continue  # تخطي هذا الموديول إذا كان هناك خطأ

            return Response(SectionSerializer(new_section).data, status=status.HTTP_201_CREATED)

        except Section.DoesNotExist:
            return Response({'detail': 'Section not found.'}, status=status.HTTP_404_NOT_FOUND)

class UpdateSectionOrderView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        sections = request.data.get('sections', [])
        device_type = request.data.get('DeviceTYPES', '').lower()   
        print('device_type',device_type)
        if not sections:
            return Response({'error': 'No sections provided.'}, status=status.HTTP_400_BAD_REQUEST)

        if device_type not in ['mobile', 'tablet', 'desktop']:
            return Response({'error': 'Invalid DeviceTYPES provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            for index, section_data in enumerate(sections):
                unique_id = section_data.get('unique_id')
                if not unique_id:
                    return Response({'error': 'unique_id missing in one of the sections.'}, status=status.HTTP_400_BAD_REQUEST)

                section = Section.objects.get(unique_id=unique_id)

                # Dynamically set the order based on device type
                order_field = f"{device_type}_order"
                setattr(section, order_field, index)
                section.save()
            return Response({'status': 'Order updated successfully.'}, status=status.HTTP_200_OK)

        except Section.DoesNotExist:
            return Response({'error': 'One or more sections not found.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class UpdateModuleOrderView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        modules = request.data.get('modules', [])
        device_type = request.data.get('DeviceTYPES', '').lower()  # Ensure consistency in casing
        print('device_type',device_type)
        if not modules:
            return Response({'error': 'No modules provided.'}, status=status.HTTP_400_BAD_REQUEST)
        if device_type not in ['mobile', 'tablet', 'desktop']:
            return Response({'error': 'Invalid DeviceTYPES provided.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            for index, module_data in enumerate(modules):
                unique_id = module_data.get('unique_id')
                if not unique_id:
                    return Response({'error': 'unique_id missing in one of the modules.'}, status=status.HTTP_400_BAD_REQUEST)

                module = Module.objects.get(unique_id=unique_id)
                # Dynamically set the order based on device type
                order_field = f"{device_type}_order"
                setattr(module, order_field, index)
                module.save()
            return Response({'status': 'Order updated successfully.'}, status=status.HTTP_200_OK)

        except Module.DoesNotExist:
            return Response({'error': 'One or more modules not found.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  
class ActiveStateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        module_id = request.data.get('moduleId')
        module_name = request.data.get('moduleName')
        is_active = request.data.get('isActive')
        device_type = request.data.get('DeviceTYPES')
        print('device_type',device_type)
        module = None
        try:
            # 1 = header
            if module_name == 1:
                module = HeaderModule.objects.get(id=module_id)
            elif module_name == 2:
            # 2 = content
                module = ContentModule.objects.get(id=module_id)
            elif module_name == 3:
            # 3 = slide
                module = SliderModule.objects.get(id=module_id)
            elif module_name == 4:
            # 4 = footer
                module = FooterModule.objects.get(id=module_id)
            else:
                return Response({"error": "Invalid module name"}, status=status.HTTP_400_BAD_REQUEST)
 
            # تحديث الحالة النشطة
            if device_type == 'desktop':
                module.is_desktop = is_active
            elif device_type == 'mobile':
                module.is_mobile = is_active
            elif device_type == 'tablet':
                module.is_tablet = is_active
            module.save()
            return Response({"status": "success"}, status=status.HTTP_200_OK)

        except (HeaderModule.DoesNotExist, SliderModule.DoesNotExist, 
                ContentModule.DoesNotExist, FooterModule.DoesNotExist) as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "An error occurred: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
 




 