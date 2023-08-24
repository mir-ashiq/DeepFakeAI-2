METADATA =\
{
	'name': 'DeepFakeAI',
	'description': 'Next generation face swapper and enhancer',
	'version': '1.0.0',
	'license': 'MIT',
	'author': 'Ashiq Hussain Mir',
	'url': 'https://codegenius.me'
}


def get(key : str) -> str:
	return METADATA[key]
