from __future__ import print_function
import argparse
import scrapy

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('id',type=str,
		metavar='Symbol/ENSGid/Key words',
		help="Argument [id] is mandetody. You can put gene symbol, ENSG id, and any keys words.")
	args = parser.parse_args()
	
	print(WebCrawler(args.id))

def WebCrawler(id):
	#어라 막혔네? ㅠㅠ

if __name__=="__main__":
	main()