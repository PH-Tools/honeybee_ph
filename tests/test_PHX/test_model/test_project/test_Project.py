from PHX.model import project, constructions


def test_blank_project(reset_class_counters):
    proj = project.PhxProject()

    assert str(proj)
    assert not proj.assembly_types
    assert not proj.window_types
    assert not proj.utilization_patterns_ventilation
    assert not proj.utilization_patterns_ph
    assert not proj.variants


def test_project_data(reset_class_counters):
    proj = project.PhxProject()

    # -- Set all the data
    fields = ['name', 'street', 'city', 'post_code',
              'telephone', 'email', 'license_number']
    group_types = ['customer', 'building', 'owner', 'responsible']
    for group_name in group_types:
        gr_attr = getattr(proj.project_data, group_name)
        for field in fields:
            setattr(gr_attr, field, f"{group_name}_{field}")

    # --- Customer
    assert proj.project_data.customer.name == 'customer_name'
    assert proj.project_data.customer.street == 'customer_street'
    assert proj.project_data.customer.city == 'customer_city'
    assert proj.project_data.customer.post_code == 'customer_post_code'
    assert proj.project_data.customer.telephone == 'customer_telephone'
    assert proj.project_data.customer.email == 'customer_email'
    assert proj.project_data.customer.license_number == 'customer_license_number'

    # --- Building
    assert proj.project_data.building.name == 'building_name'
    assert proj.project_data.building.street == 'building_street'
    assert proj.project_data.building.city == 'building_city'
    assert proj.project_data.building.post_code == 'building_post_code'
    assert proj.project_data.building.telephone == 'building_telephone'
    assert proj.project_data.building.email == 'building_email'
    assert proj.project_data.building.license_number == 'building_license_number'

    # --- Owner
    assert proj.project_data.owner.name == 'owner_name'
    assert proj.project_data.owner.street == 'owner_street'
    assert proj.project_data.owner.city == 'owner_city'
    assert proj.project_data.owner.post_code == 'owner_post_code'
    assert proj.project_data.owner.telephone == 'owner_telephone'
    assert proj.project_data.owner.email == 'owner_email'
    assert proj.project_data.owner.license_number == 'owner_license_number'

    # --- Responsible
    assert proj.project_data.responsible.name == 'responsible_name'
    assert proj.project_data.responsible.street == 'responsible_street'
    assert proj.project_data.responsible.city == 'responsible_city'
    assert proj.project_data.responsible.post_code == 'responsible_post_code'
    assert proj.project_data.responsible.telephone == 'responsible_telephone'
    assert proj.project_data.responsible.email == 'responsible_email'
    assert proj.project_data.responsible.license_number == 'responsible_license_number'


def test_add_variant_to_project(reset_class_counters):
    proj = project.PhxProject()

    assert not proj.variants

    var_1 = project.Variant()
    var_2 = project.Variant()

    assert var_1.id_num == 1
    assert var_2.id_num == 2

    proj.add_new_variant(var_1)
    assert len(proj.variants) == 1
    assert var_1 in proj.variants
    assert var_2 not in proj.variants

    proj.add_new_variant(var_2)
    assert len(proj.variants) == 2
    assert var_1 in proj.variants
    assert var_2 in proj.variants


def test_add_assembly_to_project(reset_class_counters):
    pr_1 = project.PhxProject()

    assmbly_1 = constructions.Assembly()
    assmbly_2 = constructions.Assembly()

    pr_1.add_new_assembly(assmbly_1.identifier, assmbly_1)
    assert pr_1.assembly_in_project(assmbly_1.identifier)
    assert not pr_1.assembly_in_project(assmbly_2.identifier)
    assert assmbly_1 in pr_1.assembly_types
    assert assmbly_2 not in pr_1.assembly_types

    pr_1.add_new_assembly(assmbly_2.identifier, assmbly_2)
    assert pr_1.assembly_in_project(assmbly_2.identifier)
    assert pr_1.assembly_in_project(assmbly_2.identifier)
    assert assmbly_1 in pr_1.assembly_types
    assert assmbly_2 in pr_1.assembly_types

    pr_2 = project.PhxProject()
    assert not pr_2.assembly_in_project(assmbly_1.identifier)
    assert not pr_2.assembly_in_project(assmbly_2.identifier)
    assert assmbly_1 not in pr_2.assembly_types
    assert assmbly_2 not in pr_2.assembly_types
