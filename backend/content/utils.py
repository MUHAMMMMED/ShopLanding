from .models import *
 

def link_and_save_module(page_id, section_id, module_name, module_related_id):
    """
    Links a new module to a section and assigns the related ID.
    """
    # Fetch the section based on the provided sectionId and pageId
    section = Section.objects.get(pk=section_id, page_id=page_id)

    # Validate the module type
    if module_name not in dict(Module.MODULE_TYPES).keys():
        raise ValueError('Invalid module name')

    # Create a new module
    new_module = Module.objects.create(section=section, module_type=module_name)

    # Dynamically assign the related ID to the correct field
    related_field = f"{module_name}_id"  # e.g., "header_id", "slider_id", etc.
    if hasattr(new_module, related_field):
        setattr(new_module, related_field, module_related_id)
        new_module.save()
    else:
        raise ValueError(f'Module type "{module_name}" does not support related ID.')

    return new_module