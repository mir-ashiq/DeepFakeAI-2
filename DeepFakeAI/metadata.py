METADATA =\
{
	'name': 'FaceFusion',
	'description': 'Next generation face swapper and enhancer',
	'version': '1.0.0',
	'license': 'MIT',
	'author': 'Henry Ruhs',
	'url': 'https://DeepFakeAI.io'
}


def get(key : str) -> str:
	return METADATA[key]
