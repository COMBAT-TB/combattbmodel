from neomodel import StructuredNode, StringProperty, RelationshipFrom

class FastTree(StructuredNode):
    name = StringProperty(required=True, unique_index=True)
    data = StringProperty(required=True)
    history_id = StringProperty(index=True)

    from_variant_set = RelationshipFrom("combat_tb_model.model.vcfmodel.VariantSet", "FROM_VARIANT_SET")

