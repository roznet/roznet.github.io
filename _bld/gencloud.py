#!/Users/brice/anaconda3/bin/python3

import argparse
import os
from wordcloud import WordCloud
import random

def grey_color_func( word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(50, 90)

class Generator:
    def __init__(self,args):
        self.args = args


    def generate(self):
        for name in self.args.source:
            if name.endswith( '.md' ) and os.path.isfile( name ):
                self.generate_one( name )

    def generate_one(self,name):
        if os.path.isdir( self.args.outdir ):
            outname = os.path.join( self.args.outdir, os.path.basename( name )[:-len('md')] + "png" )
            fp = open( name, 'r' )
            text = fp.read()
            #wordcloud = WordCloud( max_words = 30, background_color = (21,21,21), color_func=grey_color_func).generate( text )
            wordcloud = WordCloud( max_words = 30, background_color = (21,21,21)).generate( text )
            #wordcloud.recolor( color_func=grey_color_func, random_state=3)
            print( "{} -> {}".format( name, outname ) )
            wordcloud.to_file( outname )


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser( description='Generate word cloud image' )
    parser.add_argument( 'source', metavar='Arguments', nargs='*' )
    parser.add_argument( '-o', '--outdir', help='directory for the output', default='../assets/clouds')

    args = parser.parse_args()

    generator = Generator( args )
    generator.generate()
