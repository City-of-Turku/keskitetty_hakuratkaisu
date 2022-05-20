import pytest
from nlp_client import NLPProcessorClient

@pytest.fixture
def api_url():
    return "http://host.docker.internal:15000"

@pytest.fixture
def raw_content():
    return '''Mieleni minun tekevi, aivoni ajattelevi lähteäni laulamahan, saa'ani sanelemahan, sukuvirttä suoltamahan, lajivirttä laulamahan. Sanat suussani sulavat, puhe'et putoelevat, kielelleni kerkiävät, hampahilleni hajoovat.'''

@pytest.fixture
def preprocessed_content():
    return 'mieleni minun tekevi aivoni ajattelevi lähteäni laulamahan sanelemahan sukuvirttä suoltamahan lajivirttä sanat suussani sulavat putoelevat kielelleni kerkiävät hampahilleni hajoovat'

@pytest.fixture
def ready_for_nlp_content():
    return 'mieleni tekevi aivoni ajattelevi lähteäni sukuvirttä suoltamahan lajivirttä sanat suussani sulavat putoelevat kielelleni kerkiävät hampahilleni'

@pytest.fixture
def dictionary(tmp_path):
    content = '''minun => minä
tekee => tehdä
sanaton => sanaton
sana => sana
hajoovat => hajota
onomatopoeettinen => onomatopoeettinen
laulamahan => laulaa
sanelemahan => sanella
'''

    d = tmp_path / "tmp"
    d.mkdir()
    p = d / "nlp_dictionary.txt"
    p.write_text(content, encoding='utf-8')

    return p

@pytest.fixture
def stemmed_content():
    return ['mieleni => mieli', 'tekevi => tehdä', 'aivoni => aivot', 'ajattelevi => ajatella', 'lähteäni => lähti', 'sukuvirttä => sukuvirsi', 'suoltamahan => suoltaa', 'lajivirttä => lajivirsi', 'sanat => sana', 'suussani => suussa', 'sulavat => sulkaa', 'putoelevat => pudoella', 'kielelleni => kieli', 'kerkiävät => keritä', 'hampahilleni => hampah']

@pytest.fixture
def dictionary_after_add_results():
    return '''minun => minä
tekee, tekevi => tehdä
sanaton => sanaton
sana, sanat => sana
hajoovat => hajota
onomatopoeettinen => onomatopoeettinen
laulamahan => laulaa
sanelemahan => sanella
mieleni => mieli
aivoni => aivot
ajattelevi => ajatella
lähteäni => lähti
sukuvirttä => sukuvirsi
suoltamahan => suoltaa
lajivirttä => lajivirsi
suussani => suussa
sulavat => sulkaa
putoelevat => pudoella
kielelleni => kieli
kerkiävät => keritä
hampahilleni => hampah
'''

def test_remove_non_alpha_and_duplicates(api_url, raw_content, preprocessed_content, dictionary):
    nlp = NLPProcessorClient(api_url, dictionary)
    assert nlp.remove_non_alpha_and_duplicates(raw_content) == preprocessed_content

def test_remove_existing(tmp_path, api_url, preprocessed_content, dictionary, ready_for_nlp_content):
    nlp = NLPProcessorClient(api_url, dictionary)
    assert nlp.remove_existing(preprocessed_content) == ready_for_nlp_content

def test_process_with_nlp(api_url, ready_for_nlp_content, stemmed_content, dictionary):
    nlp = NLPProcessorClient(api_url, dictionary)
    assert nlp.process_with_nlp(ready_for_nlp_content) == stemmed_content

def test_add_results(tmp_path, api_url, stemmed_content, dictionary, dictionary_after_add_results):
    nlp = NLPProcessorClient(api_url, dictionary)
    nlp.add_results(stemmed_content)
    
    with open(dictionary, encoding='utf-8') as file:
        assert file.read() == dictionary_after_add_results