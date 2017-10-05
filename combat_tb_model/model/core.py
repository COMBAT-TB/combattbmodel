#!/usr/bin/env python

from neomodel import StructuredNode, RelationshipTo, RelationshipFrom
from neomodel import One, ZeroOrMore, OneOrMore
from neomodel import StringProperty, IntegerProperty, BooleanProperty, DateTimeProperty, FloatProperty

# class LocationRel(StructuredRel):
#     # locations are zero-based, following Chado
#     # schema for fmin/fmax, see:
#     # http://gmod.org/wiki/Chado_Sequence_Module#Feature_Locations
#     start = IntegerProperty()
#     end = IntegerProperty()
#     strand = StringProperty(choices=(('1', '+'), ('-1', '-')))

class ExternallyDescribable(StructuredNode):
    __abstract_node__ = True
    dbxref = RelationshipTo('DbXref', 'XREF', cardinality=ZeroOrMore)

class Organism(ExternallyDescribable):
    abbreviation = StringProperty()
    genus = StringProperty(required=True)
    species = StringProperty(required=True)
    strain = StringProperty()
    common_name = StringProperty(required=True)
    comment = StringProperty()


class Publication(StructuredNode):
    pmid = StringProperty(required=True, unique_index=True)
    title = StringProperty(required=True)
    volumetitle = StringProperty()
    volume = StringProperty()
    series_name = StringProperty()
    issue = StringProperty()
    year = IntegerProperty(required=True)
    pages = StringProperty()
    miniref = StringProperty()
    uniquename = StringProperty()
    is_obsolete = BooleanProperty(default=False)
    publisher = StringProperty()
    pubplace = StringProperty()

    author = RelationshipFrom('Author', 'WROTE', cardinality=OneOrMore)

class Author(StructuredNode):
    editor = StringProperty()
    surname = StringProperty(required=True, index=True)
    givennames = StringProperty(required=True, index=True)
    suffix = StringProperty()
    rank = IntegerProperty()

    wrote = RelationshipTo('Publication', 'WROTE', cardinality=ZeroOrMore)


class DbXref(StructuredNode):
    accession = StringProperty(required=True, index=True)
    version = StringProperty()
    db = StringProperty(required=True, unique_index=True)
    description = StringProperty()
    uri = StringProperty()

    refers_to = RelationshipFrom('ExternallyDefined', 'XREF', cardinality=OneOrMore)

class Location(StructuredNode):
    # the feature location model is inspired by
    # Chado: http://gmod.org/wiki/Chado_Sequence_Module#Feature_Locations

    location_key = StringProperty(required=True, unique_index=True)
    start = IntegerProperty(required=True)
    end = IntegerProperty(required=True)
    strand = StringProperty(choices=(('1','+'), ('-1', '-')), required=True)

    feature = RelationshipTo('Feature', 'ON', cardinality=One)

class Feature(ExternallyDescribable):
    # __abstract_node__ = True

    name = StringProperty()
    uniquename = StringProperty(required=True, unique_index=True)
    residues = StringProperty()
    seqlen = IntegerProperty()
    md5checksum = StringProperty()
    is_analysis = BooleanProperty(default=False)
    is_obsolete = BooleanProperty(default=False)
    timeaccessioned = DateTimeProperty()
    timelastmodified = DateTimeProperty()
    ontology_id = StringProperty()  # WHAT IS THIS?

    location = RelationshipTo('Location', 'LOCATED_AT', cardinality=ZeroOrMore)
    belongs_to = RelationshipTo('Organism', 'BELONGS_TO', cardinality=One)
    published_in = RelationshipTo('Publication', 'PUBLISHED_IN')
    go_terms = RelationshipTo('GoTerm', 'ASSOC_WITH', cardinality=ZeroOrMore)
    orthologous_to = RelationshipTo('Feature', 'ORTHOLOGOUS_TO')


class RepeatRegion(Feature):
    so_id = 'SO:0000657'
    description = StringProperty()

class Transcribed(Feature):
    __abstract_node__ = True

