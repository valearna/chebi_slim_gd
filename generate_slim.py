import argparse
import logging
import pathlib

from genedescriptions.trimming import TrimmingAlgorithmIC
from genedescriptions.data_manager import DataManager
from genedescriptions.commons import DataType
from genedescriptions.config_parser import GenedescConfigParser


def main():
    parser = argparse.ArgumentParser(description='Generate a slim version of the ontology starting from a list of '
                                                 'annotated nodes, using the AGR gene descriptions library')
    parser.add_argument('-o', '--ontology', type=str, required=True, help='Path to the ontology file')
    parser.add_argument('-a', '--annotated_nodes', required=True, type=str,
                        help='Path to the file containing annotated nodes')
    parser.add_argument('-c', '--config', required=True, type=str, help='Path to the config file')

    args = parser.parse_args()

    logging.getLogger().setLevel(logging.INFO)

    annotated_onto_nodes = [line.strip() for line in open(args.annotated_nodes)]
    config = GenedescConfigParser(args.config)
    dm = DataManager(go_relations=["subClassOf", "BFO:0000050"])

    dm.load_ontology_from_file(ontology_type=DataType.GO, ontology_url=pathlib.Path(args.ontology).as_uri(),
                               ontology_cache_path='/tmp/genedescriptions/ontology.obo', config=config)
    trimming_ic = TrimmingAlgorithmIC(ontology=dm.go_ontology)
    trimming_result = trimming_ic.trim(node_ids=annotated_onto_nodes, max_num_nodes=10, min_distance_from_root=4)
    print(trimming_result.final_terms)


if __name__ == '__main__':
    main()


