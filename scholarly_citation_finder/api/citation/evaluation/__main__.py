import os
import argparse
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scholarly_citation_finder.settings.development") 
django.setup()

from Evaluation import Evaluation


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start a evulation process.')
    parser.add_argument('name',
                        help='evulation name')
    parser.add_argument('--setsize', type=int, required=True,
                        help='author set size')
    parser.add_argument('--minpublications', type=int, default=0, dest='num_min_publications',
                        help='')       
    args = parser.parse_args()
    
    print(args)
    e = Evaluation(args.name)
    e.create_random_author_set(setsize=args.setsize, num_min_publications=args.num_min_publications)