class Trna(Transcribed):
    so_id = "SO:0000253"

class NCrna(Transcribed):
    so_id = "SO:0000655"


class Rrna(Transcribed):
    so_id = "SO:0000252"

class PseudoGene(Transcribed):
    so_id = "SO:0000336"

    biotype = StringProperty(choices=(('pseudogene', 'pseudogene'),), default='pseudogene')
    description = StringProperty()

class Gene(Transcribed):
    so_id = "SO:0000704"

    biotype = StringProperty(choices=(('protein_coding', 'protein_coding'),), default='protein_coding')
    description = StringProperty()
    # TODO: transcripts or parts ??
    transcripts = RelationshipFrom('Transcript', 'PART_OF', cardinality=ZeroOrMore)

class Transcript(Feature):
    so_id = "SO:0000673"

    # NOTE:
    # In Ensembl GFF3 biotype is inherited from the parent feature, which can be
    # (at least?) protein_coding, ncRNA or tRNA. In the current model we are only
    # storing transcripts for genes.
    biotype = StringProperty(required=True, choices=(
            ('protein_coding', 'protein_coding'),
            ('ncRNA', 'ncRNA'),
            ('tRNA', 'tRNA'),
            ('rRNA', 'rRNA'),
            ('pseudogene', 'pseudogene')))
    part_of = RelationshipTo('Transcribed', 'PART_OF')
    # TODO: exons or parts ??
    exons = RelationshipFrom('Exon', 'PART_OF', cardinality=ZeroOrMore)

class Exon(Feature):
    so_id = "SO:0000147"

    part_of = RelationshipTo('Transcript', 'PART_OF', cardinality=One)

class CDS(Feature):
    so_id = "SO:0000316"

    part_of = RelationshipTo('Transcript', 'PART_OF', cardinality=One)
    protein = RelationshipFrom('Protein', 'DERIVES_FROM', cardinality=ZeroOrMore)

class Protein(Feature):
    so_id = "SO:0000104"

    family = StringProperty()
    function = StringProperty()
    # NOTE: proteins can have multiple domains across their length, consider
    # replacing this with a protein domain feature that is located on the
    # protein
    domain = StringProperty()
    three_d = StringProperty()
    mass = FloatProperty()

    derives_from = RelationshipTo('CDS', 'DERIVES_FROM', cardinality=One)
    interacts_with = RelationshipTo('Protein', 'INTERACTS_WITH', cardinality=ZeroOrMore)
    interpro_terms = RelationshipTo('InterProTerm', 'ASSOC_WITH', cardinality=ZeroOrMore)

class Chromosome(Feature):
    so_id = "SO:0000340"

    features = RelationshipFrom('Feature', 'LOCATED_ON')

class Contig(Feature):
    so_id = "SO:0000149"

    features = RelationshipFrom('Feature', 'LOCATED_ON')

class InterProTerm(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    definition = StringProperty()

    proteins = RelationshipFrom('Protein', 'ASSOC_WITH', cardinality=OneOrMore)

class GoTerm(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    definition = StringProperty()
    is_obsolete = BooleanProperty(default=False)
    namespace = StringProperty(choices=(
            ('biological_process', 'biological_process'),
            ('cellular_component', 'cellular_component'),
            ('molecular_function', 'molecular_function')))

    is_a = RelationshipTo('GoTerm', 'IS_A')
    part_of = RelationshipTo('GoTerm', 'PART_OF')
    feature = RelationshipFrom('Feature', 'ASSOC_WITH', cardinality=OneOrMore)

class Pathway(StructuredNode):
    """
    Pathway
    """
    __primarykey__ = 'accession'

    accession = StringProperty(unique_index=True, required=True)
    source = StringProperty(required=True, index=True, choices=(('kegg', 'kegg'), ('reactome', 'reactome')))
    _type = StringProperty()
    species = StringProperty()
    _class = StringProperty()
    name = StringProperty()
    compartment = StringProperty()
    # Description
    summation = StringProperty()

    protein = RelationshipFrom("Protein", "INVOLVED_IN", cardinality=OneOrMore)
