from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom



class GalaxyUser(StructuredNode):

    user_key = StringProperty()
    username = StringProperty()
    email = StringProperty()

    owns = RelationshipTo("combat_tb_model.model.vcfmodel.VariantSet", "OWNS_SET")
